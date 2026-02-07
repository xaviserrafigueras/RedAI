# 🔴 RedAI

**Automated Pentesting CLI with AI** - A modular security toolkit for Kali Linux.

## ⚡ Features

- 🔍 **Recon**: Nmap, Shodan, Subdomains, WordPress scanning
- ⚔️ **Exploit**: SQLi, XSS, Brute Force, Hash Cracking
- 🕵️ **OSINT**: Username search, Phone lookup, Email breach, Metadata extraction
- 🛠️ **Network**: WiFi audit, ARP spoofing, Packet sniffing
- 🤖 **AI Agent**: Autonomous pentesting with GPT-4 powered Cortex

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/RedAI.git
cd RedAI

# Create virtual environment (required on Kali Linux)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY
```

## 🚀 Usage

```bash
# Interactive menu
python main.py

# Direct commands
python main.py scan 192.168.1.1
python main.py dorks example.com
python main.py --help
```

## 📁 Project Structure

```
redai/
├── ai/          # AI agents (Cortex, HiveMind)
├── core/        # Display utilities
├── database/    # SQLite persistence
└── tools/       # Security tools
    ├── recon/   # Nmap, Shodan, Fuzzing
    ├── osint/   # Username, Phone, Email
    ├── exploit/ # SQLi, XSS, Bruteforce
    ├── network/ # WiFi, ARP, Sniffer
    └── reporting/ # HTML reports
```

## ⚠️ Disclaimer

**For authorized security testing only.** The developers are not responsible for misuse.

## 📄 License

MIT
