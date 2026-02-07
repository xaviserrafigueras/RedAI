"""
Display utilities for Rich console output.
Provides standardized visual output with cyberpunk styling.
"""

import time
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markup import escape
from rich.live import Live
from rich.spinner import Spinner

from redai.config import TOOL_DESCRIPTIONS


class Display:
    """Helper para estandarizar la salida visual con Rich."""
    
    def __init__(self):
        self.console = Console()
    
    def header(self, text: str, subtitle: str = ""):
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_row(f"[bold red]⚔️ {escape(text)} ⚔️[/bold red]")
        if subtitle: 
            grid.add_row(f"[dim]{escape(subtitle)}[/dim]")
        self.console.print(Panel(grid, style="red", border_style="red"))

    def success(self, text: str):
        self.console.print(f"[bold green]✅ {escape(text)}[/bold green]")

    def error(self, text: str):
        self.console.print(f"[bold red]❌ {escape(text)}[/bold red]")

    def warning(self, text: str):
        self.console.print(f"[bold yellow]⚠️ {escape(text)}[/bold yellow]")

    def info(self, text: str):
        self.console.print(f"[bold blue]ℹ️ {escape(text)}[/bold blue]")

    def step(self, text: str):
        self.console.print(f"[cyan]➤ {escape(text)}[/cyan]")
        
    def panel(self, content, title, style="blue"):
        self.console.print(Panel(content, title=title, border_style=style))

    def tool_info(self, key: str):
        desc = TOOL_DESCRIPTIONS.get(key, "No description available.")
        self.panel(desc, f"ℹ️ Tool Help: {key.capitalize().replace('_', ' ')}", style="cyan")

    def cyber_header(self):
        """Muestra el banner estilo Cyberpunk."""
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_row("[bold red]⚡ R E D   A I   C O R T E X   v 2 . 0 ⚡[/bold red]")
        grid.add_row("[dim white]Autonomous Cyber-Security Operative System[/dim white]")
        self.console.print(Panel(grid, style="bold red", border_style="red"))

    def print_hud(self, memory: Any):
        """Print HUD with memory context (placeholder for future implementation)."""
        pass


class CyberDisplay(Display):
    """Clase para la interfaz Cyberpunk extendida."""
    
    def __init__(self):
        super().__init__()

    def thinking_animation(self, text="[bold yellow]AI is thinking...[/bold yellow]", spinner_type="dots"):
        """Muestra una animación de 'pensando' con un spinner."""
        with Live(Spinner(spinner_type, text=text), console=self.console, refresh_per_second=8) as live:
            while True:
                time.sleep(0.1)


# Global instances for easy import
display = Display()
cyber_display = CyberDisplay()
