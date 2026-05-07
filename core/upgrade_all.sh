#!/bin/bash
echo "⚡ BrayoOS Maximum Upgrade..."

# Install ALL security tools
pkg install -y \
    nmap \
    hydra \
    john \
    aircrack-ng \
    tcpdump \
    wireshark-cli \
    metasploit \
    sqlmap \
    tor \
    proxychains-ng \
    netcat-openbsd \
    openssh \
    whois \
    dnsutils \
    traceroute \
    net-tools \
    wireless-tools

echo "✅ Security tools installed!"

# Install development tools
pkg install -y \
    nodejs \
    golang \
    ruby \
    php \
    rust \
    cmake \
    clang \
    make \
    gdb

echo "✅ Dev tools installed!"

# Install Python security libraries
pip install \
    scapy \
    paramiko \
    cryptography \
    pyOpenSSL \
    requests \
    beautifulsoup4 \
    selenium \
    pwntools \
    impacket \
    --break-system-packages

echo "✅ Python security libs installed!"

# Install utilities
pkg install -y \
    ffmpeg \
    imagemagick \
    poppler \
    tesseract \
    htop \
    tree \
    ranger \
    tmux \
    zsh \
    fish \
    neovim

echo "✅ Utilities installed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ BrayoOS Maximum Upgrade Done!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
