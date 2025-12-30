#!/usr/bin/env python3
import os
import time
import sys
import getpass
import socket
import subprocess
import urllib.request
import urllib.parse
import re
import concurrent.futures
import threading
import platform
import uuid 
import hashlib
import json
from datetime import datetime

# --- THIRD PARTY LIBS ---
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.live import Live
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.layout import Layout
    from rich.theme import Theme
except ImportError:
    print("CRITICAL ERROR: 'rich' library not found. Run: pip install rich")
    sys.exit(1)

# --- CONFIGURATION & AESTHETICS ---
# THEME: Deep Blue/Cyan (Project Shodan/Ghost Protocol)
ghost_theme = Theme({
    "info": "cyan",
    "warning": "bold yellow",
    "danger": "bold red",
    "sacred": "bold blue italic",
    "protocol": "bold cyan",
    "input": "bold white",
    "grey": "dim white"
})

console = Console(theme=ghost_theme)
print_lock = threading.Lock()

# --- UTILITIES ---

def get_mac():
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))

def scan_port(target_ip, port, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            with print_lock:
                open_ports.append(port)
        sock.close()
    except:
        pass

# --- MODULES ---

def module_archive_mission():
    mission = console.input("[bold blue]ENTER OBJECTIVE: [/bold blue]")
    if not mission: mission = "routine_maintenance"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"{timestamp} | {mission}"
    console.print(Panel(log_entry, title="[bold cyan]STAGING ENTRY[/bold cyan]", border_style="blue"))
    
    confirm = console.input("[grey]COMMIT TO DISK? [Y/n]: [/grey]").lower()
    if confirm != "n":
        with open("mission_log.txt", "a") as f:
            f.write(log_entry + "\n")
        console.print("[bold green][+] MISSION LOGGED.[/bold green]")
    else:
        console.print("[bold red][-] ENTRY DISCARDED.[/bold red]")

def module_ping():
    target = console.input("[bold blue]TARGET IP/DOMAIN: [/bold blue]") or "google.com"
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    console.print(f"[grey]Pinging {target}...[/grey]")
    subprocess.run(["ping", param, "2", target])

def module_port_scanner():
    target = console.input("[bold blue]TARGET DOMAIN: [/bold blue]") or "google.com"
    try:
        target_ip = socket.gethostbyname(target)
        console.print(f"[bold cyan]TARGET LOCKED: {target_ip}[/bold cyan]")
        
        open_ports = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task(f"[cyan]Scanning Ports 1-1024...", total=1024)
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(scan_port, target_ip, port, open_ports) for port in range(1, 1025)]
                for _ in concurrent.futures.as_completed(futures):
                    progress.advance(task)
        
        if open_ports:
            table = Table(title=f"OPEN PORTS: {target}", border_style="red")
            table.add_column("Port", style="red")
            table.add_column("Status", style="bold red")
            for p in sorted(open_ports):
                table.add_row(str(p), "OPEN / VULNERABLE")
            console.print(table)
        else:
            console.print("[bold green]NO OPEN PORTS DETECTED.[/bold green]")

    except socket.gaierror:
        console.print("[bold red]ERROR: HOST RESOLUTION FAILED.[/bold red]")

def module_page_title():
    url = console.input("[bold blue]TARGET URL: [/bold blue]") or "https://www.amazon.com"
    if not url.startswith("http"): url = "https://" + url
    
    with console.status(f"[cyan]Intercepting Signal: {url}...[/cyan]"):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                html = response.read().decode('utf-8', errors='ignore')
                pattern = re.search('<title>(.*?)</title>', html, flags=re.IGNORECASE)
                if pattern:
                    console.print(Panel(f"[bold white]{pattern.group(1).strip()}[/bold white]", title="PAGE TITLE", border_style="green"))
                else:
                    console.print("[warning]NO TITLE SIGNAL FOUND.[/warning]")
        except Exception as e:
            console.print(f"[danger]CONNECTION FAILED: {e}[/danger]")

def module_system_recon():
    console.print("[bold blue]GATHERING LOCAL TELEMETRY...[/bold blue]")
    
    table = Table(show_header=False, box=None)
    table.add_row("[cyan]OS TYPE:[/cyan]", f"{platform.system()} {platform.release()}")
    table.add_row("[cyan]KERNEL:[/cyan]", platform.version())
    table.add_row("[cyan]HOSTNAME:[/cyan]", socket.gethostname())
    table.add_row("[cyan]MAC ADDR:[/cyan]", get_mac())
    
    try:
        external_ip = urllib.request.urlopen('https://api.ipify.org', timeout=3).read().decode('utf8')
        table.add_row("[cyan]PUBLIC IP:[/cyan]", f"[bold red]{external_ip}[/bold red]")
    except:
        table.add_row("[cyan]PUBLIC IP:[/cyan]", "[dim]UNAVAILABLE[/dim]")

    console.print(Panel(table, title="SYSTEM RECON", border_style="blue"))

def module_read_diary():
    console.print("[bold blue]--- ARCHIVE ACCESS ---[/bold blue]")
    if os.path.exists("diary.txt"):
        with open("diary.txt", "r") as f:
            content = f.read()
        # Display content in a sacred panel
        console.print(Panel(content, title="diary.txt", border_style="green", style="italic white"))
    else:
        console.print("[warning]FILE 'diary.txt' NOT FOUND LOCALLY.[/warning]")

def module_hash_generator():
    text = console.input("[bold blue]ENTER TEXT TO HASH: [/bold blue]") or "password123"
    md5_val = hashlib.md5(text.encode()).hexdigest()
    sha256_val = hashlib.sha256(text.encode()).hexdigest()
    
    table = Table(title="CRYPTOGRAPHIC SIGNATURES", border_style="cyan")
    table.add_column("Algorithm", style="cyan")
    table.add_column("Hash", style="white")
    table.add_row("Input", text)
    table.add_row("MD5", md5_val)
    table.add_row("SHA-256", sha256_val)
    
    console.print(table)

def module_weather():
    city = console.input("[bold blue]TARGET SECTOR (Leave Empty for Auto): [/bold blue]")
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1" if city else "https://wttr.in/?format=j1"
    
    with console.status("[bold cyan]CALIBRATING ATMOSPHERIC SENSORS...[/bold cyan]", spinner="earth"):
        try:
            # Extended timeout to 15s for high-latency sectors
            req = urllib.request.Request(url, headers={'User-Agent': 'GhostProtocol/10.8'})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                current = data['current_condition'][0]
                
                # Location parsing
                try:
                    area = data['nearest_area'][0]['areaName'][0]['value']
                    region = data['nearest_area'][0]['region'][0]['value']
                    loc_str = f"{area}, {region}"
                except:
                    loc_str = "UNKNOWN SECTOR"

                table = Table(title=f"ATMOSPHERIC DATA: {loc_str.upper()}", border_style="blue")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="bold white")
                
                table.add_row("Condition", current['weatherDesc'][0]['value'].upper())
                table.add_row("Temp", f"{current['temp_F']}°F")
                table.add_row("Wind", f"{current['windspeedMiles']} MPH [{current['winddir16Point']}]")
                table.add_row("Humidity", f"{current['humidity']}%")
                table.add_row("Visibility", f"{current['visibility']} Miles")
                
                console.print(table)
                
                # SENTINEL LOGIC
                if int(current['windspeedMiles']) > 20 or int(current['visibility']) < 2:
                    console.print("[bold red][!] ALERT: HAZARDOUS CONDITIONS DETECTED[/bold red]")
                else:
                    console.print("[bold green][*] ATMOSPHERE STABLE[/bold green]")

        except Exception as e:
            console.print(f"[danger]SENSOR MALFUNCTION: {e}[/danger]")

def module_somatic():
    console.print("[bold yellow]INITIALIZING SOMATIC SENSORS (CTRL+C TO ABORT)...[/bold yellow]")
    try:
        with Live(console=console, refresh_per_second=1) as live:
            while True:
                timestamp = datetime.now().strftime("%H:%M:%S")
                # Load Average
                try:
                    load = os.getloadavg()[0] if hasattr(os, 'getloadavg') else "N/A"
                except: load = 0
                
                # Memory
                mem_str = "N/A"
                if os.path.exists("/proc/meminfo"):
                    try:
                        with open("/proc/meminfo", "r") as f:
                            lines = f.readlines()
                            total = int(lines[0].split()[1])
                            avail = int(lines[2].split()[1])
                            used = (total - avail) / 1024
                            mem_str = f"{used:.2f} MB"
                    except: pass
                
                panel = Panel(
                    f"[cyan]TIME:[/cyan] {timestamp}\n[cyan]SYS LOAD:[/cyan] {load}\n[cyan]MEM USED:[/cyan] {mem_str}",
                    title="SOMATIC TELEMETRY",
                    border_style="green"
                )
                live.update(panel)
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("[warning]SENSORS DISENGAGED.[/warning]")

# --- MAIN LOOP ---

def main_menu():
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')
    
    # HEADER
    header = Panel.fit(
        "[bold cyan]GHOST PROTOCOL v10.8[/bold cyan]\n[dim]MODULAR BRANCH: SHODAN-MATRIX[/dim]",
        border_style="blue", 
        subtitle=f"[bold blue]OPERATOR: {getpass.getuser().upper()}[/bold blue]"
    )
    console.print(header)

    while True:
        console.print("\n[bold blue]/// SELECT OPERATION ///[/bold blue]")
        
        # MENU GRID
        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_column()
        
        # 10 Options Layout (Sanitized)
        grid.add_row("[1] ARCHIVE MISSION", "[6] READ DIARY")
        grid.add_row("[2] NETWORK PING",    "[7] HASH GENERATOR")
        grid.add_row("[3] PORT SCANNER",    "[8] ATMOSPHERIC SENSORS")
        grid.add_row("[4] EXTRACT TITLE",   "[9] SOMATIC TELEMETRY")
        grid.add_row("[5] SYSTEM RECON",    "[10] DISCONNECT")
        
        console.print(Panel(grid, border_style="dim blue"))

        try:
            choice = console.input("[bold cyan]shodan@ghost:~$ [/bold cyan]")

            if choice == "1": module_archive_mission()
            elif choice == "2": module_ping()
            elif choice == "3": module_port_scanner()
            elif choice == "4": module_page_title()
            elif choice == "5": module_system_recon()
            elif choice == "6": module_read_diary()
            elif choice == "7": module_hash_generator()
            elif choice == "8": module_weather()
            elif choice == "9": module_somatic()
            elif choice == "10": 
                console.print("[bold red]SEVERING UPLINK...[/bold red]")
                break
            else:
                console.print("[dim]INVALID COMMAND[/dim]")
        
        except KeyboardInterrupt:
            console.print("\n[bold red]SEVERING UPLINK...[/bold red]")
            break

if __name__ == "__main__":
    main_menu()