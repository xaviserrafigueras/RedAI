"""
Menu Handlers - Centralized handler functions for all menu options
"""

from rich.console import Console
from rich.prompt import Prompt
import typer

console = Console()


# =============================================================================
# RECON HANDLERS (1-9)
# =============================================================================

def handle_nmap(target: str, project: str):
    """Handle Nmap scanning."""
    from redai.tools.recon.nmap import scan
    scan(target=target, project=project, aggressive=True)


def handle_shodan(ip: str, project: str):
    """Handle Shodan intel lookup."""
    from redai.tools.recon.shodan import shodan_scan
    shodan_scan(ip=ip, project=project)


def handle_subdomains(domain: str, project: str):
    """Handle subdomain enumeration."""
    from redai.tools.recon.subdomains import subdomains
    subdomains(domain=domain, project=project)


def handle_wordpress(url: str, project: str):
    """Handle WordPress scanning."""
    from redai.tools.recon.wordpress import wp_scan
    wp_scan(url=url, project=project)


def handle_fuzz(url: str, project: str):
    """Handle web fuzzing."""
    from redai.tools.recon.fuzzing import fuzz
    fuzz(url=url, project=project)


# =============================================================================
# EXPLOIT HANDLERS (10-19)
# =============================================================================

def handle_sqli(url: str, project: str):
    """Handle SQL injection testing."""
    from redai.tools.exploit.sqli import sqli
    sqli(url=url, project=project)


def handle_xss(url: str, project: str):
    """Handle XSS scanning."""
    from redai.tools.exploit.xss import xss
    xss(url=url, project=project)


def handle_searchsploit(term: str, project: str):
    """Handle exploit search."""
    from redai.tools.exploit.exploits import search_exploits
    search_exploits(query=term, project=project)


def handle_brute(target: str, user: str, project: str):
    """Handle brute force attack."""
    from redai.tools.exploit.bruteforce import brute
    brute(target=target, user=user, project=project)


def handle_msfvenom(project: str):
    """Handle payload generation."""
    from redai.tools.exploit.payload import payload_gen
    payload_gen(project=project)


def handle_phishing(template: str, project: str):
    """Handle phishing template generation."""
    from redai.tools.exploit.phishing import phishing_gen
    phishing_gen(template=template, project=project)


def handle_takeover(domain: str, project: str):
    """Handle subdomain takeover check."""
    from redai.tools.recon.subdomains import sub_takeover
    sub_takeover(domain=domain, project=project)


# =============================================================================
# NETWORK HANDLERS (20-29)
# =============================================================================

def handle_wifi(interface: str, project: str):
    """Handle Wi-Fi auditing."""
    from redai.tools.network.wifi import wifi_audit
    wifi_audit(interface=interface, project=project)


def handle_wifi_dump(project: str):
    """Handle Wi-Fi password dumping."""
    from redai.tools.network.wifi import wifi_stealer
    wifi_stealer(project=project)


def handle_sniffer(interface: str, count: str, project: str):
    """Handle network sniffing."""
    from redai.tools.network.sniffer import sniffer
    sniffer(interface=interface, count=int(count), project=project)


def handle_arp(target: str, gateway: str, mode: str, project: str):
    """Handle ARP poisoning."""
    from redai.tools.network.arp import arp_spoof
    arp_spoof(target_ip=target, gateway_ip=gateway, kick=(mode == "kick"), project=project)


def handle_netscan(subnet: str, project: str):
    """Handle network scanning."""
    from redai.tools.network.netscan import net_scan
    net_scan(target=subnet, project=project)


def handle_hash(hash_str: str, project: str):
    """Handle hash cracking."""
    from redai.tools.exploit.crack import crack
    crack(hash_str=hash_str, project=project)


# =============================================================================
# OSINT HANDLERS (30-39)
# =============================================================================

def handle_exif(image_path: str, project: str):
    """Handle EXIF metadata extraction."""
    from redai.tools.osint.metadata import exif_scan
    exif_scan(image_path=image_path, project=project)


def handle_username(username: str, project: str):
    """Handle username OSINT."""
    from redai.tools.osint.username import username_osint
    username_osint(username=username, project=project)


def handle_phone(number: str, project: str):
    """Handle phone number OSINT."""
    from redai.tools.osint.phone import phone_osint
    phone_osint(number=number, project=project)


def handle_dorks(target: str, project: str):
    """Handle Google dork generation."""
    from redai.tools.osint.dorks import dork_gen
    dork_gen(target=target, project=project)


def handle_metadata(filepath: str, project: str):
    """Handle metadata extraction."""
    from redai.tools.osint.metadata import metadata_scan
    metadata_scan(filepath=filepath, project=project)


def handle_harvester(domain: str, project: str):
    """Handle TheHarvester OSINT."""
    from redai.tools.osint.harvester import harvester_scan
    harvester_scan(domain=domain, project=project)


# =============================================================================
# REPORTING HANDLERS (40-49)
# =============================================================================

def handle_html_report(project: str):
    """Generate HTML report."""
    from redai.tools.reporting.html import html_report
    html_report(project=project)


def handle_json_report(project: str):
    """Generate JSON report."""
    from redai.tools.reporting.json_report import json_report
    json_report(project=project)


def handle_markdown_report(project: str):
    """Generate Markdown report."""
    from redai.tools.reporting.markdown import markdown_report
    markdown_report(project=project)


# =============================================================================
# SPECIAL HANDLERS
# =============================================================================

def handle_cortex(project: str):
    """Handle AI Cortex agent."""
    from redai.tools.agent import agent
    auto = typer.confirm("Enable Autonomous Mode?")
    agent(project=project, auto_approve=auto)


# =============================================================================
# HANDLER REGISTRY
# =============================================================================

HANDLERS = {
    # Recon
    "handle_nmap": handle_nmap,
    "handle_shodan": handle_shodan,
    "handle_subdomains": handle_subdomains,
    "handle_wordpress": handle_wordpress,
    "handle_fuzz": handle_fuzz,
    
    # Exploit
    "handle_sqli": handle_sqli,
    "handle_xss": handle_xss,
    "handle_searchsploit": handle_searchsploit,
    "handle_brute": handle_brute,
    "handle_msfvenom": handle_msfvenom,
    "handle_phishing": handle_phishing,
    "handle_takeover": handle_takeover,
    
    # Network
    "handle_wifi": handle_wifi,
    "handle_wifi_dump": handle_wifi_dump,
    "handle_sniffer": handle_sniffer,
    "handle_arp": handle_arp,
    "handle_netscan": handle_netscan,
    "handle_hash": handle_hash,
    
    # OSINT
    "handle_exif": handle_exif,
    "handle_username": handle_username,
    "handle_phone": handle_phone,
    "handle_dorks": handle_dorks,
    "handle_metadata": handle_metadata,
    "handle_harvester": handle_harvester,
    
    # Reporting
    "handle_html_report": handle_html_report,
    "handle_json_report": handle_json_report,
    "handle_markdown_report": handle_markdown_report,
    
    # Special
    "handle_cortex": handle_cortex,
}
