# RedAI - Autonomous AI Pentesting Framework
# Base image: Kali Linux (includes security tools)

FROM kalilinux/kali-rolling

# Avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install Python and essential security tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    # Build tools
    golang-go \
    git \
    build-essential \
    # Essential pentesting tools (already included)
    nmap \
    gobuster \
    dirb \
    nikto \
    whatweb \
    whois \
    dnsutils \
    sqlmap \
    wpscan \
    hydra \
    theharvester \
    # Additional tools required by RedAI
    masscan \
    netcat-traditional \
    aircrack-ng \
    exiftool \
    hashcat \
    john \
    # Network diagnostic tools (for Cortex agent)
    iproute2 \
    net-tools \
    iputils-ping \
    # Utils
    curl \
    wget \
    jq \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Go-based tools (subfinder, amass, etc.)
RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install -v github.com/owasp-amass/amass/v4/...@master && \
    mv /root/go/bin/* /usr/local/bin/ && \
    rm -rf /root/go

# Install maigret (OSINT username tool)
RUN pip3 install --no-cache-dir maigret

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for logs and data
RUN mkdir -p /app/logs /app/reports

# Environment variables (override with docker-compose or -e flag)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command - interactive mode
CMD ["python3", "main.py"]
