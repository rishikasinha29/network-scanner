#!/usr/bin/env python3

from scapy.all import ARP, Ether, srp, IP, TCP, sr1
import socket
import argparse

from database import (
    initialize_database,
    insert_device,
    insert_port,
    get_scan_results
)

from risk_engine import (
    get_service,
    get_risk_level
)


COMMON_PORTS = [
    21,
    22,
    23,
    25,
    53,
    80,
    110,
    139,
    143,
    443,
    445,
    3306,
    3389,
    5432,
    5900,
    8080
]


def discover_devices(network):

    print("\n[*] Discovering devices...")
    print("[*] Network:", network)

    arp_request = ARP(pdst=network)

    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = broadcast / arp_request

    answered = srp(
        packet,
        timeout=2,
        verbose=False
    )[0]

    devices = []

    for sent, received in answered:

        ip = received.psrc
        mac = received.hwsrc

        try:
            hostname = socket.gethostbyaddr(ip)[0]

        except socket.herror:
            hostname = "Unknown"

        devices.append({
            "ip": ip,
            "mac": mac,
            "hostname": hostname
        })

    return devices


def scan_port(ip, port):

    packet = IP(dst=ip) / TCP(
        dport=port,
        flags="S"
    )

    response = sr1(
        packet,
        timeout=1,
        verbose=False
    )

    if response is None:
        return False

    if response.haslayer(TCP):

        tcp_layer = response.getlayer(TCP)

        if tcp_layer.flags == 0x12:

            return True

    return False


def scan_ports(ip):

    print(f"\n[*] Scanning ports on {ip}")

    open_ports = []

    for port in COMMON_PORTS:

        print(
            f"    Checking port {port}...",
            end="\r"
        )

        if scan_port(ip, port):

            service = get_service(port)
            risk = get_risk_level(port)

            open_ports.append({
                "port": port,
                "service": service,
                "risk": risk
            })

    print(" " * 50, end="\r")

    return open_ports


def display_results(results):

    print("\n")
    print("=" * 80)
    print("NETWORK SCAN RESULTS")
    print("=" * 80)

    current_ip = None

    for row in results:

        ip, mac, hostname, port, service, risk = row

        if ip != current_ip:

            current_ip = ip

            print("\n----------------------------------------")
            print(f"IP Address : {ip}")
            print(f"MAC Address: {mac}")
            print(f"Hostname   : {hostname}")
            print("----------------------------------------")

        if port:

            print(
                f"Port {port:<5} "
                f"Service: {service:<15} "
                f"Risk: {risk}"
            )

    print("\n" + "=" * 80)


def main():

    parser = argparse.ArgumentParser(
        description="Network Scanner using Scapy"
    )

    parser.add_argument(
        "-n",
        "--network",
        required=True,
        help="Network range e.g. 192.168.1.0/24"
    )

    args = parser.parse_args()

    initialize_database()

    devices = discover_devices(
        args.network
    )

    if not devices:

        print("\n[-] No devices discovered.")
        return

    print(
        f"\n[+] {len(devices)} device(s) discovered."
    )

    for device in devices:

        print(
            f"[+] {device['ip']} "
            f"({device['mac']})"
        )

        device_id = insert_device(
            device["ip"],
            device["mac"],
            device["hostname"]
        )

        ports = scan_ports(
            device["ip"]
        )

        for port_info in ports:

            insert_port(
                device_id,
                port_info["port"],
                port_info["service"],
                port_info["risk"]
            )

            print(
                f"    [+] Open: "
                f"{port_info['port']} "
                f"({port_info['service']}) "
                f"[{port_info['risk']}]"
            )

    results = get_scan_results()

    display_results(results)


if __name__ == "__main__":
    main()