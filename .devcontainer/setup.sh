#!/bin/bash
set -e

echo "🚀 Setting up Weaviate + Pydantic AI Workshop environment..."

# Check if uv is already installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "✅ uv already installed"
fi

# Use uv for faster dependency management with caching
echo "📦 Installing Python dependencies with uv..."
uv pip install --system -r requirements.txt

# Run a quick test to verify setup
echo "🧪 Running setup verification..."
python -c "import pydantic_ai; import weaviate; print('✅ All imports successful!')" || echo "⚠️  Some imports failed - check dependencies"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Quick start:"
echo "   1. Add your API keys to .env file"
echo "   2. Run: python step1_llm_call.py"
echo ""
echo "📚 See README.md for full workshop instructions"
