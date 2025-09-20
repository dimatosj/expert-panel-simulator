# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Commands

### Setup & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Alternative: Use install script for guided setup
./install.sh

# Create and configure environment file
cp .env.example .env
# Then edit .env to add API keys (ANTHROPIC_API_KEY or OPENAI_API_KEY)
```

### Running Simulations
```bash
# Basic usage with topic and domain
python expert_panel_simulator.py --topic "Your topic" --domain technology

# Review a document
python expert_panel_simulator.py --document file.md --domain productivity

# Use pre-configured sample panels
python expert_panel_simulator.py --sample startup_idea_validation --topic "My SaaS idea"

# Specify number of experts and rounds
python expert_panel_simulator.py --topic "System design" --experts 3 --rounds 4
```

### Testing
```bash
# Run test suite to verify installation
python test_simulator.py
```

## Architecture Overview

### Core Components

**Main Entry Point**: `expert_panel_simulator.py`
- Orchestrates the simulation using AutoGen framework
- Creates expert agents dynamically based on configuration
- Manages discussion rounds and output generation
- Key class: `ExpertPanelSimulator` handles the entire simulation lifecycle

**LLM Provider Abstraction**: `utils/llm_provider.py`
- Provides unified interface for OpenAI and Anthropic APIs
- Handles token counting, cost tracking, and retry logic
- Key classes: `LLMManager` (orchestration), `OpenAIProvider`, `AnthropicProvider`
- Automatically falls back between providers if one fails

**Expert Configuration**: `config/expert_templates.py`
- Defines expert personas across domains (productivity, technology, business, academic)
- Each expert has: name, expertise, perspective, background
- Supports custom expert creation via `create_custom_expert()`
- Pre-built sample configurations in `SAMPLE_CONFIGURATIONS` dict

### Key Design Patterns

1. **Multi-Agent Conversation**: Uses AutoGen's GroupChat for managing expert discussions with automatic turn-taking and response coordination

2. **Provider Abstraction**: LLM operations abstracted to support multiple providers seamlessly, with automatic fallback and cost tracking

3. **Template-Based Experts**: Experts defined as templates that are instantiated with specific prompts based on the discussion topic

4. **Session Management**: Each simulation creates a timestamped session with outputs saved to `outputs/session_YYYYMMDD_HHMMSS/`

## Environment Configuration

Key `.env` variables:
- `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`: Required for LLM access
- `PRIMARY_PROVIDER`: Choose default provider (anthropic/openai)
- `MAX_ROUNDS`: Number of discussion rounds (default: 8)
- `DEFAULT_EXPERT_COUNT`: Number of experts to create (default: 5)
- `TEMPERATURE`: LLM creativity (0.0-1.0, default: 0.7)
- `MAX_TOKENS`: Response length limit (default: 4000)

## Available Expert Domains

- **productivity**: GTD, PARA, Deep Work, Pomodoro, ADHD specialists
- **technology**: UX, Software Architecture, DevOps, Security, Frontend experts
- **business**: Product Management, Startup Advisory, Growth, Finance experts
- **academic**: Psychology, Education, Data Science researchers

## Output Structure

Each simulation generates:
- `transcript.md`: Full discussion transcript with timestamps
- `analytics.json`: Token usage, costs, and performance metrics
- `metadata.json`: Session configuration and summary

## Cost Considerations

Typical session costs (5 experts, 6 rounds):
- Claude-3.5-Sonnet: $0.10-$0.25
- GPT-4o: $0.15-$0.35
- Claude-3-Haiku: $0.03-$0.08

Use cheaper models by setting `ANTHROPIC_MODEL=claude-3-haiku-20240307` or `OPENAI_MODEL=gpt-3.5-turbo` in `.env`