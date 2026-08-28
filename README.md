
# 🔍 Network Scanner Using Scapy

A Python-based network scanning tool that discovers active devices on a local network, extracts IP and MAC addresses, identifies open TCP ports, assigns basic risk levels to exposed services, and stores scan results using SQLite.

This project was developed as a team project for **Project Exhibition 2**.

---

## 🚀 Features

- 🔎 Network discovery using ARP
- 🌐 IP and MAC address extraction
- 💻 Hostname resolution
- 🚪 TCP SYN-based port scanning
- 🔐 Common service identification
- ⚠️ Basic risk-level classification
- 🗄️ SQLite database integration
- 🕒 Scan results with timestamps
- 🪟 Windows support using Npcap
- ⌨️ Command-line interface

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Scapy | Network packet creation and scanning |
| SQLite | Storing scan results |
| Npcap | Packet capture support on Windows |
| Windows | Development and execution platform |

---

## 🏗️ Project Architecture

```text
                    +----------------------+
                    |      User Input      |
                    |   Network /24 Range  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |  Network Discovery   |
                    |      Scapy + ARP     |
                    +----------+-----------+
                               |
                         IP + MAC Address
                               |
                               v
                    +----------------------+
                    |     Port Scanner     |
                    |    TCP SYN / Scapy   |
                    +----------+-----------+
                               |
                          Open Ports
                               |
                               v
                    +----------------------+
                    |     Risk Engine      |
                    |  LOW / MEDIUM / HIGH |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    SQLite Database   |
                    | Devices + Port Data  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    Scan Results      |
                    |        CLI           |
                    +----------------------+
````

---

## 📂 Project Structure

```text
NetworkScanner/
│
├── scanner.py
├── database.py
├── risk_engine.py
├── requirements.txt
├── network_scanner.db
└── README.md
```

### File Description

| File                 | Description                                    |
| -------------------- | ---------------------------------------------- |
| `scanner.py`         | Main network discovery and port scanning logic |
| `database.py`        | SQLite database operations                     |
| `risk_engine.py`     | Service identification and risk classification |
| `requirements.txt`   | Python dependencies                            |
| `network_scanner.db` | Automatically generated SQLite database        |
| `README.md`          | Project documentation                          |

---

## ⚙️ How It Works

### 1. Network Discovery

The scanner uses **Scapy** to send ARP requests to the specified local network.

```text
ARP Request
     |
     v
Broadcast to Local Network
     |
     v
Active Devices Respond
     |
     v
IP Address + MAC Address
```

The scanner collects:

* IP address
* MAC address
* Hostname

The discovered information is then stored in the SQLite database.

### 2. Port Scanning

After discovering active devices, the scanner performs **TCP SYN scanning** against commonly used ports.

Example ports:

```text
21    FTP
22    SSH
23    Telnet
53    DNS
80    HTTP
443   HTTPS
445   SMB
3306  MySQL
3389  RDP
5432  PostgreSQL
5900  VNC
8080  HTTP Proxy
```

A TCP SYN-ACK response is treated as an indication that the port is open.

### 3. Risk Classification

The project uses a basic port-based risk classification system.

| Port | Service    | Risk Level |
| ---: | ---------- | ---------- |
|   21 | FTP        | HIGH       |
|   22 | SSH        | MEDIUM     |
|   23 | Telnet     | HIGH       |
|   80 | HTTP       | MEDIUM     |
|  443 | HTTPS      | LOW        |
|  445 | SMB        | HIGH       |
| 3306 | MySQL      | HIGH       |
| 3389 | RDP        | HIGH       |
| 5432 | PostgreSQL | HIGH       |
| 5900 | VNC        | HIGH       |

> **Note:** Risk levels are simplified classifications based on the exposed service/port. They do not represent a CVSS score or confirm that a vulnerability exists.

### 4. Database Storage

SQLite is used to store scan results.

#### Devices Table

```text
devices
├── id
├── ip_address
├── mac_address
├── hostname
└── scan_time
```

#### Open Ports Table

```text
open_ports
├── id
├── device_id
├── port
├── service
├── risk_level
└── scan_time
```

The `device_id` field establishes the relationship between discovered devices and their open ports.

---

## 💻 Installation — Windows

### Prerequisites

* Windows 10/11
* Python 3.x
* Npcap
* Administrator privileges
* Local network connection

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/network-scanner.git
cd network-scanner
```

### 2. Install Npcap

Scapy requires a packet-capture driver on Windows.

Download Npcap from:

[https://npcap.com/](https://npcap.com/)

During installation, enable:

```text
Install Npcap in WinPcap API-compatible Mode
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install Scapy directly:

```bash
pip install scapy
```

SQLite is included with Python and does not require a separate installation.

---

## ▶️ Usage

### Step 1: Find Your Local IP Address

Open Command Prompt:

```cmd
ipconfig
```

Example:

```text
IPv4 Address : 192.168.1.15
Subnet Mask  : 255.255.255.0
```

The local network would typically be:

```text
192.168.1.0/24
```

### Step 2: Run the Scanner

Open **Command Prompt or PowerShell as Administrator**.

```bash
python scanner.py -n 192.168.1.0/24
```

Replace the network range with your own authorized local network.

---

## 📊 Example Output

```text
[*] Discovering devices...
[*] Network: 192.168.1.0/24

[+] 4 device(s) discovered.

[+] Device Found
    IP  : 192.168.1.1
    MAC : AA:BB:CC:DD:EE:FF
    Host: router.local

[*] Scanning 192.168.1.1

    [+] Port 53 OPEN | Service: DNS | Risk: LOW
    [+] Port 80 OPEN | Service: HTTP | Risk: MEDIUM
    [+] Port 443 OPEN | Service: HTTPS | Risk: LOW

[+] Device Found
    IP  : 192.168.1.20
    MAC : 11:22:33:44:55:66
    Host: desktop

[*] Scanning 192.168.1.20

    [+] Port 445 OPEN | Service: SMB | Risk: HIGH
```

---

## 🗄️ Database

After the first scan, the application automatically creates:

```text
network_scanner.db
```

The database contains two tables:

* `devices`
* `open_ports`

Example SQL query:

```sql
SELECT * FROM devices;
```

To view open ports:

```sql
SELECT * FROM open_ports;
```

---

## 🔐 Security Considerations

This project is designed for:

* Educational purposes
* Personal networks
* Cybersecurity laboratories
* Network administration
* Authorized security testing

> ⚠️ **Only scan systems and networks for which you have explicit permission.**

The scanner performs network discovery and port scanning. It does not attempt to exploit discovered services, bypass authentication, or gain unauthorized access.

---

## ⚠️ Limitations

* Only a predefined set of commonly used ports is scanned.
* Risk levels are based on service/port heuristics.
* Does not perform CVE-based vulnerability assessment.
* Does not perform detailed service-version detection.
* Firewall rules may affect port detection.
* ARP discovery is primarily applicable to the local network.
* VPNs and network isolation can affect device discovery.
* The current version uses a command-line interface.

---

## 🚀 Future Enhancements

* [ ] PyQt5 graphical user interface
* [ ] Custom port-range scanning
* [ ] Service and version detection
* [ ] Operating-system fingerprinting
* [ ] CVE vulnerability mapping
* [ ] CVSS-based risk scoring
* [ ] Scan history dashboard
* [ ] CSV/PDF report generation
* [ ] Network topology visualization
* [ ] Real-time device monitoring
* [ ] Configurable scanning profiles
* [ ] Advanced security analytics

---

## 📚 Learning Outcomes

Through this project, we gained practical experience with:

* ARP and network discovery
* TCP/IP networking
* TCP SYN scanning
* Packet crafting using Scapy
* IP and MAC address identification
* Port and service identification
* SQLite database integration
* Python network programming
* Basic network security assessment

---

## 👩‍💻 Project Information

| Category      | Details                     |
| ------------- | --------------------------- |
| **Project**   | Network Scanner Using Scapy |
| **Date**      | April 2025                  |
| **Role**      | Developer                   |
| **Team Size** | 5 Members                   |
| **Event**     | Project Exhibition 2        |
| **Platform**  | Windows                     |
| **Language**  | Python                      |

---

## 🤝 Team Contribution

As a **Developer**, my contributions included:

* Implementing network discovery using Scapy and ARP.
* Extracting IP and MAC addresses of active hosts.
* Implementing TCP SYN-based port scanning.
* Developing service and risk-level classification.
* Integrating SQLite for persistent scan-result storage.
* Testing and integrating scanning components.

---

## 👤 Author

**Rishika Sinha**

Computer Science Engineering
VIT Bhopal University

---

## 📜 License

This project is intended for **educational and authorized security-testing purposes only**.

Use responsibly and only on networks for which you have permission to perform scanning.

```

One thing to change before committing: replace `https://github.com/your-username/network-scanner.git` with your actual GitHub repository URL.

```
