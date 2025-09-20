"""LLM Provider abstraction layer supporting OpenAI and Anthropic."""

import os
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


@dataclass
class TokenUsage:
    """Token usage tracking."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    def __add__(self, other):
        return TokenUsage(
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            total_tokens=self.total_tokens + other.total_tokens
        )


@dataclass
class LLMResponse:
    """Standardized LLM response."""
    content: str
    model: str
    tokens: TokenUsage
    cost: float
    latency: float
    provider: str


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """Generate response from messages."""
        pass

    @abstractmethod
    def estimate_cost(self, tokens: TokenUsage) -> float:
        """Estimate cost for token usage."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""

    def __init__(self, api_key: str, model: str = "gpt-4o", **kwargs):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not installed. Run: pip install openai")

        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.temperature = kwargs.get('temperature', 0.7)
        self.max_tokens = kwargs.get('max_tokens', 4000)

        # Pricing per 1K tokens (as of 2024)
        self.pricing = {
            'gpt-4o': {'input': 0.0025, 'output': 0.010},
            'gpt-4o-2024-08-06': {'input': 0.0025, 'output': 0.010},
            'gpt-4-turbo': {'input': 0.010, 'output': 0.030},
            'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
        }

    def generate(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """Generate response using OpenAI."""
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get('temperature', self.temperature),
                max_tokens=kwargs.get('max_tokens', self.max_tokens)
            )

            # Extract usage information
            usage = response.usage
            tokens = TokenUsage(
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens
            )

            cost = self.estimate_cost(tokens)
            latency = time.time() - start_time

            return LLMResponse(
                content=response.choices[0].message.content,
                model=self.model,
                tokens=tokens,
                cost=cost,
                latency=latency,
                provider="openai"
            )

        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")

    def estimate_cost(self, tokens: TokenUsage) -> float:
        """Estimate cost based on token usage."""
        pricing = self.pricing.get(self.model, self.pricing['gpt-4o'])

        input_cost = (tokens.prompt_tokens / 1000) * pricing['input']
        output_cost = (tokens.completion_tokens / 1000) * pricing['output']

        return input_cost + output_cost

    def count_tokens(self, text: str) -> int:
        """Count tokens in text (approximate if tiktoken not available)."""
        if TIKTOKEN_AVAILABLE:
            try:
                encoding = tiktoken.encoding_for_model(self.model)
                return len(encoding.encode(text))
            except:
                pass

        # Fallback: rough estimate
        return len(text.split()) * 1.3  # ~1.3 tokens per word


class AnthropicProvider(LLMProvider):
    """Anthropic API provider."""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", **kwargs):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic library not installed. Run: pip install anthropic")

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.temperature = kwargs.get('temperature', 0.7)
        self.max_tokens = kwargs.get('max_tokens', 4000)

        # Pricing per 1K tokens (as of 2024)
        self.pricing = {
            'claude-3-5-sonnet-20241022': {'input': 0.003, 'output': 0.015},
            'claude-3-opus-20240229': {'input': 0.015, 'output': 0.075},
            'claude-3-haiku-20240307': {'input': 0.00025, 'output': 0.00125},
        }

    def generate(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """Generate response using Anthropic."""
        start_time = time.time()

        # Extract system message if present
        system_message = None
        filtered_messages = []

        for msg in messages:
            if msg['role'] == 'system':
                system_message = msg['content']
            else:
                filtered_messages.append(msg)

        try:
            api_params = {
                'model': self.model,
                'messages': filtered_messages,
                'temperature': kwargs.get('temperature', self.temperature),
                'max_tokens': kwargs.get('max_tokens', self.max_tokens)
            }

            if system_message:
                api_params['system'] = system_message

            response = self.client.messages.create(**api_params)

            # Estimate token usage (Anthropic doesn't always provide this)
            prompt_text = system_message or ""
            for msg in filtered_messages:
                prompt_text += msg['content']

            completion_text = response.content[0].text

            tokens = TokenUsage(
                prompt_tokens=self.count_tokens(prompt_text),
                completion_tokens=self.count_tokens(completion_text),
                total_tokens=self.count_tokens(prompt_text + completion_text)
            )

            cost = self.estimate_cost(tokens)
            latency = time.time() - start_time

            return LLMResponse(
                content=completion_text,
                model=self.model,
                tokens=tokens,
                cost=cost,
                latency=latency,
                provider="anthropic"
            )

        except Exception as e:
            raise Exception(f"Anthropic API error: {e}")

    def estimate_cost(self, tokens: TokenUsage) -> float:
        """Estimate cost based on token usage."""
        pricing = self.pricing.get(self.model, self.pricing['claude-3-5-sonnet-20241022'])

        input_cost = (tokens.prompt_tokens / 1000) * pricing['input']
        output_cost = (tokens.completion_tokens / 1000) * pricing['output']

        return input_cost + output_cost

    def count_tokens(self, text: str) -> int:
        """Count tokens in text (approximate)."""
        # Anthropic uses similar tokenization to GPT models
        return len(text.split()) * 1.3  # Rough estimate


class LLMManager:
    """Manages multiple LLM providers with analytics."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.providers = {}
        self.total_usage = TokenUsage()
        self.total_cost = 0.0
        self.call_count = 0
        self.session_start = time.time()

        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize available providers based on config."""
        # OpenAI
        if self.config.get('OPENAI_API_KEY') and OPENAI_AVAILABLE:
            try:
                self.providers['openai'] = OpenAIProvider(
                    api_key=self.config['OPENAI_API_KEY'],
                    model=self.config.get('OPENAI_MODEL', 'gpt-4o'),
                    temperature=float(self.config.get('TEMPERATURE', 0.7)),
                    max_tokens=int(self.config.get('MAX_TOKENS', 4000))
                )
                print("✓ OpenAI provider initialized")
            except Exception as e:
                print(f"⚠ OpenAI provider failed: {e}")

        # Anthropic
        if self.config.get('ANTHROPIC_API_KEY') and ANTHROPIC_AVAILABLE:
            try:
                self.providers['anthropic'] = AnthropicProvider(
                    api_key=self.config['ANTHROPIC_API_KEY'],
                    model=self.config.get('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022'),
                    temperature=float(self.config.get('TEMPERATURE', 0.7)),
                    max_tokens=int(self.config.get('MAX_TOKENS', 4000))
                )
                print("✓ Anthropic provider initialized")
            except Exception as e:
                print(f"⚠ Anthropic provider failed: {e}")

        if not self.providers:
            raise Exception("No LLM providers available. Check your API keys and installations.")

    def generate(self, messages: List[Dict[str, str]], provider: Optional[str] = None, **kwargs) -> LLMResponse:
        """Generate response using specified or primary provider."""
        # Choose provider
        if provider is None:
            provider = self.config.get('PRIMARY_PROVIDER', 'anthropic')

        if provider not in self.providers:
            available = list(self.providers.keys())
            if available:
                provider = available[0]
                print(f"⚠ Requested provider '{provider}' not available, using '{provider}'")
            else:
                raise Exception("No LLM providers available")

        # Generate response
        response = self.providers[provider].generate(messages, **kwargs)

        # Track usage
        self.total_usage += response.tokens
        self.total_cost += response.cost
        self.call_count += 1

        return response

    def get_analytics(self) -> Dict[str, Any]:
        """Get session analytics."""
        session_duration = time.time() - self.session_start

        analytics = {
            'session_info': {
                'duration_minutes': round(session_duration / 60, 2),
                'total_calls': self.call_count,
                'providers_used': list(self.providers.keys()),
                'primary_provider': self.config.get('PRIMARY_PROVIDER', 'unknown')
            },
            'token_usage': {
                'prompt_tokens': self.total_usage.prompt_tokens,
                'completion_tokens': self.total_usage.completion_tokens,
                'total_tokens': self.total_usage.total_tokens
            },
            'costs': {
                'total_cost_usd': round(self.total_cost, 4),
                'average_cost_per_call': round(self.total_cost / max(self.call_count, 1), 4),
                'estimated_cost_per_1k_tokens': round(self.total_cost / max(self.total_usage.total_tokens / 1000, 1), 4)
            },
            'performance': {
                'calls_per_minute': round(self.call_count / max(session_duration / 60, 1), 2),
                'tokens_per_minute': round(self.total_usage.total_tokens / max(session_duration / 60, 1), 0)
            }
        }

        return analytics

    def save_analytics(self, output_path: str):
        """Save analytics to JSON file."""
        analytics = self.get_analytics()

        with open(output_path, 'w') as f:
            json.dump(analytics, f, indent=2)

        return analytics