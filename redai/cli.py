"""
RedAI CLI - Command Line Interface
Main entry point for the application with Typer commands.
Refactored to use data-driven menu system.
"""

import os
import platform
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.align import Align

from redai.core.display import display, Display
from redai.core.menu import (
    MENU_OPTIONS, 
    get_option_by_id, 
    get_options_by_category,
    CATEGORY_CONFIG
)
from redai.core.handlers import HANDLERS
from redai.database.repository import init_db


def check_os_compatibility():
    """Check if running on Linux/Kali and show warning if not."""
    system = platform.system()
    
    if system != "Linux":
        console = Console()
        console.print()
        console.print(Panel(
            f"[bold yellow]⚠️  RedAI está diseñado para [cyan]Kali Linux[/cyan][/bold yellow]\n\n"
            f"Sistema detectado: [red]{system}[/red]\n\n"
            f"Algunas herramientas (nmap, gobuster, sqlmap, etc.) pueden no funcionar.\n"
            f"Para la mejor experiencia, ejecuta RedAI en Kali Linux o usa Docker.",
            title="[bold yellow]Aviso de Compatibilidad[/bold yellow]",
            border_style="yellow"
        ))
        console.print()
        return False
    return True


# Create Typer app
app = typer.Typer(
    name="redai",
    help="RedAI - Automated Pentesting CLI with AI",
    add_completion=False
)

console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Minimal output (only errors and results)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Debug output (show all details)"),
    theme: str = typer.Option(None, "--theme", "-t", help="Color theme: default, matrix, ocean, purple, minimal")
):
    """RedAI - Ultimate Pentest Suite with AI"""
    # Set output mode based on flags
    if quiet:
        Display.set_quiet()
    elif verbose:
        Display.set_verbose()
    else:
        Display.set_normal()
    
    # Set color theme (only if specified)
    if theme:
        Display.set_theme(theme)
    
    # Check OS compatibility (show warning if not Linux)
    check_os_compatibility()
    
    init_db()
    if ctx.invoked_subcommand is None:
        interactive_menu()


def render_menu_table():
    """Render the menu table from MENU_OPTIONS data."""
    menu = Table(box=box.SIMPLE_HEAD, show_header=True, header_style="bold magenta", expand=True)
    
    # Add columns for each category
    categories = ["recon", "exploit", "network", "osint", "reporting"]
    for cat in categories:
        config = CATEGORY_CONFIG.get(cat, {})
        emoji = config.get("emoji", "")
        name = config.get("name", cat.title())
        style = config.get("style", "white")
        menu.add_column(f"{emoji} {name}", style=style)
    
    # Get max items per category
    cat_options = {cat: get_options_by_category(cat) for cat in categories}
    max_rows = max(len(opts) for opts in cat_options.values())
    
    # Build rows
    for i in range(max_rows):
        row = []
        for cat in categories:
            opts = cat_options[cat]
            if i < len(opts):
                opt = opts[i]
                row.append(f"{opt.id}. {opt.name}")
            else:
                row.append("")
        menu.add_row(*row)
    
    return menu


def interactive_menu():
    """Main interactive menu for RedAI - Data-driven version."""
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Banner Principal con ASCII Art
        display.cyber_header()
        
        # Render menu from data
        menu = render_menu_table()
        console.print(menu)
        
        # Special AI Option
        console.print(Panel(
            Align.center("[bold red]🧠 99. RED AI CORTEX (Autonomous Agent) 🧠[/bold red]"),
            border_style="red"
        ))

        console.print("\n[dim]Select an option number... (0 to exit)[/dim]")
        
        choice = Prompt.ask("[bold yellow]RedAI >[/bold yellow]")
        
        if choice == "0":
            console.print("[red]Saliendo...[/red]")
            break
        
        # Get option from registry
        option = get_option_by_id(choice)
        
        if not option:
            display.error("Invalid Option")
            Prompt.ask("\n[dim]Press Enter to continue...[/dim]")
            continue
        
        # Project Selection
        project = Prompt.ask("[blue]Project Name[/blue]", default="General")
        
        # Show tool info
        display.tool_info(option.tool_key)
        
        # Collect prompts dynamically
        kwargs = {"project": project}
        for prompt_config in option.prompts:
            if prompt_config.choices:
                console.print(f"[cyan]Options: {', '.join(prompt_config.choices)}[/cyan]")
                kwargs[prompt_config.name] = Prompt.ask(
                    prompt_config.label,
                    default=prompt_config.default,
                    choices=prompt_config.choices
                )
            else:
                kwargs[prompt_config.name] = Prompt.ask(
                    prompt_config.label,
                    default=prompt_config.default
                )
        
        # Execute handler
        try:
            handler = HANDLERS.get(option.handler)
            if handler:
                handler(**kwargs)
            else:
                display.error(f"Handler not found: {option.handler}")
        except Exception as e:
            display.error(f"Runtime Error: {e}")
            
        Prompt.ask("\n[dim]Press Enter to return to menu...[/dim]")


# Register tool commands to the app
def register_commands():
    """Register all tool commands to the Typer app."""
    # Import directly from module files to avoid __init__.py conflicts
    from redai.tools.recon import nmap as nmap_mod
    from redai.tools.recon import subdomains as sub_mod
    from redai.tools.recon import fuzzing as fuzz_mod
    from redai.tools.recon import wordpress as wp_mod
    from redai.tools.recon import shodan as shodan_mod
    from redai.tools.osint import username as user_mod
    from redai.tools.osint import phone as phone_mod
    from redai.tools.osint import dorks as dorks_mod
    from redai.tools.osint import metadata as meta_mod
    from redai.tools.osint import harvester as harv_mod
    from redai.tools.exploit import sqli as sqli_mod
    from redai.tools.exploit import xss as xss_mod
    from redai.tools.exploit import bruteforce as brute_mod
    from redai.tools.exploit import crack as crack_mod
    from redai.tools.exploit import exploits as exp_mod
    from redai.tools.exploit import payload as pay_mod
    from redai.tools.network import wifi as wifi_mod
    from redai.tools.network import sniffer as sniff_mod
    from redai.tools.network import arp as arp_mod
    from redai.tools.reporting import html as html_mod
    from redai.tools.reporting import phishing as phish_mod
    
    # Recon
    app.command(name="scan")(nmap_mod.scan)
    app.command(name="net-scan")(nmap_mod.net_scan)
    app.command(name="subdomains")(sub_mod.subdomains)
    app.command(name="sub-takeover")(sub_mod.sub_takeover)
    app.command(name="fuzz")(fuzz_mod.fuzz)
    app.command(name="wp-scan")(wp_mod.wp_scan)
    app.command(name="shodan")(shodan_mod.shodan_scan)
    
    # OSINT
    app.command(name="username")(user_mod.username_osint)
    app.command(name="phone")(phone_mod.phone_osint)
    app.command(name="dorks")(dorks_mod.dork_gen)
    app.command(name="metadata")(meta_mod.metadata_scan)
    app.command(name="exif")(meta_mod.exif_scan)
    app.command(name="harvester")(harv_mod.harvester_scan)
    
    # Exploit
    app.command(name="sqli")(sqli_mod.sqli)
    app.command(name="xss")(xss_mod.xss)
    app.command(name="brute")(brute_mod.brute)
    app.command(name="crack")(crack_mod.crack)
    app.command(name="exploits")(exp_mod.search_exploits)
    app.command(name="payload")(pay_mod.payload_gen)
    
    # Network
    app.command(name="wifi-audit")(wifi_mod.wifi_audit)
    app.command(name="wifi-stealer")(wifi_mod.wifi_stealer)
    app.command(name="sniffer")(sniff_mod.sniffer)
    app.command(name="arp-spoof")(arp_mod.arp_spoof)
    
    # Reporting
    app.command(name="html-report")(html_mod.html_report)
    app.command(name="phishing")(phish_mod.phishing_gen)


# Try to register commands (will fail if tool modules not yet created)
try:
    register_commands()
except ImportError:
    pass  # Tools not yet migrated, will use interactive menu only
