"""
Utility functions for RedAI.
Includes sudo management, AI analysis hooks, and system helpers.
"""

import subprocess
import os
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt


console = Console()

# --- GLOBAL SUDO MANAGER ---
SUDO_PASSWORD: Optional[str] = None


def get_sudo_pass() -> str:
    """Obtiene la contraseña sudo (caché o prompt)."""
    global SUDO_PASSWORD
    
    # 1. Check if effectively root (Linux)
    if hasattr(os, "geteuid"):
        if os.geteuid() == 0:
            return ""  # Ya es root
            
    # 2. Check Cache
    if SUDO_PASSWORD is not None:
        return SUDO_PASSWORD
        
    # 3. Prompt User
    console.print(Panel(
        "[yellow]⚠️ This tool requires [bold red]ROOT[/bold red] privileges.[/yellow]\n"
        "[dim]Enter your password to authorize sudo actions for this session.[/dim]",
        title="🔒 Privilege Escalation", border_style="red"
    ))
    pwd = Prompt.ask("Password", password=True)
    SUDO_PASSWORD = pwd
    return pwd


def run_sudo(cmd_parts: list, capture_output: bool = True) -> subprocess.CompletedProcess:
    """Ejecuta un comando con sudo -S inyectando la contraseña."""
    pwd = get_sudo_pass()
    
    # Si ya es root, ejecutar directo
    if not pwd: 
        return subprocess.run(cmd_parts, capture_output=capture_output, text=True)
    
    # Si no, construir pipeline: echo PASS | sudo -S cmd
    # Usamos sudo -S -p '' para que lea de stdin sin prompt
    final_cmd = ["sudo", "-S", "-p", ""] + cmd_parts
    
    return subprocess.run(
        final_cmd, 
        input=pwd + "\n", 
        capture_output=capture_output, 
        text=True
    )


def enable_ip_forwarding_windows() -> bool:
    """Enables IP Forwarding on Windows via PowerShell to prevent DoS during ARP Spoofing."""
    if os.name != 'nt':
        return False
        
    try:
        # Check current state
        check_cmd = 'Get-NetIPInterface | Where-Object {$_.Forwarding -eq "Enabled"}'
        result = subprocess.run(
            ["powershell", "-Command", check_cmd],
            capture_output=True, text=True
        )
        
        if "Enabled" not in result.stdout:
            # Enable forwarding
            enable_cmd = 'Set-NetIPInterface -Forwarding Enabled'
            subprocess.run(
                ["powershell", "-Command", enable_cmd],
                capture_output=True, text=True
            )
            console.print("[green]✅ IP Forwarding enabled on Windows.[/green]")
        return True
    except Exception as e:
        console.print(f"[red]❌ Failed to enable IP Forwarding: {e}[/red]")
        return False


def suggest_ai_analysis(output: str, context: str):
    """
    Ofrece al usuario analizar el output de una herramienta usando la IA.
    """
    # Import here to avoid circular imports
    from redai.ai.client import get_client, get_model_name
    from redai.core.display import display
    
    if not output or len(output.strip()) < 5:
        return

    client = get_client()
    if not client:
        return

    # Visual Prompt
    console.print()
    console.print(Panel(
        f"[cyan]Output capture size:[/cyan] {len(output)} bytes.\n"
        "[bold green]Do you want the AI to analyze this result and suggest next steps?[/]",
        title="🤖 AI Analyst", border_style="cyan", style="on black"
    ))
    
    if Prompt.ask("[bold cyan]Analyze?[/]", choices=["y", "n"], default="y") == "y":
        try:
            with console.status("[bold green]Analizando datos...[/]", spinner="dots"):
                prompt = (
                    f"Analyze the following output from the tool '{context}'. "
                    "Explain the key findings, potential vulnerabilities, and suggest 3 actionable next commands.\n\n"
                    f"OUTPUT:\n{output[:4000]}"  # Truncate to avoid context limit
                )
                
                response = client.chat.completions.create(
                    model=get_model_name(),
                    messages=[
                        {"role": "system", "content": "You are a Senior Pentester Assistant. Analyze tool output concise and tactical."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                analysis = response.choices[0].message.content
                
            display.panel(analysis, title=f"🧠 Cortex Analysis: {context}", style="magenta")
            
        except Exception as e:
            display.error(f"AI Analysis Failed: {e}")
