#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zabbix_ping.py — ICMP ping for Zabbix Agent (Windows).

Copyright (c) 2026 Alexander Ivanov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__version__ = "0.2.0"
__author__ = "Alexander Ivanov"
__license__ = "MIT"

import os
import socket
import struct
import sys
import time
from typing import Union
from argparse import ArgumentParser, Namespace


def calculate_checksum(data):
    if len(data) % 2:
        data += b'\x00'

    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += checksum >> 16
    return ~checksum & 0xffff


def ping(host, timeout) -> Union[float, None, str]:
    try:
        dest_addr = socket.gethostbyname(host)
    except socket.gaierror as e:
        return f"Ошибка разрешения имени хоста '{host}': {e}"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError as e:
        return f"Ошибка отсутствия права администратора для создания raw socket: {e}"
    except OSError as e:
        return f"Ошибка при создании socket: {e}"

    sock.settimeout(timeout)

    icmp_type = 8
    icmp_code = 0
    icmp_checksum = 0
    icmp_id = os.getpid() & 0xFFFF
    icmp_seq = 1

    header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)

    data = struct.pack('!d', time.time())

    icmp_checksum = calculate_checksum(header + data)

    header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)

    packet = header + data
    start_time = time.perf_counter()

    try:
        sock.sendto(packet, (dest_addr, 0))
    except socket.error as e:
        sock.close()
        return f"Ошибка при отправке пакета: {e}"

    try:
        while True:
            recv_packet, addr = sock.recvfrom(1024)
            end_time = time.perf_counter()

            if sys.platform == 'win32':
                ip_header_len = (recv_packet[0] & 0x0f) * 4
                icmp_header = recv_packet[ip_header_len:ip_header_len + 8]
            else:
                icmp_header = recv_packet[:8]

            recv_type, recv_code, recv_checksum, recv_id, recv_seq = struct.unpack('!BBHHH', icmp_header)

            if recv_type == 0 and recv_id == icmp_id:
                elapsed_ms = (end_time - start_time) * 1000
                return elapsed_ms

    except socket.timeout:
        return None
    except Exception as e:
        return f"Ошибка при получении ответа: {e}"
    finally:
        sock.close()


def parse_args() -> Namespace:
    parser = ArgumentParser(
        prog='zabbix_ping.py',
        description='ICMP ping для Zabbix Agent (Windows). Возвращает RTT в мс, -1 при таймауте или сообщение ошибке.',
        add_help=True,
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}',
        help='Показать версию и выйти',
    )
    parser.add_argument(
        'host',
        help='Хост или IP-адрес для проверки',
    )
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=4,
        help='Таймаут одной попытки в секундах (по умолчанию: 4 секунды, как в стандартном ping)',
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rtt = ping(args.host, timeout=args.timeout)

    if rtt is None:
        print("-1")
        return 1
    elif isinstance(rtt, str):
        print(rtt, file=sys.stderr)
        return 2
    else:
        print(f'{rtt:.3f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
