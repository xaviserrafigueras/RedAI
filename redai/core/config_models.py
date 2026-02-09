"""
Pydantic configuration models for RedAI.
Provides type validation and clear error messages for config.yaml.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field


# =============================================================================
# Nested Configuration Models
# =============================================================================

class RetryConfig(BaseModel):
    """Retry configuration for API calls."""
    max_attempts: int = Field(3, ge=1, le=10, description="Maximum retry attempts")
    min_wait: int = Field(2, ge=1, description="Minimum wait between retries (seconds)")
    max_wait: int = Field(30, ge=1, description="Maximum wait between retries (seconds)")


class AIConfig(BaseModel):
    """AI provider configuration."""
    provider: Literal["openai", "deepseek", "claude", "ollama"] = Field(
        "openai", 
        description="AI provider to use"
    )
    model: str = Field("gpt-4o-mini", description="Model name")
    base_url: Optional[str] = Field(None, description="Custom API base URL (overrides provider default)")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(4000, ge=1, le=128000, description="Maximum tokens per response")
    retry: RetryConfig = Field(default_factory=RetryConfig)


class AgentConfig(BaseModel):
    """Autonomous agent configuration."""
    max_steps: int = Field(20, ge=1, le=100, description="Maximum steps per objective")
    command_timeout: int = Field(120, ge=10, le=3600, description="Command timeout in seconds")
    auto_approve: bool = Field(False, description="Auto-approve commands (DANGEROUS)")
    max_history: int = Field(15, ge=1, le=50, description="Max history messages in context")
    default_project: str = Field("General", description="Default project name")


class PathsConfig(BaseModel):
    """File paths configuration."""
    logs: str = Field("./logs", description="Log files directory")
    reports: str = Field("./reports", description="Reports output directory")
    database: str = Field("./database.db", description="SQLite database path")


class APIsConfig(BaseModel):
    """External API keys configuration."""
    breachdirectory_api_key: Optional[str] = Field(None, description="BreachDirectory API key")
    shodan_api_key: Optional[str] = Field(None, description="Shodan API key")


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        "INFO", 
        description="Log level"
    )
    file_enabled: bool = Field(True, description="Enable file logging")
    console_enabled: bool = Field(True, description="Enable console logging")
    retention_days: int = Field(30, ge=0, description="Keep logs for N days (0=forever)")


class UIConfig(BaseModel):
    """UI configuration."""
    show_banner: bool = Field(True, description="Show startup banner")
    theme: str = Field("default", description="Color theme name")
    verbose: bool = Field(False, description="Verbose output mode")


class ToolConfig(BaseModel):
    """Individual tool configuration."""
    default_args: Optional[str] = None
    wordlist: Optional[str] = None
    timeout: int = Field(300, ge=10, description="Tool timeout in seconds")


# =============================================================================
# Main Configuration Model
# =============================================================================

class AppConfig(BaseModel):
    """Main application configuration container."""
    ai: AIConfig = Field(default_factory=AIConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    apis: APIsConfig = Field(default_factory=APIsConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    tools: dict[str, ToolConfig] = Field(default_factory=dict)
    
    # Legacy compatibility properties
    @property
    def openai_api_key(self) -> Optional[str]:
        """Legacy property for backward compatibility."""
        return None  # Will be resolved by config.py get_ai_api_key()
    
    @property
    def ai_base_url(self) -> str:
        """Legacy property for backward compatibility."""
        return self.ai.base_url or ""
    
    @property
    def ai_model(self) -> str:
        """Legacy property for backward compatibility."""
        return self.ai.model
    
    @property
    def default_project(self) -> str:
        """Legacy property for backward compatibility."""
        return self.agent.default_project
    
    @property
    def max_agent_history(self) -> int:
        """Legacy property for backward compatibility."""
        return self.agent.max_history
    
    @property
    def breachdirectory_api_key(self) -> Optional[str]:
        """Legacy property for backward compatibility."""
        return self.apis.breachdirectory_api_key
    
    @property
    def shodan_api_key(self) -> Optional[str]:
        """Legacy property for backward compatibility."""
        return self.apis.shodan_api_key
