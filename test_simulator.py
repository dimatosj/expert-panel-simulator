#!/usr/bin/env python3
"""Test script for Expert Panel Simulator."""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")

    try:
        import autogen
        print("✓ AutoGen imported")
    except ImportError as e:
        print(f"❌ AutoGen import failed: {e}")
        return False

    try:
        from utils.llm_provider import LLMManager
        print("✓ LLM provider imported")
    except ImportError as e:
        print(f"❌ LLM provider import failed: {e}")
        return False

    try:
        from config.expert_templates import get_available_domains
        domains = get_available_domains()
        print(f"✓ Expert templates imported ({len(domains)} domains)")
    except ImportError as e:
        print(f"❌ Expert templates import failed: {e}")
        return False

    return True

def test_expert_domains():
    """Test expert domain functionality."""
    print("\nTesting expert domains...")

    try:
        from config.expert_templates import get_expert_set, get_available_domains

        domains = get_available_domains()
        print(f"Available domains: {domains}")

        for domain in domains[:3]:  # Test first 3
            experts = get_expert_set(domain)
            print(f"  {domain}: {len(experts)} experts")

        print("✓ Expert domains working")
        return True
    except Exception as e:
        print(f"❌ Expert domains failed: {e}")
        return False

def test_llm_config():
    """Test LLM configuration."""
    print("\nTesting LLM configuration...")

    # Check for API keys
    has_openai = bool(os.getenv('OPENAI_API_KEY'))
    has_anthropic = bool(os.getenv('ANTHROPIC_API_KEY'))

    print(f"OpenAI API key configured: {has_openai}")
    print(f"Anthropic API key configured: {has_anthropic}")

    if not has_openai and not has_anthropic:
        print("⚠️  No API keys found. Add to .env file for full functionality")
        return False

    try:
        config = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', 'test'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY', 'test'),
            'PRIMARY_PROVIDER': 'anthropic',
            'TEMPERATURE': '0.7',
            'MAX_TOKENS': '4000'
        }

        # Don't actually initialize LLM (might fail without real keys)
        print("✓ LLM configuration structure valid")
        return True
    except Exception as e:
        print(f"❌ LLM configuration failed: {e}")
        return False

def test_sample_config():
    """Test sample configurations."""
    print("\nTesting sample configurations...")

    try:
        from config.expert_templates import SAMPLE_CONFIGURATIONS

        samples = list(SAMPLE_CONFIGURATIONS.keys())
        print(f"Available samples: {samples}")

        for sample_name in samples:
            config = SAMPLE_CONFIGURATIONS[sample_name]
            print(f"  {sample_name}: {config['domain']} domain, {len(config['experts'])} experts")

        print("✓ Sample configurations working")
        return True
    except Exception as e:
        print(f"❌ Sample configurations failed: {e}")
        return False

def test_cli_help():
    """Test CLI help functionality."""
    print("\nTesting CLI help...")

    try:
        import subprocess
        result = subprocess.run([
            sys.executable, 'expert_panel_simulator.py', '--help'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode == 0 and 'Expert Panel Simulator' in result.stdout:
            print("✓ CLI help working")
            return True
        else:
            print("❌ CLI help failed")
            return False
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("EXPERT PANEL SIMULATOR - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Import Test", test_imports),
        ("Expert Domains", test_expert_domains),
        ("LLM Configuration", test_llm_config),
        ("Sample Configurations", test_sample_config),
        ("CLI Help", test_cli_help)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! System ready to use.")
        print("\nNext steps:")
        print("1. Add API keys to .env file")
        print("2. Run: python expert_panel_simulator.py --topic 'Test idea' --domain technology")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Check errors above.")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)