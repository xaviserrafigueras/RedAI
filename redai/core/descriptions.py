"""
Tool descriptions for the help system.
Separated from config.py to avoid circular imports.
"""

TOOL_DESCRIPTIONS = {
    "nmap": "Escáner de red para descubrir hosts y servicios abiertos. Uso: nmap -sV -sC <target>.",
    "shodan": "Motor de búsqueda de dispositivos conectados (IoT, Servidores). Requiere API Key.",
    "sqlmap": "Herramienta automática de SQL Injection. Detecta y explota vulns DB.",
    "gobuster": "Fuzzer de directorios y subdominios usando diccionarios.",
    "hashcat": "Cracker de hashes GPU-accelerated. Soporta MD5, SHA, NTLM, etc.",
    "hydra": "Cracker de fuerza bruta para protocolos (SSH, FTP, HTTP, etc.).",
    "wifite": "Auditoría automatizada de redes Wi-Fi (WEP, WPA, WPS).",
    "aircrack-ng": "Suite completa para hackear redes Wi-Fi.",
    "metasploit": "Framework de explotación con miles de exploits y payloads.",
    "nikto": "Escáner de vulnerabilidades web (misconfigs, archivos peligrosos).",
    "wpscan": "Escáner especializado en WordPress (plugins, temas, usuarios).",
    "maigret": "Rastreo de nombre de usuario en 3000+ sitios web (OSINT).",
    "phone": "Inteligencia de números telefónicos (Operadora, País, Zona Horaria).",
    "harvester": "Recolector de emails, subdominios y hosts (TheHarvester).",
    "dorks": "Generador de Google Dorks para encontrar archivos sensibles y paneles.",
    "metadata": "Extracción profunda de metadatos en documentos y archivos (PDF, DOC, IMG).",
    "wifi": "Gestión de perfiles Wi-Fi guardados y ataques de desautenticación.",
    "sniffer": "Captura y análisis de tráfico de red en tiempo real (Scapy).",
    "arp": "Ataque MITM (ARP Spoofing) para interceptar tráfico o cortar internet (Kick).",
    "dns": "DNS Spoofing para redirigir tráfico de dominios legítimos a una IP maliciosa.",
}
