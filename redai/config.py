"""
Centralized Configuration for RedAI
Loads configuration from YAML file, environment variables, and defaults.
Priority: Environment Variables > YAML Config > Defaults
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from dotenv import load_dotenv

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


@dataclass
class AISettings:
    """AI-related settings."""
    api_key: Optional[str] = field(default_factory=lambda: get_config_value(
        "ai.api_key", "OPENAI_API_KEY", None
    ))
    base_url: str = field(default_factory=lambda: get_config_value(
        "ai.base_url", "AI_BASE_URL", "https://api.openai.com/v1"
    ))
    model: str = field(default_factory=lambda: get_config_value(
        "ai.model", "AI_MODEL", "gpt-4o-mini"
    ))
    temperature: float = field(default_factory=lambda: get_config_value(
        "ai.temperature", None, 0.7
    ))
    max_tokens: int = field(default_factory=lambda: get_config_value(
        "ai.max_tokens", None, 4000
    ))
    retry_max_attempts: int = field(default_factory=lambda: get_config_value(
        "ai.retry.max_attempts", None, 3
    ))
    retry_min_wait: int = field(default_factory=lambda: get_config_value(
        "ai.retry.min_wait", None, 2
    ))
    retry_max_wait: int = field(default_factory=lambda: get_config_value(
        "ai.retry.max_wait", None, 30
    ))


@dataclass
class AgentSettings:
    """Agent-related settings."""
    max_steps: int = field(default_factory=lambda: get_config_value(
        "agent.max_steps", None, 20
    ))
    command_timeout: int = field(default_factory=lambda: get_config_value(
        "agent.command_timeout", None, 120
    ))
    auto_approve: bool = field(default_factory=lambda: get_config_value(
        "agent.auto_approve", None, False
    ))
    max_history: int = field(default_factory=lambda: get_config_value(
        "agent.max_history", None, 15
    ))
    default_project: str = field(default_factory=lambda: get_config_value(
        "agent.default_project", None, "General"
    ))


@dataclass
class PathSettings:
    """Path-related settings."""
    logs: str = field(default_factory=lambda: get_config_value(
        "paths.logs", None, "./logs"
    ))
    reports: str = field(default_factory=lambda: get_config_value(
        "paths.reports", None, "./reports"
    ))
    database: str = field(default_factory=lambda: get_config_value(
        "paths.database", None, "./database.db"
    ))


@dataclass
class APISettings:
    """External API settings."""
    breachdirectory_api_key: Optional[str] = field(default_factory=lambda: get_config_value(
        "apis.breachdirectory_api_key", "BREACHDIRECTORY_API_KEY", None
    ))
    shodan_api_key: Optional[str] = field(default_factory=lambda: get_config_value(
        "apis.shodan_api_key", "SHODAN_API_KEY", None
    ))


@dataclass 
class LoggingSettings:
    """Logging-related settings."""
    level: str = field(default_factory=lambda: get_config_value(
        "logging.level", None, "INFO"
    ))
    file_enabled: bool = field(default_factory=lambda: get_config_value(
        "logging.file_enabled", None, True
    ))
    console_enabled: bool = field(default_factory=lambda: get_config_value(
        "logging.console_enabled", None, True
    ))
    retention_days: int = field(default_factory=lambda: get_config_value(
        "logging.retention_days", None, 30
    ))


@dataclass
class UISettings:
    """UI-related settings."""
    show_banner: bool = field(default_factory=lambda: get_config_value(
        "ui.show_banner", None, True
    ))
    theme: str = field(default_factory=lambda: get_config_value(
        "ui.theme", None, "default"
    ))
    verbose: bool = field(default_factory=lambda: get_config_value(
        "ui.verbose", None, False
    ))


@dataclass
class Settings:
    """Main application settings container."""
    ai: AISettings = field(default_factory=AISettings)
    agent: AgentSettings = field(default_factory=AgentSettings)
    paths: PathSettings = field(default_factory=PathSettings)
    apis: APISettings = field(default_factory=APISettings)
    logging: LoggingSettings = field(default_factory=LoggingSettings)
    ui: UISettings = field(default_factory=UISettings)
    
    # Legacy compatibility properties
    @property
    def openai_api_key(self) -> Optional[str]:
        return self.ai.api_key
    
    @property
    def ai_base_url(self) -> str:
        return self.ai.base_url
    
    @property
    def ai_model(self) -> str:
        return self.ai.model
    
    @property
    def default_project(self) -> str:
        return self.agent.default_project
    
    @property
    def max_agent_history(self) -> int:
        return self.agent.max_history
    
    @property
    def breachdirectory_api_key(self) -> Optional[str]:
        return self.apis.breachdirectory_api_key
    
    @property
    def shodan_api_key(self) -> Optional[str]:
        return self.apis.shodan_api_key


def get_tool_config(tool_name: str) -> Dict[str, Any]:
    """Get configuration for a specific tool."""
    tools_config = _yaml_config.get("tools", {})
    return tools_config.get(tool_name, {})


# Global settings instance
settings = Settings()


# Tool descriptions for help system
TOOL_DESCRIPTIONS = {
    "nmap": "Escáner de red para descubrir hosts y servicios abiertos. Uso: nmap -sV -sC <target>.",
    "shodan": "Motor de búsqueda de dispositivos conectados (IoT, Servidores). Requiere API Key.",
    "sqlmap": "Herramienta automática de SQL Injection. Detecta y explota vulns DB.",
    "gobuster": "Fuzzer de directorios y subdominios usando diccionarios.",
    "hashcat": "Cracker de hashes GPU-accelerated. Soporta MD5, SHA, NTLM, etc.",
    "hydra": "Cracker de fuerza bruta para protocolos (SSH, FTP, HTTP, etc.).",
    "wifite": "Auditoría automatizada de redes Wi-Fi (WEP, WPA, WPS).",
    "aircrack-ng": "Suite completa para hackear redes Wi-Fi.",
    "metasploit": "Framework de explotación con miles de exploits y payloads.",
    "nikto": "Escáner de vulnerabilidades web (misconfigs, archivos peligrosos).",
    "wpscan": "Escáner especializado en WordPress (plugins, temas, usuarios).",
    "maigret": "Rastreo de nombre de usuario en 3000+ sitios web (OSINT).",
    "phone": "Inteligencia de números telefónicos (Operadora, País, Zona Horaria).",
    "harvester": "Recolector de emails, subdominios y hosts (TheHarvester).",
    "dorks": "Generador de Google Dorks para encontrar archivos sensibles y paneles.",
    "metadata": "Extracción profunda de metadatos en documentos y archivos (PDF, DOC, IMG).",
    "wifi": "Gestión de perfiles Wi-Fi guardados y ataques de desautenticación.",
    "sniffer": "Captura y análisis de tráfico de red en tiempo real (Scapy).",
    "arp": "Ataque MITM (ARP Spoofing) para interceptar tráfico o cortar internet (Kick).",
    "dns": "DNS Spoofing para redirigir tráfico de dominios legítimos a una IP maliciosa.",
}
