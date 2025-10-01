# Quick Start Guide

Get up and running with Expert Panel Simulator in 5 minutes!

## 🚀 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or use the install script (recommended)
./install.sh
```

## 🔑 2. API Setup

### Option A: Anthropic (Recommended)
1. Get key from: https://console.anthropic.com/
2. Add to `.env`:
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
PRIMARY_PROVIDER=anthropic
```

### Option B: OpenAI
1. Get key from: https://platform.openai.com/api-keys
2. Add to `.env`:
```env
OPENAI_API_KEY=sk-...
PRIMARY_PROVIDER=openai
```

## 🎯 3. First Simulation

```bash
# Review a product idea
python expert_panel_simulator.py --topic "AI-powered task manager" --domain technology
```

**What happens:**
- Creates 5 tech experts (UX Designer, Software Architect, DevOps Engineer, Security Expert, Frontend Expert)
- They discuss your idea for ~6 rounds
- Generates transcript, analytics, and cost breakdown
- Saves everything to `outputs/session_YYYYMMDD_HHMMSS/`

## 📊 Example Output

```
🚀 Expert Panel Simulator initialized
📁 Session: 20241120_143022
💾 Output: outputs/session_20241120_143022
👥 Created 5 experts: UX Designer, Software Architect, DevOps Engineer, Security Specialist, Frontend Engineer
🗣️ Starting expert discussion...

✅ Simulation complete!
💰 Cost: $0.1247
🔢 Tokens: 23,760
⏱️ Duration: 8.5 minutes
📄 Outputs saved to: outputs/session_20241120_143022
```

## 🎨 Try Different Domains

```bash
# Business validation
python expert_panel_simulator.py --topic "SaaS subscription model" --domain business

# Productivity system review
python expert_panel_simulator.py --document task_system.md --domain productivity

# Academic research discussion
python expert_panel_simulator.py --topic "Machine learning ethics" --domain academic
```

## 📋 Use Sample Configurations

```bash
# Startup idea validation with pre-configured experts
python expert_panel_simulator.py --sample startup_idea_validation --topic "My app idea"

# App architecture review
python expert_panel_simulator.py --sample app_architecture_review --document spec.md

# Task management system review
python expert_panel_simulator.py --sample task_management_review --document design.md
```

## 💡 Pro Tips

1. **Start small**: Use 3-5 experts for focused discussions
2. **Review documents**: Add `--document file.md` for detailed feedback
3. **Check costs**: Start with cheaper models (Claude-3-Haiku, GPT-3.5-Turbo)
4. **Save configs**: Create YAML files for repeated expert panels
5. **Read transcripts**: The generated markdown files contain gold insights

## 🔧 Common Issues

**"No LLM providers available"**
- Check your API key in `.env`
- Verify the key has credits/quota

**High costs**
- Try: `ANTHROPIC_MODEL=claude-3-haiku-20240307` (much cheaper)
- Reduce experts: `--experts 3`
- Shorter discussions: `--rounds 4`

## 📖 Next Steps

- Read the full [README.md](README.md) for advanced options
- Explore [expert templates](config/expert_templates.py) for customization
- Check [sample configurations](config/expert_templates.py#L387) for ideas

---

**Need help?** Run the test suite: `python test_simulator.py`