"""
OpenAI client configuration with retry and logging.
"""

from typing import Optional, List, Dict
from openai import OpenAI

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)

from redai.config import settings
from redai.core.logger import get_logger


logger = get_logger("ai.client")

# Global client instance
_client: Optional[OpenAI] = None


def get_client() -> Optional[OpenAI]:
    """Get or create the OpenAI client instance (works with any OpenAI-compatible API)."""
    global _client
    
    if _client is None:
        provider = settings.ai.provider
        api_key = settings.ai.api_key or "ollama"  # Ollama doesn't need real key
        base_url = settings.ai.base_url
        
        # For Ollama, we don't need a real API key
        if provider == "ollama":
            api_key = "ollama"
        
        if not api_key or api_key == "":
            logger.warning(f"No API key configured for provider: {provider}")
            return None
        
        _client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        logger.info(f"AI client initialized: provider={provider}, model={settings.ai.model}, base_url={base_url}")
    
    return _client


def get_model_name() -> str:
    """Get the configured AI model name."""
    return settings.ai.model


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((Exception,)),
    before_sleep=before_sleep_log(logger, log_level=20)  # INFO level
)
def chat_completion(
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 4000
) -> str:
    """
    Make a chat completion request with automatic retry.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        temperature: Creativity level (0-1)
        max_tokens: Maximum response length
    
    Returns:
        AI response text
    
    Raises:
        Exception if all retries fail
    """
    client = get_client()
    
    if not client:
        logger.error("No API client available - check your API key")
        raise ValueError("No API Key configured")
    
    logger.debug(f"Sending request with {len(messages)} messages")
    
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    result = response.choices[0].message.content
    logger.debug(f"Received response: {len(result)} chars")
    
    return result


def ask_ai_logic(prompt: str) -> str:
    """Simple AI query for basic prompts (with retry)."""
    try:
        return chat_completion([{"role": "user", "content": prompt}])
    except Exception as e:
        logger.error(f"AI request failed after retries: {e}")
        return f"Error IA: {e}"
