"""
Display utilities for Rich console output.
Provides standardized visual output with cyberpunk styling.
Supports quiet/verbose modes and color themes.
"""

import time
from enum import Enum
from typing import Any, Dict
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markup import escape
from rich.live import Live
from rich.spinner import Spinner

from redai.config import TOOL_DESCRIPTIONS


class OutputMode(Enum):
    """Output verbosity modes."""
    QUIET = "quiet"      # Only errors and final results
    NORMAL = "normal"    # Standard output
    VERBOSE = "verbose"  # Debug information included


@dataclass
class ColorTheme:
    """Color theme definition."""
    name: str
    primary: str       # Headers, main elements
    secondary: str     # Panels, borders
    accent: str        # Steps, highlights
    success: str       # Success messages
    error: str         # Error messages
    warning: str       # Warning messages
    info: str          # Info messages
    dim: str           # Subtle text
    result: str        # Result messages


# Available themes
THEMES: Dict[str, ColorTheme] = {
    "default": ColorTheme(
        name="default",
        primary="bold red",
        secondary="red",
        accent="cyan",
        success="bold green",
        error="bold red",
        warning="bold yellow",
        info="bold blue",
        dim="dim white",
        result="bold cyan"
    ),
    "matrix": ColorTheme(
        name="matrix",
        primary="bold green",
        secondary="green",
        accent="bright_green",
        success="bold bright_green",
        error="bold red",
        warning="bold yellow",
        info="green",
        dim="dim green",
        result="bold bright_green"
    ),
    "ocean": ColorTheme(
        name="ocean",
        primary="bold blue",
        secondary="blue",
        accent="cyan",
        success="bold turquoise2",
        error="bold red",
        warning="bold orange1",
        info="bold steel_blue1",
        dim="dim steel_blue",
        result="bold turquoise2"
    ),
    "purple": ColorTheme(
        name="purple",
        primary="bold purple",
        secondary="magenta",
        accent="orchid",
        success="bold green",
        error="bold red",
        warning="bold orange1",
        info="bold violet",
        dim="dim purple",
        result="bold orchid"
    ),
    "minimal": ColorTheme(
        name="minimal",
        primary="bold white",
        secondary="white",
        accent="white",
        success="bold white",
        error="bold red",
        warning="bold yellow",
        info="white",
        dim="dim",
        result="bold white"
    ),
}


class Display:
    """Helper para estandarizar la salida visual con Rich."""
    
    # Class-level settings (shared across all instances)
    _mode: OutputMode = OutputMode.NORMAL
    _theme: ColorTheme = THEMES["default"]
    
    def __init__(self):
        self.console = Console()
    
    # --- Mode Methods ---
    @classmethod
    def set_mode(cls, mode: OutputMode):
        """Set the global output mode."""
        cls._mode = mode
    
    @classmethod
    def set_quiet(cls):
        """Enable quiet mode."""
        cls._mode = OutputMode.QUIET
    
    @classmethod
    def set_verbose(cls):
        """Enable verbose mode."""
        cls._mode = OutputMode.VERBOSE
    
    @classmethod
    def set_normal(cls):
        """Enable normal mode."""
        cls._mode = OutputMode.NORMAL
    
    @classmethod
    def is_quiet(cls) -> bool:
        """Check if quiet mode is enabled."""
        return cls._mode == OutputMode.QUIET
    
    @classmethod
    def is_verbose(cls) -> bool:
        """Check if verbose mode is enabled."""
        return cls._mode == OutputMode.VERBOSE
    
    # --- Theme Methods ---
    @classmethod
    def set_theme(cls, theme_name: str):
        """Set the color theme by name."""
        if theme_name in THEMES:
            cls._theme = THEMES[theme_name]
        else:
            # Default to 'default' if invalid theme
            cls._theme = THEMES["default"]
    
    @classmethod
    def get_theme(cls) -> ColorTheme:
        """Get the current theme."""
        return cls._theme
    
    @classmethod
    def get_available_themes(cls) -> list:
        """Get list of available theme names."""
        return list(THEMES.keys())
    
    # --- Display Methods ---
    def header(self, text: str, subtitle: str = ""):
        """Show header (hidden in quiet mode)."""
        if self._mode == OutputMode.QUIET:
            return
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_row(f"[{self._theme.primary}]⚔️ {escape(text)} ⚔️[/{self._theme.primary}]")
        if subtitle: 
            grid.add_row(f"[{self._theme.dim}]{escape(subtitle)}[/{self._theme.dim}]")
        self.console.print(Panel(grid, style=self._theme.secondary, border_style=self._theme.secondary))

    def success(self, text: str):
        """Show success message (always shown)."""
        self.console.print(f"[{self._theme.success}]✅ {escape(text)}[/{self._theme.success}]")

    def error(self, text: str):
        """Show error message (always shown)."""
        self.console.print(f"[{self._theme.error}]❌ {escape(text)}[/{self._theme.error}]")

    def warning(self, text: str):
        """Show warning message (always shown)."""
        self.console.print(f"[{self._theme.warning}]⚠️ {escape(text)}[/{self._theme.warning}]")

    def info(self, text: str):
        """Show info message (hidden in quiet mode)."""
        if self._mode == OutputMode.QUIET:
            return
        self.console.print(f"[{self._theme.info}]ℹ️ {escape(text)}[/{self._theme.info}]")

    def step(self, text: str):
        """Show step message (hidden in quiet mode)."""
        if self._mode == OutputMode.QUIET:
            return
        self.console.print(f"[{self._theme.accent}]➤ {escape(text)}[/{self._theme.accent}]")
    
    def debug(self, text: str):
        """Show debug message (only in verbose mode)."""
        if self._mode != OutputMode.VERBOSE:
            return
        self.console.print(f"[dim magenta]🔍 DEBUG: {escape(text)}[/dim magenta]")
        
    def panel(self, content, title, style=None):
        """Show panel (hidden in quiet mode)."""
        if style is None:
            style = self._theme.accent
        if self._mode == OutputMode.QUIET:
            # In quiet mode, just print minimal output
            self.console.print(f"[dim]--- {title} ---[/dim]")
            if isinstance(content, str):
                lines = content.split('\n')[:5]
                self.console.print('\n'.join(lines))
                if len(content.split('\n')) > 5:
                    self.console.print("[dim]...(truncated)[/dim]")
            return
        self.console.print(Panel(content, title=title, border_style=style))

    def tool_info(self, key: str):
        """Show tool info (hidden in quiet mode)."""
        if self._mode == OutputMode.QUIET:
            return
        desc = TOOL_DESCRIPTIONS.get(key, "No description available.")
        self.panel(desc, f"ℹ️ Tool Help: {key.capitalize().replace('_', ' ')}", style=self._theme.accent)

    def cyber_header(self):
        """Muestra el banner estilo Cyberpunk (hidden in quiet mode)."""
        if self._mode == OutputMode.QUIET:
            return
        
        # ASCII Art banner
        ascii_art = f"""
[{self._theme.primary}]
    ██████╗ ███████╗██████╗      █████╗ ██╗
    ██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██║
    ██████╔╝█████╗  ██║  ██║    ███████║██║
    ██╔══██╗██╔══╝  ██║  ██║    ██╔══██║██║
    ██║  ██║███████╗██████╔╝    ██║  ██║██║
    ╚═╝  ╚═╝╚══════╝╚═════╝     ╚═╝  ╚═╝╚═╝
[/{self._theme.primary}]
[{self._theme.accent}]        ⚡ C O R T E X   v 1 . 0 ⚡[/{self._theme.accent}]
[{self._theme.dim}]    Autonomous Pentesting Framework[/{self._theme.dim}]

[{self._theme.accent}]    👤 Xavi Serra Figueras[/{self._theme.accent}]
[{self._theme.dim}]    GitHub: github.com/xaviserrafigueras[/{self._theme.dim}]
[{self._theme.dim}]    LinkedIn: linkedin.com/in/xaviserrafigueras[/{self._theme.dim}]
"""
        self.console.print(Panel(ascii_art, border_style=self._theme.secondary))

    def print_hud(self, memory: Any):
        """Print HUD with memory context (placeholder for future implementation)."""
        pass
    
    def result(self, text: str):
        """Show result message (always shown, even in quiet mode)."""
        self.console.print(f"[{self._theme.result}]📋 {escape(text)}[/{self._theme.result}]")


class CyberDisplay(Display):
    """Clase para la interfaz Cyberpunk extendida."""
    
    def __init__(self):
        super().__init__()

    def thinking_animation(self, text=None, spinner_type="dots"):
        """Muestra una animación de 'pensando' con un spinner (hidden in quiet mode)."""
        if self._mode == OutputMode.QUIET:
            return
        if text is None:
            text = f"[{self._theme.warning}]AI is thinking...[/{self._theme.warning}]"
        with Live(Spinner(spinner_type, text=text), console=self.console, refresh_per_second=8) as live:
            while True:
                time.sleep(0.1)


# Global instances for easy import
display = Display()
cyber_display = CyberDisplay()
