"""
Menu Configuration - Data-driven menu system for RedAI CLI
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class PromptConfig:
    """Configuration for a user prompt."""
    name: str           # Parameter name for handler
    label: str          # Display label
    default: Optional[str] = None
    choices: Optional[List[str]] = None


@dataclass
class MenuOption:
    """Configuration for a menu option."""
    id: str
    name: str
    category: str       # recon, exploit, network, osint, reporting
    handler: str        # Handler function name
    tool_key: str       # For display.tool_info()
    prompts: List[PromptConfig] = field(default_factory=list)
    requires: Optional[str] = None  # External tool requirement
    emoji: str = ""


# =============================================================================
# MENU OPTIONS - Add/modify tools here
# =============================================================================

MENU_OPTIONS: List[MenuOption] = [
    # -------------------------------------------------------------------------
    # RECON (1-9)
    # -------------------------------------------------------------------------
    MenuOption(
        id="1", name="Nmap Scanner", category="recon",
        handler="handle_nmap", tool_key="nmap",
        prompts=[PromptConfig("target", "Target IP")],
        requires="nmap"
    ),
    MenuOption(
        id="2", name="Shodan Intel", category="recon",
        handler="handle_shodan", tool_key="shodan",
        prompts=[PromptConfig("ip", "IP for Shodan")]
    ),
    MenuOption(
        id="3", name="Subdomains", category="recon",
        handler="handle_subdomains", tool_key="subdomains",
        prompts=[PromptConfig("domain", "Domain")]
    ),
    MenuOption(
        id="4", name="WordPress Scan", category="recon",
        handler="handle_wordpress", tool_key="wordpress",
        prompts=[PromptConfig("url", "WordPress URL")],
        requires="wpscan"
    ),
    MenuOption(
        id="5", name="Fuzzing Web", category="recon",
        handler="handle_fuzz", tool_key="fuzz",
        prompts=[PromptConfig("url", "Base URL")]
    ),
    
    # -------------------------------------------------------------------------
    # EXPLOIT (10-19)
    # -------------------------------------------------------------------------
    MenuOption(
        id="10", name="SQL Injection", category="exploit",
        handler="handle_sqli", tool_key="sqli",
        prompts=[PromptConfig("url", "Vulnerable URL")],
        requires="sqlmap"
    ),
    MenuOption(
        id="11", name="XSS Scanner", category="exploit",
        handler="handle_xss", tool_key="xss",
        prompts=[PromptConfig("url", "Target URL")]
    ),
    MenuOption(
        id="12", name="SearchSploit", category="exploit",
        handler="handle_searchsploit", tool_key="searchsploit",
        prompts=[PromptConfig("term", "Search Term")],
        requires="searchsploit"
    ),
    MenuOption(
        id="13", name="Brute Force", category="exploit",
        handler="handle_brute", tool_key="brute",
        prompts=[
            PromptConfig("target", "Target IP"),
            PromptConfig("user", "Username", default="root")
        ]
    ),
    MenuOption(
        id="14", name="Msfvenom Payloads", category="exploit",
        handler="handle_msfvenom", tool_key="msfvenom",
        prompts=[],
        requires="msfvenom"
    ),
    MenuOption(
        id="15", name="Phishing Templates", category="exploit",
        handler="handle_phishing", tool_key="phishing",
        prompts=[PromptConfig("template", "Template", default="google", 
                             choices=["google", "microsoft", "netflix", "paypal"])]
    ),
    MenuOption(
        id="16", name="Subdomain Takeover", category="exploit",
        handler="handle_takeover", tool_key="takeover",
        prompts=[PromptConfig("domain", "Target Subdomain")]
    ),
    
    # -------------------------------------------------------------------------
    # NETWORK (20-29)
    # -------------------------------------------------------------------------
    MenuOption(
        id="20", name="Wi-Fi Auditor", category="network",
        handler="handle_wifi", tool_key="wifi",
        prompts=[PromptConfig("interface", "Wireless Interface", default="wlan0")]
    ),
    MenuOption(
        id="21", name="Wi-Fi Dump", category="network",
        handler="handle_wifi_dump", tool_key="wifi",
        prompts=[]
    ),
    MenuOption(
        id="22", name="Network Sniffer", category="network",
        handler="handle_sniffer", tool_key="sniffer",
        prompts=[
            PromptConfig("interface", "Network Interface", default="eth0"),
            PromptConfig("count", "Packets to capture", default="50")
        ]
    ),
    MenuOption(
        id="23", name="ARP Poison", category="network",
        handler="handle_arp", tool_key="arp",
        prompts=[
            PromptConfig("target", "Target IP (Victim)"),
            PromptConfig("gateway", "Gateway IP (Router)"),
            PromptConfig("mode", "Mode", default="mitm", choices=["mitm", "kick"])
        ]
    ),
    MenuOption(
        id="24", name="Network Scanner", category="network",
        handler="handle_netscan", tool_key="nmap",
        prompts=[PromptConfig("subnet", "Subnet to scan", default="192.168.1.0/24")]
    ),
    MenuOption(
        id="25", name="Hash Cracker", category="network",
        handler="handle_hash", tool_key="hash",
        prompts=[PromptConfig("hash_str", "Hash to Crack")]
    ),
    
    # -------------------------------------------------------------------------
    # OSINT (30-39)
    # -------------------------------------------------------------------------
    MenuOption(
        id="30", name="Exif Spy", category="osint",
        handler="handle_exif", tool_key="exif",
        prompts=[PromptConfig("image_path", "Path to Image")]
    ),
    MenuOption(
        id="31", name="Username Recon", category="osint",
        handler="handle_username", tool_key="maigret",
        prompts=[PromptConfig("username", "Username")]
    ),
    MenuOption(
        id="32", name="Phone OSINT", category="osint",
        handler="handle_phone", tool_key="phone",
        prompts=[PromptConfig("number", "Phone Number (+1...)")]
    ),
    MenuOption(
        id="33", name="Google Dorks", category="osint",
        handler="handle_dorks", tool_key="dorks",
        prompts=[PromptConfig("target", "Target Domain")]
    ),
    MenuOption(
        id="34", name="Metadata FOCA", category="osint",
        handler="handle_metadata", tool_key="metadata",
        prompts=[PromptConfig("filepath", "File Path")]
    ),
    MenuOption(
        id="35", name="TheHarvester", category="osint",
        handler="handle_harvester", tool_key="harvester",
        prompts=[PromptConfig("domain", "Target Domain")]
    ),
    
    # -------------------------------------------------------------------------
    # REPORTING (40-49)
    # -------------------------------------------------------------------------
    MenuOption(
        id="40", name="HTML Report", category="reporting",
        handler="handle_html_report", tool_key="html",
        prompts=[]
    ),
    MenuOption(
        id="41", name="JSON Report", category="reporting",
        handler="handle_json_report", tool_key="json",
        prompts=[]
    ),
    MenuOption(
        id="42", name="Markdown Report", category="reporting",
        handler="handle_markdown_report", tool_key="markdown",
        prompts=[]
    ),
    
    # -------------------------------------------------------------------------
    # SPECIAL
    # -------------------------------------------------------------------------
    MenuOption(
        id="99", name="RED AI CORTEX", category="special",
        handler="handle_cortex", tool_key="agent",
        prompts=[],
        emoji="🧠"
    ),
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_option_by_id(option_id: str) -> Optional[MenuOption]:
    """Get a menu option by its ID."""
    for option in MENU_OPTIONS:
        if option.id == option_id:
            return option
    return None


def get_options_by_category(category: str) -> List[MenuOption]:
    """Get all menu options for a category."""
    return [opt for opt in MENU_OPTIONS if opt.category == category]


def get_all_categories() -> List[str]:
    """Get list of all categories in order."""
    return ["recon", "exploit", "network", "osint", "reporting"]


CATEGORY_CONFIG = {
    "recon": {"emoji": "🔍", "name": "Recon", "style": "cyan"},
    "exploit": {"emoji": "⚔️", "name": "Exploit", "style": "red"},
    "network": {"emoji": "🌐", "name": "Network", "style": "green"},
    "osint": {"emoji": "🕵️", "name": "OSINT", "style": "yellow"},
    "reporting": {"emoji": "📊", "name": "Reporting", "style": "blue"},
}
