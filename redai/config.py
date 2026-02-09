"""
Centralized Configuration for RedAI
Loads configuration from YAML file, environment variables, and defaults.
Priority: Environment Variables > YAML Config > Defaults

Uses Pydantic for validation - invalid config.yaml will show clear error messages.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from pydantic import ValidationError

from redai.core.config_models import AppConfig

# Load .env file first
load_dotenv()


def load_yaml_config() -> Dict[str, Any]:
    """Load configuration from YAML file if it exists."""
    try:
        import yaml
    except ImportError:
        return {}
    
    # Look for config files in order of priority
    config_paths = [
        Path("config.yaml"),
        Path("config.yml"),
        Path("config.local.yaml"),
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
                    return config
            except Exception:
                pass
    
    return {}


# Load YAML config once at module load
_yaml_config = load_yaml_config()


def get_config_value(yaml_path: str, env_var: str = None, default: Any = None) -> Any:
    """
    Get a configuration value with priority: ENV > YAML > default.
    
    Args:
        yaml_path: Dot-separated path in YAML (e.g., "ai.model")
        env_var: Environment variable name to check
        default: Default value if not found
    
    Returns:
        Configuration value
    """
    # 1. Check environment variable first (highest priority)
    if env_var:
        env_value = os.getenv(env_var)
        if env_value is not None:
            # Convert string to appropriate type
            if isinstance(default, bool):
                return env_value.lower() in ('true', '1', 'yes')
            elif isinstance(default, int):
                try:
                    return int(env_value)
                except ValueError:
                    pass
            elif isinstance(default, float):
                try:
                    return float(env_value)
                except ValueError:
                    pass
            return env_value
    
    # 2. Check YAML config
    if _yaml_config:
        keys = yaml_path.split('.')
        value = _yaml_config
        try:
            for key in keys:
                value = value[key]
            if value is not None:
                return value
        except (KeyError, TypeError):
            pass
    
    # 3. Return default
    return default


# =============================================================================
# AI Provider Registry
# =============================================================================
AI_PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "env_key": "OPENAI_API_KEY",
        "default_model": "gpt-4o-mini",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "env_key": "DEEPSEEK_API_KEY",
        "default_model": "deepseek-chat",
    },
    "claude": {
        "base_url": "https://api.anthropic.com/v1",
        "env_key": "CLAUDE_API_KEY",
        "default_model": "claude-3-haiku-20240307",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "env_key": None,  # No API key needed for local
        "default_model": "llama3",
    },
}


def get_provider_config() -> dict:
    """Get the current AI provider configuration."""
    provider = get_config_value("ai.provider", "AI_PROVIDER", "openai").lower()
    return AI_PROVIDERS.get(provider, AI_PROVIDERS["openai"])


def get_ai_api_key() -> str:
    """Get the API key for the current provider."""
    provider = get_config_value("ai.provider", "AI_PROVIDER", "openai").lower()
    provider_config = AI_PROVIDERS.get(provider, AI_PROVIDERS["openai"])
    
    env_key = provider_config.get("env_key")
    if env_key:
        return os.getenv(env_key, "")
    return ""  # Ollama doesn't need a key


def get_ai_base_url() -> str:
    """Get the base URL for the current provider (or custom if specified)."""
    # Check for custom base_url first
    custom_url = get_config_value("ai.base_url", "AI_BASE_URL", None)
    if custom_url:
        return custom_url
    
    # Otherwise use provider default
    provider_config = get_provider_config()
    return provider_config.get("base_url", "https://api.openai.com/v1")


def get_ai_model() -> str:
    """Get the AI model (from config or provider default)."""
    provider_config = get_provider_config()
    default_model = provider_config.get("default_model", "gpt-4o-mini")
    return get_config_value("ai.model", "AI_MODEL", default_model)


def get_tool_config(tool_name: str) -> Dict[str, Any]:
    """Get configuration for a specific tool."""
    tools_config = _yaml_config.get("tools", {})
    return tools_config.get(tool_name, {})


# =============================================================================
# Configuration Loading with Pydantic Validation
# =============================================================================

def _merge_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """Merge environment variable overrides into config dict."""
    # AI overrides
    if "ai" not in config:
        config["ai"] = {}
    
    if os.getenv("AI_PROVIDER"):
        config["ai"]["provider"] = os.getenv("AI_PROVIDER")
    if os.getenv("AI_MODEL"):
        config["ai"]["model"] = os.getenv("AI_MODEL")
    if os.getenv("AI_BASE_URL"):
        config["ai"]["base_url"] = os.getenv("AI_BASE_URL")
    
    # API key overrides
    if "apis" not in config:
        config["apis"] = {}
    
    if os.getenv("SHODAN_API_KEY"):
        config["apis"]["shodan_api_key"] = os.getenv("SHODAN_API_KEY")
    if os.getenv("BREACHDIRECTORY_API_KEY"):
        config["apis"]["breachdirectory_api_key"] = os.getenv("BREACHDIRECTORY_API_KEY")
    
    return config


def load_validated_config() -> AppConfig:
    """
    Load and validate configuration using Pydantic.
    
    Raises SystemExit with clear error messages if validation fails.
    """
    config_data = _merge_env_overrides(_yaml_config.copy())
    
    try:
        return AppConfig(**config_data)
    except ValidationError as e:
        # Print errors using plain print() to avoid circular imports
        print("\n" + "=" * 60)
        print("❌ CONFIGURATION ERROR - Invalid config.yaml")
        print("=" * 60)
        
        for error in e.errors():
            location = ".".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            print(f"  • {location}: {message}")
        
        print("=" * 60)
        print("Please fix config.yaml and try again.")
        print("See config.example.yaml for valid options.\n")
        sys.exit(1)


# =============================================================================
# Global Settings Instance (Validated)
# =============================================================================
settings = load_validated_config()


# =============================================================================
# Extended Settings Properties (for backward compatibility)
# =============================================================================
class Settings:
    """
    Wrapper class that combines Pydantic config with runtime-resolved values.
    This maintains backward compatibility with existing code.
    """
    
    def __init__(self, config: AppConfig):
        self._config = config
    
    # Delegate to Pydantic config
    @property
    def ai(self):
        return self._config.ai
    
    @property
    def agent(self):
        return self._config.agent
    
    @property
    def paths(self):
        return self._config.paths
    
    @property
    def apis(self):
        return self._config.apis
    
    @property
    def logging(self):
        return self._config.logging
    
    @property
    def ui(self):
        return self._config.ui
    
    # Runtime-resolved properties (need API key lookup)
    @property
    def openai_api_key(self) -> Optional[str]:
        return get_ai_api_key()
    
    @property
    def ai_base_url(self) -> str:
        return get_ai_base_url()
    
    @property
    def ai_model(self) -> str:
        return self._config.ai.model
    
    @property
    def default_project(self) -> str:
        return self._config.agent.default_project
    
    @property
    def max_agent_history(self) -> int:
        return self._config.agent.max_history
    
    @property
    def breachdirectory_api_key(self) -> Optional[str]:
        return self._config.apis.breachdirectory_api_key
    
    @property
    def shodan_api_key(self) -> Optional[str]:
        return self._config.apis.shodan_api_key


# Replace raw config with wrapped Settings
settings = Settings(settings)
