# Expert Panel Simulator

> **Multi-Agent Expert Review System** - Create virtual expert panels to review any topic, document, or idea using AI-powered domain experts.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 What is this?

The Expert Panel Simulator creates virtual panels of domain experts who discuss and review your ideas, documents, or concepts. Think of it as having instant access to a roundtable of industry experts who can provide diverse perspectives and actionable feedback.

**Perfect for:**
- 📋 Product design reviews
- 🏗️ Architecture assessments
- 💼 Business idea validation
- 📚 Academic research discussions
- 🎯 Strategy planning sessions
- 🔍 System design reviews

## ✨ Key Features

- **🧠 Multiple AI Providers**: Choose between OpenAI GPT-4 or Anthropic Claude
- **👥 Expert Templates**: Pre-built experts across productivity, tech, business, and academic domains
- **📊 Comprehensive Analytics**: Track token usage, costs, and performance metrics
- **💰 Cost Transparency**: Real-time cost tracking with detailed breakdowns
- **📄 Rich Outputs**: Markdown transcripts, JSON analytics, and session metadata
- **🎨 Customizable**: Create your own expert personas and discussion formats
- **⚡ Easy Setup**: Works out of the box with minimal configuration

## 🏃‍♂️ Quick Start

### 1. Installation

```bash
# Clone or download this directory
git clone <your-repo-url>
cd expert-panel-simulator

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Get OpenAI key from: https://platform.openai.com/api-keys
# Get Anthropic key from: https://console.anthropic.com/
```

**Minimum .env setup:**
```env
# Choose one or both providers
ANTHROPIC_API_KEY=your_anthropic_key_here
# OPENAI_API_KEY=your_openai_key_here

# Set primary provider
PRIMARY_PROVIDER=anthropic
```

### 3. Run Your First Simulation

```bash
# Review a product idea with tech experts
python expert_panel_simulator.py --topic "AI-powered task manager" --domain technology

# Review a document with business experts
python expert_panel_simulator.py --document my_business_plan.md --domain business

# Use a sample configuration
python expert_panel_simulator.py --sample startup_idea_validation --topic "My SaaS idea"
```

## 📖 Usage Examples

### Basic Usage

```bash
# Product review with 5 tech experts
python expert_panel_simulator.py \
  --topic "Mobile app for habit tracking" \
  --domain technology \
  --experts 5

# Document review with productivity experts
python expert_panel_simulator.py \
  --document design_spec.md \
  --domain productivity

# Business strategy with custom rounds
python expert_panel_simulator.py \
  --topic "Expansion strategy" \
  --domain business \
  --rounds 6
```

### Advanced Options

```bash
# Force specific provider
python expert_panel_simulator.py \
  --topic "System architecture" \
  --domain technology \
  --provider openai

# Custom output directory
python expert_panel_simulator.py \
  --topic "Research proposal" \
  --domain academic \
  --output my_reviews/

# Use sample configuration
python expert_panel_simulator.py \
  --sample app_architecture_review \
  --document technical_spec.md
```

## 🎯 Available Expert Domains

### **Productivity** (`--domain productivity`)
- **GTD Specialist** - Task capture and context-based action
- **Digital Organization Expert** - PARA method and progressive summarization
- **Focus & Attention Expert** - Deep work and attention management
- **Time-Boxing Coach** - Pomodoro and interval-based productivity
- **Executive Function Specialist** - ADHD and executive function support

### **Technology** (`--domain technology`)
- **UX Designer** - User experience and interface design
- **Software Architect** - System architecture and scalability
- **DevOps Engineer** - Infrastructure and operations
- **Security Specialist** - Cybersecurity and privacy
- **Frontend Engineer** - Frontend development and performance

### **Business** (`--domain business`)
- **Product Strategist** - Product planning and market fit
- **Startup Mentor** - Entrepreneurship and lean validation
- **Growth Specialist** - Marketing funnels and user acquisition
- **Finance Advisor** - Business finance and sustainability

### **Academic** (`--domain academic`)
- **Cognitive Psychology Researcher** - Human cognition and behavior
- **Learning Scientist** - Education and knowledge transfer
- **Data Science Researcher** - Machine learning and statistical modeling

## 📊 Sample Configurations

Use `--sample <name>` for pre-configured expert panels:

### `task_management_review`
**Domain:** Productivity
**Experts:** GTD, PARA, ADHD Specialist, Deep Work
**Focus:** Task management system design

### `app_architecture_review`
**Domain:** Technology
**Experts:** Software Architect, UX Designer, DevOps, Security
**Focus:** Application architecture and design

### `startup_idea_validation`
**Domain:** Business
**Experts:** Product Manager, Startup Advisor, Growth Expert, Finance
**Focus:** Startup idea and business model validation

## 💰 Cost & Analytics

The simulator provides detailed analytics after each session:

```json
{
  "session_info": {
    "duration_minutes": 8.5,
    "total_calls": 12,
    "primary_provider": "anthropic"
  },
  "token_usage": {
    "prompt_tokens": 15420,
    "completion_tokens": 8340,
    "total_tokens": 23760
  },
  "costs": {
    "total_cost_usd": 0.1247,
    "average_cost_per_call": 0.0104,
    "estimated_cost_per_1k_tokens": 0.0052
  }
}
```

**Typical Costs (5 experts, 6 rounds):**
- **Anthropic Claude-3.5-Sonnet**: $0.10 - $0.25
- **OpenAI GPT-4o**: $0.15 - $0.35
- **Anthropic Claude-3-Haiku**: $0.03 - $0.08

## 📁 Output Structure

Each simulation creates a timestamped session directory:

```
outputs/
└── session_20241120_143022/
    ├── transcript.md       # Full discussion transcript
    ├── analytics.json      # Token usage and cost analytics
    └── metadata.json       # Session configuration and summary
```

### Sample Transcript Format

```markdown
# Expert Panel Discussion Transcript
Session: 20241120_143022
Generated: 2024-11-20T14:32:45

## UX Designer (14:32:45)
As a UX designer, I see significant potential in this concept. The key challenge will be balancing feature richness with interface simplicity...

## Software Architect (14:33:12)
From an architecture perspective, we need to consider scalability early. I'd recommend starting with a microservices approach...
```

## 🛠️ Configuration

### Environment Variables

Create a `.env` file with these options:

```env
# API Keys (get from provider websites)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
PRIMARY_PROVIDER=anthropic

# Model Selection
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
OPENAI_MODEL=gpt-4o-2024-08-06

# Model Parameters
TEMPERATURE=0.7          # Creativity (0.0-1.0)
MAX_TOKENS=4000         # Response length limit

# Simulation Settings
MAX_ROUNDS=8            # Discussion rounds
DEFAULT_EXPERT_COUNT=5  # Number of experts
DISCUSSION_STYLE=formal # formal, casual, academic

# Output Options
OUTPUT_DIR=outputs      # Where to save results
SAVE_TRANSCRIPTS=true   # Save full transcripts
ENABLE_TOKEN_COUNTING=true
ENABLE_COST_TRACKING=true
```

### Command Line Options

```bash
Usage: expert_panel_simulator.py [OPTIONS]

Options:
  -t, --topic TEXT        Topic for expert panel discussion
  -d, --document PATH     Document file to review
  --domain CHOICE         Expert domain (productivity/technology/business/academic)
  -e, --experts INT       Number of experts (3-7 recommended)
  -c, --config PATH       YAML configuration file
  --sample CHOICE         Use sample configuration
  --provider CHOICE       Override primary LLM provider (openai/anthropic)
  -o, --output PATH       Output directory override
  -r, --rounds INT        Number of discussion rounds
  --help                  Show this message and exit
```

## 🎨 Customization

### Creating Custom Experts

You can create custom expert personas by extending the expert templates:

```python
from config.expert_templates import create_custom_expert

custom_expert = create_custom_expert(
    name="Dr. Jane Smith (AI Ethics Expert)",
    expertise="AI Ethics and Responsible AI Development",
    perspective="Focuses on ethical implications and societal impact",
    background="PhD in Philosophy, 10+ years in AI ethics research"
)
```

### Custom Configuration Files

Create YAML configs for repeated use:

```yaml
# my_config.yaml
experts:
  - name: "Custom Expert 1"
    expertise: "Domain Expertise"
    perspective: "Unique viewpoint"
    background: "Professional background"

discussion_rounds:
  - "Round 1: Analysis"
  - "Round 2: Recommendations"
  - "Round 3: Implementation"

settings:
  max_rounds: 6
  temperature: 0.8
```

## 🔧 Troubleshooting

### Common Issues

**❌ "No LLM providers available"**
- Check your API keys in `.env` file
- Verify keys are valid and have credits
- Install required packages: `pip install openai anthropic`

**❌ "Module not found" errors**
- Install dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

**❌ High costs**
- Use cheaper models: `claude-3-haiku` or `gpt-3.5-turbo`
- Reduce expert count or rounds
- Set lower `MAX_TOKENS` limit

**❌ Rate limiting**
- The system includes retry logic with exponential backoff
- Consider switching providers or reducing concurrency
- Anthropic typically has higher rate limits than OpenAI

### API Key Setup

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

**Anthropic:**
1. Go to https://console.anthropic.com/
2. Create API key
3. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- **New Expert Domains**: Add experts for healthcare, finance, education, etc.
- **Enhanced Analytics**: Better visualization of expert consensus/disagreement
- **Integration Features**: Export to other tools, API endpoints
- **UI Development**: Web interface for easier use

## 📜 License

MIT License - feel free to use this for personal or commercial projects.

## 🙏 Acknowledgments

Built on:
- [AutoGen](https://github.com/microsoft/autogen) - Multi-agent conversation framework
- [OpenAI API](https://openai.com/api/) - GPT-4 and other models
- [Anthropic API](https://www.anthropic.com/) - Claude models

---

**💡 Pro Tips:**
- Start with 3-5 experts for focused discussions
- Use document review for detailed feedback
- Try different domains for diverse perspectives
- Check analytics to optimize costs
- Save successful configurations for reuse

**Questions or issues?** Open an issue on GitHub or check our troubleshooting guide!