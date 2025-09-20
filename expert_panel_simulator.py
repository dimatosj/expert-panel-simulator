#!/usr/bin/env python3
"""
Expert Panel Simulator - Generic Multi-Agent Expert Review System

Creates virtual expert panels to review and discuss any topic, document, or idea.
Supports multiple AI providers (OpenAI, Anthropic) with comprehensive analytics.

Usage:
    python expert_panel_simulator.py --topic "My Product Idea" --domain technology
    python expert_panel_simulator.py --document design.md --experts 5
    python expert_panel_simulator.py --config my_config.yaml
"""

import os
import sys
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import traceback

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.llm_provider import LLMManager, TokenUsage
from config.expert_templates import get_expert_set, create_custom_expert, get_available_domains, SAMPLE_CONFIGURATIONS

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠ python-dotenv not installed. Using environment variables only.")

try:
    import autogen
    from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    print("❌ AutoGen not available. Install with: pip install pyautogen==0.2.35")
    sys.exit(1)


class ExpertPanelSimulator:
    """Main class for running expert panel simulations."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the simulator with configuration."""
        self.config = config
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(config.get('OUTPUT_DIR', 'outputs')) / f"session_{self.session_id}"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize LLM manager
        self.llm_manager = LLMManager(config)

        # Session tracking
        self.start_time = datetime.now()
        self.metadata = {
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat(),
            'config': self._sanitize_config(config)
        }

        print(f"🚀 Expert Panel Simulator initialized")
        print(f"📁 Session: {self.session_id}")
        print(f"💾 Output: {self.output_dir}")

    def _sanitize_config(self, config: Dict) -> Dict:
        """Remove sensitive information from config for logging."""
        sanitized = config.copy()
        sensitive_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
        for key in sensitive_keys:
            if key in sanitized:
                sanitized[key] = "***"
        return sanitized

    def create_expert_panel(self, topic: str, domain: str = None, expert_names: List[str] = None, custom_experts: List[Dict] = None) -> Dict[str, AssistantAgent]:
        """Create a panel of expert agents."""
        experts = {}

        if custom_experts:
            # Use custom expert definitions
            for expert_def in custom_experts:
                expert = self._create_expert_agent(
                    expert_def['name'],
                    expert_def['expertise'],
                    expert_def.get('perspective', ''),
                    expert_def.get('background', ''),
                    topic
                )
                experts[expert_def['name'].lower().replace(' ', '_')] = expert

        elif expert_names and domain:
            # Use specific experts from a domain
            domain_experts = get_expert_set(domain)
            for expert_name in expert_names:
                if expert_name in domain_experts:
                    template = domain_experts[expert_name]
                    expert = self._create_expert_agent(
                        template.name,
                        template.expertise,
                        template.perspective,
                        template.background,
                        topic
                    )
                    experts[expert_name] = expert

        elif domain:
            # Use all experts from a domain
            domain_experts = get_expert_set(domain)
            max_experts = int(self.config.get('DEFAULT_EXPERT_COUNT', 5))

            for i, (key, template) in enumerate(domain_experts.items()):
                if i >= max_experts:
                    break
                expert = self._create_expert_agent(
                    template.name,
                    template.expertise,
                    template.perspective,
                    template.background,
                    topic
                )
                experts[key] = expert

        else:
            raise ValueError("Must specify either domain, expert_names, or custom_experts")

        print(f"👥 Created {len(experts)} experts: {', '.join([e.name for e in experts.values()])}")
        return experts

    def _create_expert_agent(self, name: str, expertise: str, perspective: str, background: str, topic: str) -> AssistantAgent:
        """Create an individual expert agent."""

        # Get verbosity settings
        verbosity = self.config.get('VERBOSITY', 'normal')
        max_length = int(self.config.get('MAX_RESPONSE_LENGTH', 200))
        response_format = self.config.get('RESPONSE_FORMAT', 'paragraph')

        # Set length instructions based on verbosity
        length_instructions = {
            'concise': f"Keep responses VERY brief (50-100 words max). Get straight to the point.",
            'normal': f"Keep responses focused (100-{max_length} words). Be clear but thorough.",
            'verbose': f"Provide detailed analysis ({max_length}-400 words). Include examples and nuance."
        }

        format_instructions = {
            'bullet_points': "Use bullet points for key insights. No long paragraphs.",
            'paragraph': "Use 1-2 clear paragraphs.",
            'detailed': "Provide comprehensive analysis with sections and examples."
        }

        system_prompt = f"""You are {name}, an expert in {expertise}.

BACKGROUND: {background}

PERSPECTIVE: {perspective}

You are participating in an expert panel discussion about: {topic}

RESPONSE GUIDELINES:
- VERBOSITY: {verbosity.upper()}
- {length_instructions.get(verbosity, length_instructions['normal'])}
- FORMAT: {format_instructions.get(response_format, format_instructions['paragraph'])}

INSTRUCTIONS:
- Provide insights from your unique expertise and perspective
- Be specific and actionable in your recommendations
- Reference your professional experience when relevant
{"- Build on or respectfully disagree with other experts" if self.config.get('ENABLE_EXPERT_INTERACTION', 'true').lower() == 'true' else "- Focus on your own expert analysis"}
- Use your authentic voice and known approaches
- Be constructive and professional

DISCUSSION STYLE: {self.config.get('DISCUSSION_STYLE', 'formal')}

CRITICAL: You MUST keep responses {verbosity}. Maximum {max_length} words per response.

Remember: You are {name} - stay true to your known methodologies and approaches."""

        # Create AutoGen config for this agent
        autogen_config = {
            "config_list": [
                {
                    "model": self.config.get('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022'),
                    "api_key": self.config.get('ANTHROPIC_API_KEY'),
                    "api_type": "anthropic"
                }
            ],
            "temperature": float(self.config.get('TEMPERATURE', 0.7)),
            "timeout": 600,
        }

        # Override if using OpenAI
        if self.config.get('PRIMARY_PROVIDER') == 'openai':
            autogen_config["config_list"][0] = {
                "model": self.config.get('OPENAI_MODEL', 'gpt-4o'),
                "api_key": self.config.get('OPENAI_API_KEY'),
                "api_type": "openai"
            }

        return AssistantAgent(
            name=name.split('(')[0].strip(),  # Clean name for AutoGen
            system_message=system_prompt,
            llm_config=autogen_config,
            max_consecutive_auto_reply=10
        )

    def run_simulation(self, topic: str, document_content: str = None, rounds: List[str] = None, **kwargs) -> Dict[str, Any]:
        """Run the complete expert panel simulation."""
        print(f"\n🎯 Starting simulation: {topic}")

        # Create expert panel
        experts = self.create_expert_panel(topic, **kwargs)

        # Create moderator
        moderator = self._create_moderator(topic, rounds)

        # Create user proxy for coordination
        user_proxy = UserProxyAgent(
            name="coordinator",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False
        )

        # Set up group chat
        all_agents = [user_proxy] + [moderator] + list(experts.values())
        group_chat = GroupChat(
            agents=all_agents,
            messages=[],
            max_round=int(self.config.get('MAX_ROUNDS', 8)),
            speaker_selection_method="round_robin"
        )

        manager = GroupChatManager(groupchat=group_chat, llm_config=moderator.llm_config)

        # Prepare initial prompt
        if document_content:
            initial_message = f"""We are conducting an expert panel review of the following:

TOPIC: {topic}

DOCUMENT:
{document_content}

Please provide your expert analysis and recommendations. Each expert should share their perspective based on their area of expertise."""
        else:
            initial_message = f"""We are conducting an expert panel discussion on: {topic}

Each expert should provide their analysis, insights, and recommendations from their unique professional perspective. Feel free to build on each other's ideas or offer alternative viewpoints."""

        # Run the simulation
        print("🗣️ Starting expert discussion...")

        try:
            chat_result = user_proxy.initiate_chat(
                manager,
                message=initial_message,
                clear_history=True
            )

            # Process results
            transcript = self._extract_transcript(chat_result)

            # Generate analytics
            analytics = self.llm_manager.get_analytics()

            # Save outputs
            return self._save_session_outputs(
                topic=topic,
                transcript=transcript,
                analytics=analytics,
                experts=experts,
                document_content=document_content
            )

        except Exception as e:
            print(f"❌ Simulation error: {e}")
            traceback.print_exc()
            return {"error": str(e)}

    def _create_moderator(self, topic: str, rounds: List[str] = None) -> AssistantAgent:
        """Create a moderator agent to guide the discussion."""

        # Check for custom rounds from config
        custom_rounds = self.config.get('CUSTOM_ROUNDS', '')
        if custom_rounds:
            rounds = [r.strip() for r in custom_rounds.split(',')]
        elif not rounds:
            # Default rounds based on verbosity
            verbosity = self.config.get('VERBOSITY', 'normal')
            if verbosity == 'concise':
                rounds = [
                    "Quick Assessment",
                    "Key Issues",
                    "Recommendations"
                ]
            elif verbosity == 'verbose':
                rounds = [
                    "Comprehensive Analysis",
                    "Detailed Examination",
                    "Strengths and Opportunities",
                    "Challenges and Risks",
                    "Strategic Recommendations",
                    "Implementation Roadmap",
                    "Long-term Considerations",
                    "Final Synthesis"
                ]
            else:  # normal
                rounds = [
                    "Initial Analysis",
                    "Key Considerations",
                    "Potential Issues",
                    "Recommendations",
                    "Implementation Strategy",
                    "Final Thoughts"
                ]

        rounds_text = "\n".join([f"{i+1}. {round}" for i, round in enumerate(rounds)])

        # Get verbosity for moderator
        verbosity = self.config.get('VERBOSITY', 'normal')
        moderator_style = {
            'concise': "Keep introductions VERY brief (1-2 sentences). Move quickly between rounds.",
            'normal': "Provide clear but concise round introductions. Keep the pace moving.",
            'verbose': "Thoroughly introduce each round and synthesize discussions in detail."
        }

        system_prompt = f"""You are a professional moderator facilitating an expert panel discussion about: {topic}

DISCUSSION ROUNDS ({len(rounds)} total):
{rounds_text}

MODERATION STYLE: {verbosity.upper()}
{moderator_style.get(verbosity, moderator_style['normal'])}

YOUR ROLE:
- Guide the discussion through structured rounds
- Ensure all experts contribute meaningfully
{"- Ask clarifying questions when needed" if verbosity != 'concise' else "- Keep discussion moving quickly"}
- Keep discussions focused and productive
{"- Synthesize key points and identify areas of agreement/disagreement" if verbosity != 'concise' else "- Quick summaries only"}
- Manage time and move discussion forward

GUIDELINES:
- Be neutral and objective
- Encourage specific, actionable insights
{"- Draw out quiet participants" if len(rounds) > 3 else "- Ensure quick responses"}
- Highlight important consensus or disagreements
- Keep your own responses {verbosity}
- Maintain professional tone

CRITICAL: This is a {verbosity} discussion with {len(rounds)} rounds. Keep pace appropriate."""

        # Use same config as experts
        autogen_config = {
            "config_list": [
                {
                    "model": self.config.get('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022'),
                    "api_key": self.config.get('ANTHROPIC_API_KEY'),
                    "api_type": "anthropic"
                }
            ],
            "temperature": float(self.config.get('TEMPERATURE', 0.7)),
            "timeout": 600,
        }

        if self.config.get('PRIMARY_PROVIDER') == 'openai':
            autogen_config["config_list"][0] = {
                "model": self.config.get('OPENAI_MODEL', 'gpt-4o'),
                "api_key": self.config.get('OPENAI_API_KEY'),
                "api_type": "openai"
            }

        return AssistantAgent(
            name="Moderator",
            system_message=system_prompt,
            llm_config=autogen_config,
            max_consecutive_auto_reply=10
        )

    def _extract_transcript(self, chat_result) -> str:
        """Extract transcript from chat result."""
        if hasattr(chat_result, 'chat_history'):
            messages = chat_result.chat_history
        else:
            messages = getattr(chat_result, 'messages', [])

        transcript_lines = []
        transcript_lines.append(f"# Expert Panel Discussion Transcript")
        transcript_lines.append(f"Session: {self.session_id}")
        transcript_lines.append(f"Generated: {datetime.now().isoformat()}")
        transcript_lines.append("")

        for message in messages:
            if isinstance(message, dict):
                name = message.get('name', 'Unknown')
                content = message.get('content', '')
                timestamp = datetime.now().strftime("%H:%M:%S")

                transcript_lines.append(f"## {name} ({timestamp})")
                transcript_lines.append(content)
                transcript_lines.append("")

        return "\n".join(transcript_lines)

    def _save_session_outputs(self, topic: str, transcript: str, analytics: Dict, experts: Dict, document_content: str = None) -> Dict[str, Any]:
        """Save all session outputs and return summary."""

        # Save transcript
        transcript_path = self.output_dir / "transcript.md"
        transcript_path.write_text(transcript)

        # Save analytics
        analytics_path = self.output_dir / "analytics.json"
        self.llm_manager.save_analytics(str(analytics_path))

        # Save metadata
        self.metadata.update({
            'end_time': datetime.now().isoformat(),
            'topic': topic,
            'expert_count': len(experts),
            'expert_names': [agent.name for agent in experts.values()],
            'document_provided': document_content is not None,
            'total_cost': analytics['costs']['total_cost_usd'],
            'total_tokens': analytics['token_usage']['total_tokens']
        })

        metadata_path = self.output_dir / "metadata.json"
        metadata_path.write_text(json.dumps(self.metadata, indent=2))

        # Generate summary
        summary = {
            'session_id': self.session_id,
            'topic': topic,
            'outputs': {
                'transcript': str(transcript_path),
                'analytics': str(analytics_path),
                'metadata': str(metadata_path)
            },
            'analytics_summary': {
                'total_cost': f"${analytics['costs']['total_cost_usd']:.4f}",
                'total_tokens': f"{analytics['token_usage']['total_tokens']:,}",
                'duration': f"{analytics['session_info']['duration_minutes']:.1f} minutes",
                'provider': analytics['session_info']['primary_provider']
            }
        }

        print(f"\n✅ Simulation complete!")
        print(f"💰 Cost: ${analytics['costs']['total_cost_usd']:.4f}")
        print(f"🔢 Tokens: {analytics['token_usage']['total_tokens']:,}")
        print(f"⏱️ Duration: {analytics['session_info']['duration_minutes']:.1f} minutes")
        print(f"📄 Outputs saved to: {self.output_dir}")

        return summary


def load_config() -> Dict[str, Any]:
    """Load configuration from environment and config files."""
    config = {}

    # Load from environment
    env_vars = [
        'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'PRIMARY_PROVIDER',
        'OPENAI_MODEL', 'ANTHROPIC_MODEL', 'TEMPERATURE', 'MAX_TOKENS',
        'MAX_ROUNDS', 'ENABLE_FREE_DISCUSSION', 'SAVE_TRANSCRIPTS',
        'OUTPUT_DIR', 'DEFAULT_EXPERT_COUNT', 'DISCUSSION_STYLE'
    ]

    for var in env_vars:
        if os.getenv(var):
            config[var] = os.getenv(var)

    return config


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Expert Panel Simulator - Multi-Agent Expert Review System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Review a product idea with tech experts
  python expert_panel_simulator.py --topic "AI-powered task manager" --domain technology

  # Review a document with productivity experts
  python expert_panel_simulator.py --document design.md --domain productivity

  # Custom expert panel
  python expert_panel_simulator.py --topic "Startup idea" --config custom_config.yaml

  # Use sample configuration
  python expert_panel_simulator.py --sample task_management_review --document spec.md

Available domains: productivity, technology, business, academic, software_development, product_design
        """
    )

    parser.add_argument('--topic', '-t', help='Topic or question for expert panel to discuss')
    parser.add_argument('--document', '-d', help='Path to document for experts to review')
    parser.add_argument('--domain', choices=get_available_domains(), help='Expert domain to use')
    parser.add_argument('--experts', '-e', type=int, default=5, help='Number of experts (3-7 recommended)')
    parser.add_argument('--config', '-c', help='Path to YAML configuration file')
    parser.add_argument('--sample', choices=list(SAMPLE_CONFIGURATIONS.keys()), help='Use sample configuration')
    parser.add_argument('--provider', choices=['openai', 'anthropic'], help='Override primary LLM provider')
    parser.add_argument('--output', '-o', help='Output directory override')
    parser.add_argument('--rounds', '-r', type=int, help='Number of discussion rounds')

    args = parser.parse_args()

    # Validate required arguments
    if not args.topic and not args.document and not args.sample:
        parser.error("Must provide --topic, --document, or --sample")

    # Load configuration
    config = load_config()

    # Override with command line arguments
    if args.provider:
        config['PRIMARY_PROVIDER'] = args.provider
    if args.output:
        config['OUTPUT_DIR'] = args.output
    if args.rounds:
        config['MAX_ROUNDS'] = str(args.rounds)

    # Handle sample configurations
    if args.sample:
        sample_config = SAMPLE_CONFIGURATIONS[args.sample]
        args.domain = args.domain or sample_config['domain']
        args.topic = args.topic or f"Review of {sample_config['focus']}"

    # Load document if provided
    document_content = None
    if args.document:
        try:
            document_content = Path(args.document).read_text()
            print(f"📄 Loaded document: {args.document}")
        except Exception as e:
            print(f"❌ Error loading document: {e}")
            return 1

    # Determine topic
    topic = args.topic or f"Review of {Path(args.document).name if args.document else 'provided document'}"

    try:
        # Initialize simulator
        simulator = ExpertPanelSimulator(config)

        # Run simulation
        result = simulator.run_simulation(
            topic=topic,
            document_content=document_content,
            domain=args.domain,
            expert_names=None,  # Use all experts from domain
            custom_experts=None
        )

        if 'error' in result:
            print(f"❌ Simulation failed: {result['error']}")
            return 1

        print(f"\n🎉 Session complete: {result['session_id']}")
        return 0

    except KeyboardInterrupt:
        print("\n⏹️ Simulation interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())