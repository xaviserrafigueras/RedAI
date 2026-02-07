"""
Nmap Scanner and Network Discovery
"""

import os
import shlex
import subprocess

from rich.console import Console
from rich.panel import Panel

from redai.core.display import display
from redai.core.utils import run_sudo, suggest_ai_analysis
from redai.database.repository import save_scan


console = Console()


def scan(target: str, project: str = "General", ports: str = "F", aggressive: bool = False, auto: bool = False):
    """Escanea puertos con Nmap."""
    if not auto:
        display.header(f"Nmap Scanner: {target}")
    
    opciones = "-F" if ports == "F" else f"-p {ports}"
    extra = "-A" if aggressive else ""
    comando = f"nmap {opciones} {extra} {target}"
    
    if not auto:
        console.print(f"[yellow]🚀 Ejecutando en proyecto '{project}':[/yellow] {comando}")
    
    try:
        proceso = run_sudo(shlex.split(comando), capture_output=True)
        resultado_scan = proceso.stdout
        
        if proceso.returncode == 0:
            if not auto:
                console.print(Panel(resultado_scan, title="Nmap Result", border_style="green"))
            
            suggest_ai_analysis(resultado_scan, "nmap")
            save_scan(target=target, command_type="nmap", output=resultado_scan, project_name=project)
            
            if not auto:
                console.print("[bold green]✔ Guardado.[/bold green]")
        else:
            display.error(f"Error Nmap: {proceso.stderr}")
            
    except FileNotFoundError:
        display.error("ERROR: Nmap no instalado o no encontrado en PATH.")
    except Exception as e:
        display.error(f"Error Ejecución: {e}")


def net_scan(target: str = "192.168.1.0/24", project: str = "General", auto: bool = False):
    """Escáner de Red (Descubre dispositivos conectados con Nmap/ARP)."""
    display.header(f"Network Scanner: {target}")
    
    try:
        # Use nmap ping scan
        cmd = ["nmap", "-sn", target]
        display.step("Discovering hosts on network...")
        
        proceso = run_sudo(cmd, capture_output=True)
        
        if proceso.returncode == 0:
            console.print(Panel(proceso.stdout, title="Network Scan Results", border_style="cyan"))
            suggest_ai_analysis(proceso.stdout, "Network Discovery")
            save_scan(target=target, command_type="net_scan", output=proceso.stdout, project_name=project)
        else:
            display.error(f"Scan error: {proceso.stderr}")
            
    except Exception as e:
        display.error(f"Error: {e}")
