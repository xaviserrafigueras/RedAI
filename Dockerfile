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
    # Essential pentesting tools
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
    # Utils
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

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
