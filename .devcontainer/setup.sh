#!/bin/bash
set -e

echo "🚀 Setting up Weaviate + Pydantic AI Workshop environment..."

# Install uv for faster dependency management
echo "📦 Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Install dependencies using uv
echo "📦 Installing Python dependencies..."
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
