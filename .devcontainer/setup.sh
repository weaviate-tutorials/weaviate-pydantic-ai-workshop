#!/bin/bash
set -e

echo "🚀 Setting up Weaviate + Pydantic AI Workshop environment..."

# Ensure we're in the right directory
cd "$(dirname "$0")/.."

# Check if uv is already installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add to PATH for this session
    export PATH="$HOME/.cargo/bin:$PATH"
    # Ensure uv is available for subsequent commands
    if ! command -v uv &> /dev/null; then
        echo "❌ Failed to install uv"
        exit 1
    fi
else
    echo "✅ uv already installed"
fi

# Use uv for faster dependency management with caching
echo "📦 Installing Python dependencies with uv..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found in current directory"
    exit 1
fi

uv sync

source .venv/bin/activate

# Run a quick test to verify setup
echo "🧪 Running setup verification..."
python -c "import pydantic_ai; import weaviate; print('✅ All imports successful!')" || {
    echo "⚠️  Some imports failed - this might be expected if API keys aren't configured yet"
    echo "   You can continue with the workshop setup"
}

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Quick start:"
echo "   1. Add your API keys to .env file"
echo "   2. Run: python step1_llm_call.py"
echo ""
echo "📚 See README.md for full workshop instructions"
