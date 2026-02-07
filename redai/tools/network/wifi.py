"""
WiFi Audit and Password Extractor
"""

import os
import re
import shutil
import subprocess

from rich.console import Console
from rich.table import Table
from rich import box

from redai.core.display import display
from redai.core.utils import run_sudo
from redai.database.repository import save_scan


console = Console()


def wifi_audit(interface: str = "wlan0", project: str = "General", auto: bool = False):
    """Auditoría Wi-Fi automatizada (Wrapper Wifite)."""
    display.header(f"Wi-Fi Auditor: {interface}")
    
    # Auto-detect interfaces (Linux only)
    if os.path.exists("/sys/class/net"):
        available = [x for x in os.listdir("/sys/class/net") if x.startswith("wlan")]
        if available and interface == "wlan0" and "wlan0" not in available:
            display.info(f"Auto-detected interfaces: {', '.join(available)}")
    
    tool = "wifite"
    if not shutil.which(tool):
        display.warning("Wifite not found. Trying aircrack-ng fallback...")
        if not shutil.which("airmon-ng"):
            display.error("No Wi-Fi tools found (wifite or aircrack-ng). Install on Kali.")
            return
        display.info("Recommended: sudo apt install wifite")
        return
    
    # Prime sudo cache
    run_sudo(["true"], capture_output=True)
    
    # Use os.system for interactive tools
    cmd_str = f"sudo {tool} -i {interface} --kill"
    display.step(f"Launching {tool} (Interactive Mode)...")
    
    try:
        os.system(cmd_str)
    except KeyboardInterrupt:
        pass
    
    display.success("Wi-Fi Audit Finished.")
    save_scan(interface, "wifi_audit", "Audit completed", project)


def wifi_stealer(project: str = "General", auto: bool = False):
    """Extrae contraseñas de Wi-Fi guardadas (Windows & Linux)."""
    display.header("Wi-Fi Password Extractor")
    
    networks = []
    
    if os.name == 'nt':
        # Windows
        try:
            # Get all profiles
            profiles_output = subprocess.run(
                ["netsh", "wlan", "show", "profiles"],
                capture_output=True, text=True
            )
            
            profile_names = re.findall(r"All User Profile\s*:\s*(.+)", profiles_output.stdout)
            
            for name in profile_names:
                name = name.strip()
                try:
                    key_output = subprocess.run(
                        ["netsh", "wlan", "show", "profile", name, "key=clear"],
                        capture_output=True, text=True
                    )
                    
                    key_match = re.search(r"Key Content\s*:\s*(.+)", key_output.stdout)
                    password = key_match.group(1).strip() if key_match else "N/A"
                    
                    networks.append({"ssid": name, "password": password})
                except:
                    pass
                    
        except Exception as e:
            display.error(f"Windows extraction failed: {e}")
            
    else:
        # Linux
        wifi_dir = "/etc/NetworkManager/system-connections/"
        
        if os.path.exists(wifi_dir):
            try:
                for filename in os.listdir(wifi_dir):
                    filepath = os.path.join(wifi_dir, filename)
                    
                    result = run_sudo(["cat", filepath], capture_output=True)
                    content = result.stdout
                    
                    ssid = filename
                    psk_match = re.search(r"psk=(.+)", content)
                    password = psk_match.group(1) if psk_match else "N/A"
                    
                    networks.append({"ssid": ssid, "password": password})
                    
            except Exception as e:
                display.error(f"Linux extraction failed: {e}")
        else:
            display.warning("NetworkManager config not found.")
    
    # Display results
    if networks:
        table = Table(title=f"Saved Wi-Fi Networks ({len(networks)})", box=box.SIMPLE)
        table.add_column("SSID", style="cyan")
        table.add_column("Password", style="green")
        
        output_lines = []
        for net in networks:
            table.add_row(net["ssid"], net["password"])
            output_lines.append(f"{net['ssid']}: {net['password']}")
        
        console.print(table)
        
        output = "\n".join(output_lines)
        save_scan("local", "wifi_stealer", output, project)
    else:
        display.warning("No saved networks found.")
