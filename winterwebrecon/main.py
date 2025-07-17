#!/usr/bin/env python3

import requests
import argparse
import os
import sys
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init
import concurrent.futures
import socket

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣆⠀⠀⠀⠀⠀⠀⠀⠀⡄⣤⡤⣤⣀⡄⣄⡀⡤⠀⠀⠀⠀⠀⡹⣏⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠣⡠⠀⠀⢠⢠⠲⠟⠛⠉⠙⠙⠙⠖⡭⠋⡝⢶⡄⣤⣄⣀⠦⡅⠱⠙⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠧⠀⠀⠉⠑⣖⠗⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢣⡁⠋⣁⠀⠀⠀⠀⢑⢆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⡇⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢂⣎⢚⡀⡄⠀⠁⣐⢄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣍⠀⡀⡇⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢑⡦⣄⠀⠀⡈⡈⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠷⣂⢼⠑⡖⠊⠉⠁⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⣤⠀⠀⠀⠀⠀⢥⣷⡆⢠⡅⡼⢃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡿⠀⢇⠀⠴⠒⠂⠐⠢⣄⠀⠀⠀⠀⠀⠀⣯⠆⠀⠀⠀⠀⣅⣯⢶⠿⠡⠂⠄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⢡⠀⡉⠀⠀⠀⠀⠑⠀⠀⠀⠀⠀⢈⡫⠀⠀⠀⠀⠀⣳⣿⡷⠋⠂⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡄⢸⠄⠙⠋⠉⠀⢀⢍⠀⠀⠀⠀⠀⣹⡏⠀⠀⠀⠀⠀⣇⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣀⢄⠠⡀⡀⠀⠀⠀⢗⢜⠑⠒⠒⠒⠒⠚⠒⠀⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⣠⡟⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡘⠅⠆⠓⠑⠑⠨⠔⡄⠀⠀⢯⣀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢠⢐⡴⢏⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠟⠉⠀⠀⠀⠀⠀⠀⠀⠊⣃⡀⠀⠈⡱⢇⣤⣀⡀⢀⡀⣀⣀⣀⣢⡒⡒⣜⢺⣖⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠢⡄⠀⢄⣠⢤⠬⣘⡷⠿⠛⠛⠓⠺⠫⠻⠙⠐⠈⠣⠢⣴⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣠⠤⠅⡢⠢⠦⢤⣤⠀⠀⠀⠀⠰⡘⠹⠛⡷⡤⣀⡀⠀⠤⠂⡐⠈⢁⢀⡀⠀⠤⣴⣄⠓⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡏⠀⠁⠀⠀⠀⠘⠎⠀⠀⠀⠀⢐⢒⠀⠀⢀⡚⠟⢆⡀⠀⠀⠀⠀⠀⠀⠀⠑⠋⢫⡿⠰⡂⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠂⡐⢀⠀⠀⠀⡘⠀⠀⠀⠀⠀⠖⠐⠀⠰⢗⡠⡐⣸⣗⡒⠰⢐⠖⠒⡒⠒⢻⠿⣋⢿⠙⠙⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠠⠢⡀⢤⠁⠀⠀⠀⠀⡰⠠⠁⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠸⠦⠁⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠛⠃⠀⠀⠀⠀⣑⠃⠁⠀⠀⠀⠀⠀⠀⠨⠇⠀⠀⠀⠀⠀⠀⠀⠐⡟⠀⠡⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⡋⠀⠀⠀⠀⠀⠀⠀⠀⠅⡂⠀⠀⠀⠀⠀⠀⠀⠠⣉⠀⠀⠈⠅⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢇⡃⠀⠀⠀⠀⠀⠀⠀⠀⠫⠀⠀⠀⠀⠀⠀⠀⠀⠀⣆⠀⠀⠀⠀⠑⠱⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⡹⡀⡀⠀⠀⠀⠀⠀⠐⠧⠀⠀⠀⠀⠀⠀⠀⠀⠐⡔⢠⡀⠀⢠⠶⠶⡺⣛⡷⠦⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠢⡌⡈⠀⠁⠈⢵⡊⠀⠀⠀⠀⠀⠀⠀⠀⢀⡭⠀⢑⠀⠈⣊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠘⠪⠗⡮⡇⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⠂⠀⢧⡀⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
╔╗╔╗╔╗╔══╗╔═╗ ╔╗╔════╗╔═══╗╔═══╗    ╔╗╔╗╔╗╔═══╗╔══╗     ╔═══╗╔═══╗╔═══╗╔═══╗╔═╗ ╔╗
║║║║║║╚╣╠╝║║╚╗║║║╔╗╔╗║║╔══╝║╔═╗║    ║║║║║║║╔══╝║╔╗║     ║╔═╗║║╔══╝║╔═╗║║╔═╗║║║╚╗║║
║║║║║║ ║║ ║╔╗╚╝║╚╝║║╚╝║╚══╗║╚═╝║    ║║║║║║║╚══╗║╚╝╚╗    ║╚═╝║║╚══╗║║ ╚╝║║ ║║║╔╗╚╝║
║╚╝╚╝║ ║║ ║║╚╗║║  ║║  ║╔══╝║╔╗╔╝    ║╚╝╚╝║║╔══╝║╔═╗║    ║╔╗╔╝║╔══╝║║ ╔╗║║ ║║║║╚╗║║
╚╗╔╗╔╝╔╣╠╗║║ ║║║ ╔╝╚╗ ║╚══╗║║║╚╗    ╚╗╔╗╔╝║╚══╗║╚═╝║    ║║║╚╗║╚══╗║╚═╝║║╚═╝║║║ ║║║
 ╚╝╚╝ ╚══╝╚╝ ╚═╝ ╚══╝ ╚═══╝╚╝╚═╝     ╚╝╚╝ ╚═══╝╚═══╝    ╚╝╚═╝╚═══╝╚═══╝╚═══╝╚╝ ╚═╝

Usage: wwtool [http://target.com] [OPTIONS]
Use -h or --help to see available options.
{Style.RESET_ALL}"""

COMMON_PATHS = [
    'admin', 'login', 'dashboard', 'config', '.git', 'backup', 'phpmyadmin',
    'uploads', 'register', 'user', 'signin', 'signup', 'wp-admin', 'robots.txt'
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (WinterWebRecon by Alvaro)"
}

def resolve_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"{Fore.LIGHTYELLOW_EX}[+] IP Address: {ip}")
    except Exception as e:
        print(f"{Fore.RED}[-] Could not resolve IP: {e}")

def check_domain(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        print(f"{Fore.GREEN}[+] Domain responded with status {res.status_code}")
        return True
    except requests.RequestException as e:
        print(f"{Fore.RED}[-] Error connecting to {url}: {e}")
        return False

def get_headers(url):
    try:
        res = requests.get(url, headers=HEADERS)
        print(f"{Fore.CYAN}[i] Headers:")
        for key, value in res.headers.items():
            print(f"    {key}: {value}")
    except:
        print(f"{Fore.RED}[-] Failed to get headers.")

def check_robots(url):
    robots_url = urljoin(url, "/robots.txt")
    try:
        res = requests.get(robots_url, headers=HEADERS)
        if res.status_code == 200:
            print(f"{Fore.YELLOW}[+] Found robots.txt:")
            print(res.text)
        else:
            print(f"{Fore.RED}[-] robots.txt not found.")
    except:
        print(f"{Fore.RED}[-] Failed to fetch robots.txt")

def check_sitemap(url):
    sitemap_url = urljoin(url, "/sitemap.xml")
    try:
        res = requests.get(sitemap_url, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            print(f"{Fore.YELLOW}[+] Found sitemap.xml:")
            print(res.text[:1000] + "..." if len(res.text) > 1000 else res.text)
        else:
            print(f"{Fore.RED}[-] sitemap.xml not found.")
    except requests.Timeout:
        print(f"{Fore.RED}[-] sitemap.xml request timed out.")
    except requests.RequestException as e:
        print(f"{Fore.RED}[-] Failed to fetch sitemap.xml: {e}")

def brute_force_paths(base_url):
    print(f"{Fore.MAGENTA}[i] Bruteforcing common paths...")
    def check_path(path):
        full_url = urljoin(base_url, path)
        try:
            r = requests.get(full_url, headers=HEADERS, timeout=3)
            if r.status_code < 400:
                return f"[+] {full_url} --> {r.status_code}"
        except:
            pass
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_path, COMMON_PATHS))

    for res in results:
        if res:
            print(Fore.GREEN + res)

def detect_tech(url):
    try:
        res = requests.get(url, headers=HEADERS)
        techs = []
        headers = res.headers
        if "server" in headers:
            techs.append(f"Server: {headers['server']}")
        if "x-powered-by" in headers:
            techs.append(f"X-Powered-By: {headers['x-powered-by']}")
        if techs:
            print(f"{Fore.CYAN}[+] Possible technologies detected:")
            for t in techs:
                print("    " + t)
        else:
            print(f"{Fore.YELLOW}[i] No obvious technologies detected in headers.")
    except:
        print(f"{Fore.RED}[-] Could not detect technologies.")

def enumerate_subdomains(domain):
    crt_url = f"https://crt.sh/?q=%25.{domain}&output=json"
    print(f"{Fore.MAGENTA}[i] Enumerating subdomains via crt.sh...")
    try:
        r = requests.get(crt_url, timeout=10)
        if r.status_code == 200:
            subdomains = set()
            for entry in r.json():
                name_value = entry.get("name_value")
                if name_value:
                    for sub in name_value.split("\n"):
                        if domain in sub:
                            subdomains.add(sub.strip())
            if subdomains:
                print(f"{Fore.GREEN}[+] Found {len(subdomains)} subdomains:")
                for sd in sorted(subdomains):
                    print("   - " + sd)
            else:
                print(f"{Fore.YELLOW}[i] No subdomains found.")
        else:
            print(f"{Fore.RED}[-] crt.sh returned an error.")
    except Exception as e:
        print(f"{Fore.RED}[-] Error during subdomain enumeration: {e}")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description="Winter Web Recon - Advanced Web Reconnaissance Tool")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., https://example.com)")
    parser.add_argument("--sitemap", action="store_true", help="Attempt to fetch sitemap.xml")
    parser.add_argument("--brute", action="store_true", help="Bruteforce common web paths")
    parser.add_argument("-t", "--tech", action="store_true", help="Detect technologies from HTTP headers")
    parser.add_argument("-sD", "--subdomains", action="store_true", help="Enumerate subdomains via crt.sh")
    args = parser.parse_args()

    if not args.url.startswith("http"):
        print(f"{Fore.RED}[-] Please include http:// or https:// in the URL")
        sys.exit(1)

    parsed_url = urlparse(args.url)
    domain = parsed_url.netloc

    print(f"{Fore.BLUE}[***] Starting recon on {args.url}\n")

    resolve_ip(domain)

    if not check_domain(args.url):
        sys.exit(1)

    get_headers(args.url)
    check_robots(args.url)

    if args.sitemap:
        check_sitemap(args.url)
    
    if args.brute:
        brute_force_paths(args.url)

    if args.tech:
        detect_tech(args.url)

    if args.subdomains:
        enumerate_subdomains(domain)

    print(f"\n{Style.BRIGHT}{Fore.GREEN}[✓] Recon complete!")

if __name__ == "__main__":
    main()
