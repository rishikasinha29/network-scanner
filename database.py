import sqlite3
from datetime import datetime


DB_NAME = "network_scanner.db"


def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            mac_address TEXT,
            hostname TEXT,
            scan_time TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS open_ports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER,
            port INTEGER,
            service TEXT,
            risk_level TEXT,
            scan_time TEXT NOT NULL,
            FOREIGN KEY(device_id) REFERENCES devices(id)
        )
    """)

    connection.commit()
    connection.close()


def insert_device(ip, mac, hostname):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO devices
        (ip_address, mac_address, hostname, scan_time)
        VALUES (?, ?, ?, ?)
    """, (ip, mac, hostname, scan_time))

    device_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return device_id


def insert_port(device_id, port, service, risk_level):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO open_ports
        (device_id, port, service, risk_level, scan_time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        device_id,
        port,
        service,
        risk_level,
        scan_time
    ))

    connection.commit()
    connection.close()


def get_scan_results():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            devices.ip_address,
            devices.mac_address,
            devices.hostname,
            open_ports.port,
            open_ports.service,
            open_ports.risk_level
        FROM devices
        LEFT JOIN open_ports
        ON devices.id = open_ports.device_id
        ORDER BY devices.ip_address
    """)

    results = cursor.fetchall()

    connection.close()

    return results