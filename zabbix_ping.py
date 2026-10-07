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

__version__ = "0.1.0"
__author__ = "Alexander Ivanov"
__license__ = "MIT"

import sys
from argparse import ArgumentParser, Namespace

from ping3 import ping


def parse_args() -> Namespace:
    parser = ArgumentParser(
        prog='zabbix_ping.py',
        description='ICMP ping для Zabbix Agent (Windows). Возвращает RTT в мс, -1 при таймауте или -2 при неудаче.',
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
    rtt = ping(args.host, timeout=args.timeout, unit='ms')

    if rtt is None:
        print("-1")
        return 1
    elif rtt is False:
        print("-2")
        return 2
    else:
        print(f'{rtt:.3f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
