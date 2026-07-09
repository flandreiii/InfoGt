# InfoGt - Network Reconnaissance Tool 🎯

```
╔═══════════════════════════════════╗
║         InfoGt v1.0               ║
║    Network Reconnaissance Tool    ║
║        by flandreiii              ║
╚═══════════════════════════════════╝
```

## 📋 Description

**InfoGt** is a network reconnaissance tool with a graphical interface built for **Parrot OS**. A modern wrapper for `nmap` with support for **proxychains4**, multiple scan modes, and real-time colorized output.

Perfect for:
- Penetration testing
- Network reconnaissance
- Vulnerability scanning
- Service enumeration
- Host discovery

---

## ✨ Features

- ✅ **8 Predefined Scan Modes** (Quick, Standard, Aggressive, Stealth, UDP, Vulnerability, Ping Sweep, Service)
- ✅ **Dark Theme GUI Matrix-Style** - Easy to use, professional
- ✅ **Proxychains4 Integration** - Anonymous scanning through proxy
- ✅ **Real-Time Output Streaming** - See results as they come in
- ✅ **Multi-Threaded** - Doesn't block the interface
- ✅ **Export Results** - Automatic saving to .txt file
- ✅ **Target Validation** - Supports IPs, domains, /24 ranges
- ✅ **Status Indicator** - Visualize scan progress

---

## 📸 Screenshot

IN THE FILES

```

```

---

## 🚀 Quick Installation

### System with Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install nmap proxychains4 python3-tk -y

# Clone/Download tool
git clone https://github.com/flandreiii/infog.git
cd infog

# Or direct download the file
chmod +x InfoGt_GUI.py
```

### Run

```bash
# Normal mode
python3 InfoGt_GUI.py

# With sudo (recommended for some scan modes)
sudo python3 InfoGt_GUI.py
```

---

## 📖 Usage

### 1. **Enter Target**
   - IP: `192.168.1.5`
   - Domain: `example.com`
   - Range: `10.0.0.0/24`

### 2. **Select Scan Mode**
   - **Quick** - Fast scan (top 1000 ports)
   - **Standard** - All ports + service detection
   - **Aggressive** - Intensive scan (ports, OS, services, NSE scripts)
   - **Stealth** - Slow SYN scan (avoid detection)
   - **UDP** - UDP port scanning
   - **Vulnerability** - Vulnerability detection
   - **Ping Sweep** - Discover hosts in range
   - **Service** - Detailed service enumeration

### 3. **Extra Options**
   - ✓ Check "Use Proxychains4" for routing through proxy
   - ✓ Click "Browse" to save results

### 4. **Start Scan**
   - Click "▶ START SCAN"
   - Monitor output in real-time
   - Click "⏹ STOP SCAN" to stop

---

## 🔐 Proxychains4 Setup (Optional)

For anonymous scanning through SOCKS proxy:

### 1. Edit config
```bash
sudo nano /etc/proxychains4.conf
```

### 2. Disable dynamic_chain
```bash
# dynamic_chain    # comment with #
strict_chain       # uncomment
```

### 3. Add proxies (at end)
```bash
# SOCKS5 proxy (local)
socks5 127.0.0.1 9050

# Or SOCKS4
socks4 127.0.0.1 1080

# Or HTTP proxy
http 127.0.0.1 8080
```

### 4. Test
```bash
proxychains4 curl ifconfig.me
```

### 5. Check "Use Proxychains4" in tool

---

## 💻 Quick Commands

```bash
# Fast scan on local network
python3 InfoGt_GUI.py
# → Select "Quick" mode + "192.168.1.0/24"

# Aggressive scan with saving
python3 InfoGt_GUI.py
# → Select "Aggressive" + "Browse" for output file

# Scan through proxy
python3 InfoGt_GUI.py
# → Check "Use Proxychains4" + select scan mode

# Vulnerability scan
python3 InfoGt_GUI.py
# → Select "Vulnerability Scan"
```

---

## 🛠️ Scan Modes Detailed

| Mode | Purpose | Time |
|------|---------|------|
| **Quick** | Fast reconnaissance | 30s-5m |
| **Standard** | Port enumeration + services | 5m-30m |
| **Aggressive** | Deep scan + scripts | 30m-2h |
| **Stealth** | IDS/IPS evasion | 2h-6h |
| **UDP** | UDP port discovery | 10m-1h |
| **Vulnerability** | CVE detection | 5m-30m |
| **Ping Sweep** | Host discovery | 30s-5m |
| **Service** | Detailed service info | 5m-1h |

---

## 📋 Systems

- ✅ **Parrot OS** - Tested
- ✅ **Kali Linux** - Compatible
- ✅ **Debian/Ubuntu** - Compatible
- ✅ **Arch Linux** - Compatible

Any Linux distribution with `nmap`, `proxychains4`, and `python3-tk`.

---

## ⚙️ Advanced Configuration

### Custom Nmap Scripts

In `InfoGt_GUI.py`, around lines 280-290, you can modify commands:

```python
scan_commands = {
    'vuln': ["-p-", "-sV", "-sC", "--script=vuln,smb-enum-*"],  # Add scripts
}
```

### Custom Timeout

Edit timeout (default 1 hour):
```python
process = subprocess.Popen(cmd, ..., timeout=3600)  # Edit 3600 = 1 hour
```

---

## 🐛 Troubleshooting

### Error: "command not found: nmap"
```bash
sudo apt install nmap
```

### Error: "No module named 'tkinter'"
```bash
sudo apt install python3-tk
```

### Error: "sudo: no such file or directory"
```bash
sudo visudo
# Verify PATH includes /usr/bin
```

### Proxychains4 not working
```bash
# Check configuration
grep -v "^#\|^$" /etc/proxychains4.conf

# Test proxy
proxychains4 curl ifconfig.me
```

### Scan gets stuck
- Increase timeout in code
- Reduce intensity (Stealth instead of Aggressive)
- Check connection

---

## 📝 Usage Examples

### Scenario 1: Quick scan on local network
```
Target: 192.168.1.0/24
Mode: Quick
Proxychains4: OFF
Output: (none)
Result: ~2 minutes, top 1000 ports
```

### Scenario 2: Vulnerability assessment with saving
```
Target: 10.0.0.50
Mode: Vulnerability Scan
Proxychains4: OFF
Output: ~/results/assessment.txt
Result: ~15 minutes, CVE detection
```

### Scenario 3: Aggressive scan anonymous
```
Target: example.com
Mode: Aggressive
Proxychains4: ON (with Tor/VPN)
Output: ~/results/aggressive.txt
Result: ~1 HOUR, deep enumeration
```

---

## 🎨 Customization

Edit colors in `InfoGt_GUI.py`:

```python
self.colors = {
    'green': '#00ff00',    # Change to #ffff00 for yellow
    'red': '#ff0000',
    'yellow': '#ffff00',
    'blue': '#00aaff',
}
```

---

## 📜 License

Free for personal and educational use.

---

## 🤝 Support & Donate

If this tool helps you, consider a small donation:

### ☕ [Buy Me A Coffee](https://buymeacoffee.com/flandreiii)

Support me for:
- Bug fixes
- Feature requests
- New scan modes
- Custom integrations

---

## 🔄 Updates & Versions

**v1.0** (Current)
- ✅ GUI interface
- ✅ 8 scan modes
- ✅ Proxychains4 integration
- ✅ Real-time output
- ✅ Export results

**v1.1** (Upcoming)
- 🔜 Custom scan profiles
- 🔜 Scan scheduling
- 🔜 Result comparisons
- 🔜 Advanced filtering

---

## 👨‍💻 Author

**flandreiii**  
*Cybersecurity Tool Developer*

---

## #️⃣ Hashtags

`#InfoGt` `#NmapGUI` `#Reconnaissance` `#NetworkScanning` `#Nmap` `#Proxychains4` `#PenetrationTesting` `#Hacking` `#CyberSecurity` `#ParrotOS` `#KaliLinux` `#InfoSec` `#RedTeam` `#EthicalHacking` `#Tools` `#OpenSource` `#Python` `#Tkinter` `#SecurityTools` `#NetworkSecurityTools`

---

## ⚠️ Disclaimer

**LEGAL NOTICE:**
- Use InfoGt ONLY for authorized purposes
- Do NOT use on systems without permission
- Author is NOT responsible for misuse
- Respect laws in your country

---

## 📞 Contact

**Report bugs:** DM on social media  
**Feature requests:** Comment in GitHub issues  
**Support:** [Buy Me A Coffee](https://buymeacoffee.com/flandreiii)

---

```
┌─────────────────────────────────────┐
│   Made with ❤️ by flandreiii        │
│   © 2026 - InfoGt v1.0              │
└─────────────────────────────────────┘
```

**Happy scanning! 🎯**
