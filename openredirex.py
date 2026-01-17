#!/usr/bin/env python3

import asyncio
import aiohttp
import argparse
import sys
import os
import random
import time
import shutil
import re
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from typing import List
from tqdm import tqdm

class Colors:
    MINT     = '\033[38;5;121m'
    SKY      = '\033[38;5;117m'
    GOLD     = '\033[38;5;222m'
    CORAL    = '\033[38;5;210m'
    LAVENDER = '\033[38;5;183m'
    SILVER   = '\033[38;5;249m'
    SLATE    = '\033[38;5;241m'
    BOLD     = '\033[1m'
    ENDC     = '\033[0m'

def get_banner():
    term_width = shutil.get_terminal_size().columns
    banner_lines = [
        "┏━┓┏━┓┏━╸┏┓╻┏━┓┏━╸╺┳┓╻┏━┓┏━╸╻ ╻",
        "┃ ┃┣━┛┣╸ ┃┗┫┣┳┛┣╸  ┃┃┃┣┳┛┣╸ ┏╋┛",
        "┗━┛╹  ┗━╸╹ ╹╹┗╸┗━╸╺┻┛╹╹┗╸┗━╸╹ ╹"
    ]
    dev_line = "DEVELOPED BY INTELEON404 | VERSION OR v1.9"
    tag_line = "“ADVANCED OPENREDIREX FINDER”"
    
    output = ""
    for line in banner_lines:
        output += f"{Colors.MINT}{line.center(term_width)}{Colors.ENDC}\n"
    output += f"{Colors.LAVENDER}{dev_line.center(term_width)}{Colors.ENDC}\n"
    output += f"{Colors.SKY}{tag_line.center(term_width)}{Colors.ENDC}\n"
    return output

class RedirexHunter:
    def __init__(self, args):
        self.args = args
        self.found_count = 0
        self.total_scanned = 0
        self.start_time = time.time()
        self.user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]

    async def load_payloads(self) -> List[str]:
        if not self.args.payloads or not os.path.exists(self.args.payloads):
            print(f"\n{Colors.CORAL}[!] ERROR: Payload file required (-p file.txt){Colors.ENDC}")
            sys.exit(1)
        with open(self.args.payloads, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def prepare_urls(self, raw_source) -> List[str]:
        urls = []
        seen = set()
        for line in raw_source:
            url = line.strip()
            if not url: continue
            if not url.startswith(('http://', 'https://')): url = 'https://' + url
            parsed = urlparse(url)
            params = parse_qsl(parsed.query)
            if not params:
                urls.append(url.rstrip('/') + f"?redirect={self.args.keyword}")
            else:
                for i in range(len(params)):
                    new_params = [(k, self.args.keyword if idx == i else v) for idx, (k, v) in enumerate(params)]
                    fuzzed_url = urlunparse(parsed._replace(query=urlencode(new_params)))
                    if fuzzed_url not in seen:
                        urls.append(fuzzed_url); seen.add(fuzzed_url)
        return urls

    async def scan_url(self, semaphore, session, url, payloads, pbar):
        async with semaphore:
            for payload in payloads:
                test_url = url.replace(self.args.keyword, payload)
                self.total_scanned += 1
                try:
                    async with session.get(test_url, allow_redirects=True, timeout=self.args.timeout, 
                                         headers={"User-Agent": random.choice(self.user_agents)}, proxy=self.args.proxy) as response:
                        if response.history:
                            final_dest = str(response.url)
                            if self.args.verify.lower() in final_dest.lower():
                                self.found_count += 1
                                if not self.args.silent:
                                    tqdm.write(f"{Colors.BOLD}{Colors.MINT}[FOUND]{Colors.ENDC} {Colors.SILVER}{test_url}{Colors.ENDC} {Colors.SKY}→{Colors.ENDC} {Colors.GOLD}{final_dest}{Colors.ENDC}")
                                if self.args.output:
                                    with open(self.args.output, 'a') as f: f.write(f"{test_url} | {final_dest}\n")
                            elif self.args.all and not self.args.silent:
                                tqdm.write(f"{Colors.SKY}[INFO]{Colors.ENDC} {Colors.SLATE}{test_url} redirected elsewhere.{Colors.ENDC}")
                        elif self.args.all and not self.args.silent:
                            tqdm.write(f"{Colors.SKY}[INFO]{Colors.ENDC} {Colors.SLATE}{test_url} returned {response.status}.{Colors.ENDC}")
                except Exception:
                    if self.args.all and not self.args.silent:
                        tqdm.write(f"{Colors.CORAL}[ERR]{Colors.ENDC} {Colors.SLATE}Connection failed: {test_url}{Colors.ENDC}")
                
                if pbar: 
                    pbar.set_postfix({"found": self.found_count}, refresh=True)
                    pbar.update()

    async def run(self):
        payloads = await self.load_payloads()
        if self.args.url: raw_source = [self.args.url]
        elif self.args.input: raw_source = open(self.args.input)
        else: raw_source = sys.stdin if not sys.stdin.isatty() else []
        targets = self.prepare_urls(raw_source)
        if hasattr(raw_source, 'close'): raw_source.close()
        
        if not self.args.silent:
            print(f"{Colors.SKY}[*] Initializing: {len(targets)} endpoints | {len(payloads)} payloads{Colors.ENDC}")

        conn = aiohttp.TCPConnector(limit_per_host=20, ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            semaphore = asyncio.Semaphore(self.args.concurrency)
            total_reqs = len(targets) * len(payloads)
            
            with tqdm(total=total_reqs, desc=f"{Colors.LAVENDER}Hunting{Colors.ENDC}", unit='req', 
                      bar_format='{l_bar}{bar:20}{r_bar}', colour='cyan', disable=self.args.silent) as pbar:
                await asyncio.gather(*[self.scan_url(semaphore, session, u, payloads, pbar) for u in targets])

        if not self.args.silent:
            duration = round(time.time() - self.start_time, 2)
            print(f"\n{Colors.BOLD}{Colors.GOLD}» SCAN SUMMARY{Colors.ENDC}")
            print(f"{Colors.GOLD}├─ {Colors.SILVER}DURATION: {duration}s{Colors.ENDC}")
            print(f"{Colors.GOLD}├─ {Colors.SILVER}TOTAL REQUESTS: {self.total_scanned}{Colors.ENDC}")
            print(f"{Colors.GOLD}╰─ {Colors.SILVER}VULNERABILITIES FOUND: {Colors.MINT}{self.found_count}{Colors.ENDC}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenRedireX - v1.9 Left-Align Branch Summary")
    parser.add_argument('-u', '--url', help='Target URL')
    parser.add_argument('-i', '--input', help='Input List')
    parser.add_argument('-p', '--payloads', help='Payload File', required=True)
    parser.add_argument('-k', '--keyword', help='Keyword', default="FUZZ")
    parser.add_argument('-c', '--concurrency', help='Threads', type=int, default=100)
    parser.add_argument('-v', '--verify', help='Verify Domain', default="google.com")
    parser.add_argument('-o', '--output', help='Save Findings')
    parser.add_argument('-t', '--timeout', help='Timeout', type=int, default=10)
    parser.add_argument('-s', '--silent', help='Silent Mode', action='store_true')
    parser.add_argument('-a', '--all', help='Show all results (INFO for no vulnerability)', action='store_true')
    parser.add_argument('--proxy', help='Proxy URL')
    
    args = parser.parse_args()
    if not args.silent: print(get_banner())
    try: asyncio.run(RedirexHunter(args).run())
    except KeyboardInterrupt: pass
