"""
Subdomain Enumeration and Takeover Detection
"""

import subprocess
import shutil

import dns.resolver
from rich.console import Console
from rich.panel import Panel

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis, ensure_tool_installed
from redai.database.repository import save_scan
from rich.prompt import Prompt


console = Console()


def subdomains(domain: str, project: str = "General", auto: bool = False):
    """Reconocimiento pasivo de subdominios con elección de herramienta."""
    display.header(f"Subdomain Enumeration ({domain})")
    
    # Ask user which tool to use
    console.print("\n[cyan]Herramientas disponibles:[/cyan]")
    console.print("  [bold]1.[/bold] Sublist3r - Clásico, múltiples fuentes")
    console.print("  [bold]2.[/bold] Subfinder - Moderno, rápido, +50 fuentes (recomendado)")
    
    tool_choice = Prompt.ask("[yellow]Selecciona herramienta[/yellow]", choices=["1", "2"], default="2")
    
    if tool_choice == "1":
        _run_sublist3r(domain, project)
    else:
        _run_subfinder(domain, project)


def _run_sublist3r(domain: str, project: str):
    """Ejecuta sublist3r para enumerar subdominios."""
    try:
        display.step(f"Usando Sublist3r para {domain}...")
        
        if not ensure_tool_installed("sublist3r", "sublist3r"):
            return

        cmd = ["sublist3r", "-d", domain, "-t", "10", "-n"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        
        output = proc.stdout + proc.stderr
        
        # Extraer solo subdominios del output (filtrar errores)
        subdomains_found = _extract_subdomains(output, domain)
        
        if subdomains_found:
            display.success(f"Encontrados {len(subdomains_found)} subdominios:")
            for sub in subdomains_found:
                console.print(f"  [green]•[/green] {sub}")
        
        display.panel(output, f"Subdomains: {domain}")
        suggest_ai_analysis(output, "Subdomain Enumeration")
        save_scan(target=domain, command_type="subdomains", output=output, project_name=project)

    except Exception as e:
        display.error(f"Error: {e}")


def _run_subfinder(domain: str, project: str):
    """Ejecuta subfinder para enumerar subdominios (recomendado)."""
    try:
        display.step(f"Usando Subfinder para {domain}...")
        
        # Check if subfinder is installed
        if not shutil.which("subfinder"):
            console.print("\n[yellow]⚠️ Subfinder no está instalado.[/yellow]")
            console.print("[dim]Instálalo con:[/dim]")
            console.print("  [cyan]go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest[/cyan]")
            console.print("  [dim]O en Kali:[/dim] [cyan]sudo apt install subfinder[/cyan]")
            
            # Fallback to sublist3r
            if Prompt.ask("\n¿Usar Sublist3r en su lugar?", choices=["y", "n"], default="y") == "y":
                _run_sublist3r(domain, project)
            return

        cmd = ["subfinder", "-d", domain, "-silent"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        output = proc.stdout.strip()
        subdomains_found = [line.strip() for line in output.split("\n") if line.strip()]
        
        if subdomains_found:
            display.success(f"Encontrados {len(subdomains_found)} subdominios:")
            for sub in subdomains_found[:30]:  # Mostrar máximo 30
                console.print(f"  [green]•[/green] {sub}")
            if len(subdomains_found) > 30:
                console.print(f"  [dim]... y {len(subdomains_found) - 30} más[/dim]")
        else:
            display.warning("No se encontraron subdominios.")
        
        full_output = "\n".join(subdomains_found)
        suggest_ai_analysis(full_output, "Subdomain Enumeration (Subfinder)")
        save_scan(target=domain, command_type="subdomains", output=full_output, project_name=project)

    except subprocess.TimeoutExpired:
        display.error("Timeout: el escaneo tardó demasiado.")
    except Exception as e:
        display.error(f"Error: {e}")


def _extract_subdomains(output: str, domain: str) -> list:
    """Extrae subdominios válidos del output de sublist3r."""
    import re
    pattern = rf"[\w.-]+\.{re.escape(domain)}"
    matches = re.findall(pattern, output, re.IGNORECASE)
    return list(set(matches))


def sub_takeover(domain: str, project: str = "General", auto: bool = False):
    """Verificación de vulnerabilidad Subdomain Takeover."""
    if not auto:
        display.tool_info("takeover")
    display.header(f"Subdomain Takeover Check: {domain}")
    
    vuln_signatures = {
        "github.io": "GitHub Pages",
        "herokuapp.com": "Heroku",
        "s3.amazonaws.com": "AWS S3",
        "bitbucket.org": "Bitbucket",
        "azurewebsites.net": "Azure App",
        "ghost.io": "Ghost",
        "pantheon.io": "Pantheon",
        "myshopify.com": "Shopify",
        "tumblr.com": "Tumblr",
        "wordpress.com": "WordPress",
    }

    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        out_msg = ""
        vulnerable = False
        
        for rdata in answers:
            cname = str(rdata.target)
            display.info(f"CNAME found: {cname}")
            
            for sig, platform in vuln_signatures.items():
                if sig in cname:
                    msg = f"🚨 POTENTIAL TAKEOVER: {domain} -> {cname} ({platform})"
                    console.print(Panel(msg, style="bold red"))
                    out_msg += msg + "\n"
                    vulnerable = True
                    break
            
            if not vulnerable:
                out_msg += f"CNAME: {cname} (No known takeover signature detected)\n"

        if not vulnerable:
            display.success(f"{domain} seems safe (CNAME check).")
            
        save_scan(domain, "sub_takeover", out_msg, project)

    except dns.resolver.NoAnswer:
        display.warning("No CNAME record found.")
    except Exception as e:
        display.error(f"DNS Error: {e}")
