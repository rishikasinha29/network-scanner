RISK_LEVELS = {
    21: ("FTP", "HIGH"),
    22: ("SSH", "MEDIUM"),
    23: ("Telnet", "HIGH"),
    25: ("SMTP", "MEDIUM"),
    53: ("DNS", "LOW"),
    80: ("HTTP", "MEDIUM"),
    110: ("POP3", "MEDIUM"),
    139: ("NetBIOS", "HIGH"),
    143: ("IMAP", "MEDIUM"),
    443: ("HTTPS", "LOW"),
    445: ("SMB", "HIGH"),
    3306: ("MySQL", "HIGH"),
    3389: ("RDP", "HIGH"),
    5432: ("PostgreSQL", "HIGH"),
    5900: ("VNC", "HIGH"),
    8080: ("HTTP-Proxy", "MEDIUM"),
}


def get_service(port):
    if port in RISK_LEVELS:
        return RISK_LEVELS[port][0]

    return "Unknown"


def get_risk_level(port):
    if port in RISK_LEVELS:
        return RISK_LEVELS[port][1]

    return "LOW"
