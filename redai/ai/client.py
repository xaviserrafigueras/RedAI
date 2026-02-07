"""
OpenAI client configuration and basic AI functions.
"""

from typing import Optional
from openai import OpenAI

from redai.config import settings


# Global client instance
_client: Optional[OpenAI] = None


def get_client() -> Optional[OpenAI]:
    """Get or create the OpenAI client instance."""
    global _client
    
    if _client is None and settings.openai_api_key:
        _client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.ai_base_url
        )
    
    return _client


def get_model_name() -> str:
    """Get the configured AI model name."""
    return settings.ai_model


def ask_ai_logic(prompt: str) -> str:
    """Simple AI query for basic prompts."""
    client = get_client()
    
    if not client:
        return "Error: No API Key configured."
    
    try:
        response = client.chat.completions.create(
            model=get_model_name(),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error IA: {e}"
