"""
RedAI CLI - Command Line Interface
Main entry point for the application with Typer commands.
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


def interactive_menu():
    """Main interactive menu for RedAI."""
    # Import tools here to avoid circular imports
    from redai.tools.recon.nmap import scan, net_scan
    from redai.tools.recon.subdomains import subdomains, sub_takeover
    from redai.tools.recon.fuzzing import fuzz
    from redai.tools.recon.wordpress import wp_scan
    from redai.tools.recon.shodan import shodan_scan
    from redai.tools.osint.username import username_osint
    from redai.tools.osint.phone import phone_osint
    from redai.tools.osint.dorks import dork_gen
    from redai.tools.osint.metadata import metadata_scan, exif_scan
    from redai.tools.osint.harvester import harvester_scan
    from redai.tools.exploit.sqli import sqli
    from redai.tools.exploit.xss import xss
    from redai.tools.exploit.bruteforce import brute
    from redai.tools.exploit.crack import crack
    from redai.tools.exploit.exploits import search_exploits
    from redai.tools.exploit.payload import payload_gen
    from redai.tools.network.wifi import wifi_audit, wifi_stealer
    from redai.tools.network.sniffer import sniffer
    from redai.tools.network.arp import arp_spoof
    from redai.tools.reporting.html import html_report
    from redai.tools.reporting.phishing import phishing_gen
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Banner Principal con ASCII Art
        display.cyber_header()
        
        # Tabla de Menú
        menu = Table(box=box.SIMPLE_HEAD, show_header=True, header_style="bold magenta", expand=True)
        menu.add_column("🔍 Recon", style="cyan")
        menu.add_column("⚔️ Exploit", style="red")
        menu.add_column("🌐 Network", style="green")
        menu.add_column("🕵️ OSINT", style="yellow")
        
        menu.add_row(
            "1. Nmap Scanner", 
            "5. SQL Injection",
            "10. Msfvenom Payloads",
            "14. Exif Spy"
        )
        menu.add_row(
            "2. Shodan Intel", 
            "6. XSS Scanner", 
            "11. Hash Cracker",
            "15. Username Recon"
        )
        menu.add_row(
            "3. Subdomains", 
            "7. Fuzzing Web", 
            "12. HTML Report",
            "16. Phone OSINT"
        )
        menu.add_row(
            "4. WordPress Scan", 
            "8. SearchSploit", 
            "13. Wi-Fi Auditor",
            "17. Google Dorks"
        )
        menu.add_row(
            "",
            "9. Brute Force",
            "20. Network Sniffer",
            "18. Metadata FOCA"
        )
        menu.add_row(
            "",
            "22. Subdomain Takeover",
            "21. ARP Poison",
            "19. TheHarvester"
        )
        menu.add_row(
            "",
            "23. Phishing Templates",
            "24. Network Scanner",
            ""
        )
        menu.add_row(
            "",
            "26. Wi-Fi Dump",
            "28. JSON Report",
            ""
        )
        menu.add_row(
            "",
            "",
            "29. Markdown Report",
            ""
        )
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
        
        # Project Selection
        project = Prompt.ask("[blue]Project Name[/blue]", default="General")
        
        # --- Menu Options Logic ---
        try:
            if choice == "1":
                display.tool_info("nmap")
                target = Prompt.ask("Target IP")
                scan(target=target, project=project, aggressive=True)
            elif choice == "2":
                display.tool_info("shodan")
                ip = Prompt.ask("IP for Shodan")
                shodan_scan(ip=ip, project=project)
            elif choice == "3":
                display.tool_info("subdomains")
                domain = Prompt.ask("Domain")
                subdomains(domain=domain, project=project)
            elif choice == "4":
                display.tool_info("wordpress")
                url = Prompt.ask("WordPress URL")
                wp_scan(url=url, project=project)
            elif choice == "5":
                display.tool_info("sqli")
                url = Prompt.ask("Vulnerable URL")
                sqli(url=url, project=project)
            elif choice == "6":
                display.tool_info("xss")
                url = Prompt.ask("Target URL (XSS)")
                xss(url=url, project=project)
            elif choice == "7":
                display.tool_info("fuzz")
                url = Prompt.ask("Base URL")
                fuzz(url=url, project=project)
            elif choice == "8":
                display.tool_info("searchsploit")
                term = Prompt.ask("Search Term")
                search_exploits(query=term, project=project)
            elif choice == "9":
                display.tool_info("brute")
                target = Prompt.ask("Target IP")
                user = Prompt.ask("Username", default="root")
                brute(target=target, user=user, project=project)
            elif choice == "10":
                display.tool_info("msfvenom")
                payload_gen(project=project)
            elif choice == "11":
                display.tool_info("hash")
                h = Prompt.ask("Hash to Crack")
                crack(hash_str=h, project=project)
            elif choice == "12":
                display.tool_info("html")
                html_report(project=project)
            elif choice == "28":
                from redai.tools.reporting.json_report import json_report
                json_report(project=project)
            elif choice == "29":
                from redai.tools.reporting.markdown import markdown_report
                markdown_report(project=project)
            elif choice == "99" or choice == "13":
                display.tool_info("agent")
                from redai.tools.agent import agent
                auto = typer.confirm("Enable Autonomous Mode?")
                agent(project=project, auto_approve=auto)
            elif choice == "14":
                display.tool_info("exif")
                img = Prompt.ask("Path to Image")
                exif_scan(image_path=img, project=project)
            elif choice == "15":
                display.tool_info("maigret")
                u = Prompt.ask("Username")
                username_osint(username=u, project=project)
            elif choice == "16":
                display.tool_info("phone")
                num = Prompt.ask("Phone Number (+1...)")
                phone_osint(number=num, project=project)
            elif choice == "17":
                display.tool_info("dorks")
                tgt = Prompt.ask("Target Domain")
                dork_gen(target=tgt, project=project)
            elif choice == "18":
                display.tool_info("metadata")
                fpath = Prompt.ask("File Path")
                metadata_scan(filepath=fpath, project=project)
            elif choice == "19":
                display.tool_info("harvester")
                dom = Prompt.ask("Target Domain")
                harvester_scan(domain=dom, project=project)
            elif choice == "20":
                display.tool_info("wifi")
                iface = Prompt.ask("Wireless Interface", default="wlan0")
                wifi_audit(interface=iface, project=project)
            elif choice == "21":
                display.tool_info("sniffer")
                iface = Prompt.ask("Network Interface", default="eth0")
                pkt = Prompt.ask("Packets to capture", default="50")
                sniffer(interface=iface, count=int(pkt), project=project)
            elif choice == "22":
                display.tool_info("takeover")
                dom = Prompt.ask("Target Subdomain")
                sub_takeover(domain=dom, project=project)
            elif choice == "23":
                display.tool_info("phishing")
                console.print("[cyan]Templates: google, microsoft, netflix, paypal[/cyan]")
                tmpl = Prompt.ask("Select Template", default="google")
                phishing_gen(template=tmpl, project=project)
            elif choice == "24":
                display.tool_info("arp")
                target = Prompt.ask("Target IP (Victim)")
                gateway = Prompt.ask("Gateway IP (Router)")
                mode = Prompt.ask("Mode", choices=["mitm", "kick"], default="mitm")
                arp_spoof(target_ip=target, gateway_ip=gateway, kick=(mode == "kick"), project=project)
            elif choice == "26":
                wifi_stealer(project=project)
            elif choice == "27":
                net = Prompt.ask("Subnet to scan", default="192.168.1.0/24")
                net_scan(target=net, project=project)
            else:
                display.error("Invalid Option")
                
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
