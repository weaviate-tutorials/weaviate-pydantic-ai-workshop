#!/usr/bin/env python3
"""
Setup verification script for the Weaviate + Pydantic AI Workshop.
Run this before the workshop to ensure everything is configured correctly.
"""

import os
import sys
from dotenv import load_dotenv


def check_imports():
    """Verify all required packages are installed."""
    print("🔍 Checking Python packages...")

    packages = {
        "pydantic_ai": "Pydantic AI",
        "weaviate": "Weaviate Client",
        "dotenv": "python-dotenv",
    }

    all_good = True
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NOT INSTALLED")
            all_good = False

    return all_good


def check_env_file():
    """Check if .env file exists and has required keys."""
    print("\n🔍 Checking .env file...")

    if not os.path.exists(".env"):
        print("  ❌ .env file not found")
        print("     Run: cp .env.example .env")
        return False

    print("  ✅ .env file exists")
    return True


def check_api_keys():
    """Verify API keys are configured."""
    print("\n🔍 Checking API keys...")

    load_dotenv()

    required_keys = {
        "ANTHROPIC_API_KEY": "Anthropic (required for all steps)",
        "WEAVIATE_URL": "Weaviate URL (required for steps 4-6)",
        "WEAVIATE_RO_KEY": "Weaviate API Key (required for steps 4-6)",
        "COHERE_API_KEY": "Cohere (required for steps 4-6)",
    }

    all_configured = True
    for key, description in required_keys.items():
        value = os.getenv(key)
        if not value or value.startswith("your_"):
            print(f"  ⚠️  {description}")
            print(f"      {key} not configured")
            all_configured = False
        else:
            print(f"  ✅ {description}")

    return all_configured


def test_basic_llm():
    """Test basic LLM connectivity (optional - requires API key)."""
    print("\n🔍 Testing Anthropic API connection...")

    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key.startswith("your_"):
        print("  ⏭️  Skipping (API key not configured)")
        return True

    try:
        from pydantic_ai import ModelRequest
        from pydantic_ai.direct import model_request_sync

        response = model_request_sync(
            "anthropic:claude-3-5-haiku-latest",
            [ModelRequest.user_text_prompt("Say 'test successful' and nothing else")],
        )

        print("  ✅ Anthropic API working")
        return True
    except Exception as e:
        print(f"  ❌ Anthropic API test failed: {str(e)[:100]}")
        return False


def main():
    print("=" * 80)
    print("WEAVIATE + PYDANTIC AI WORKSHOP - SETUP VERIFICATION")
    print("=" * 80)
    print()

    checks = [check_imports(), check_env_file(), check_api_keys(), test_basic_llm()]

    print("\n" + "=" * 80)
    if all(checks):
        print("✅ All checks passed! You're ready for the workshop!")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n📚 For help, see README.md or ask in the workshop chat")
        sys.exit(1)
    print("=" * 80)


if __name__ == "__main__":
    main()
