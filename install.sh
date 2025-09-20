#!/bin/bash

# Expert Panel Simulator Installation Script

echo "=========================================="
echo "Expert Panel Simulator - Installation"
echo "=========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d ' ' -f2 | cut -d '.' -f1,2)
required_version="3.8"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo "❌ Python 3.8+ required. You have Python $python_version"
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

echo "✓ Python $python_version found"

# Create virtual environment (optional but recommended)
read -p "Create virtual environment? (y/n): " create_venv
if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Setup environment file
if [ ! -f ".env" ]; then
    echo ""
    echo "Setting up environment configuration..."
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your API keys:"
    echo "   - OpenAI API key from: https://platform.openai.com/api-keys"
    echo "   - Anthropic API key from: https://console.anthropic.com/"
    echo ""
else
    echo "✓ .env file already exists"
fi

# Test installation
echo "Testing installation..."
python3 -c "
import sys
try:
    import autogen
    import dotenv
    from config.expert_templates import get_available_domains
    print('✓ All modules imported successfully')
    print(f'✓ Available domains: {get_available_domains()}')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your API keys"
    echo "2. Run your first simulation:"
    echo "   python expert_panel_simulator.py --topic 'My idea' --domain technology"
    echo ""
    echo "For help: python expert_panel_simulator.py --help"
    echo "Documentation: README.md"
else
    echo "❌ Installation test failed"
    exit 1
fi