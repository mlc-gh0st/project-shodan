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
from datetime import datetime

# GLOBAL LOCK
print_lock = threading.Lock()

def slow_print(text, speed=0.02):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def scan_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            with print_lock:
                print(f"[+] PORT {port}: OPEN (VULNERABILITY DETECTED)")
        sock.close()
    except:
        pass

def raw_whois(server, query):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((server, 43))
        s.send(f"{query}\r\n".encode())
        response = b""
        while True:
            data = s.recv(4096)
            if not data: break
            response += data
        s.close()
        return response.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error: {e}"

def get_mac():
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))

# SYSTEM STARTUP
if platform.system().lower() == 'windows':
    os.system('cls')
else:
    os.system('clear')

print("\033[1;32m")
slow_print("GHOST PROTOCOL v10.1 (STABLE LINK) LOADED.")
print("---------------------------------")

current_user = getpass.getuser()
slow_print(f"OPERATOR: {current_user}")
slow_print(f"KERNEL:   {platform.release()}")

while True:
    print("\nSELECT OPERATION:")
    print("1.  ARCHIVE MISSION (LOGOS - LOCAL)")
    print("2.  NETWORK PING (ECHO)")
    print("3.  PORT SCANNER (THREADED)")
    print("4.  EXTRACT PAGE TITLE")
    print("5.  WHOIS LOOKUP")
    print("6.  SYSTEM RECON")
    print("7.  HASH GENERATOR")
    print("8.  BRUTE FORCE SIMULATOR")
    print("9.  ATMOSPHERIC SENSORS")
    print("10. SOMATIC TELEMETRY (REAL-TIME)")
    print("11. DISCONNECT")
    
    # [PATCH APPLIED HERE: SHIELDED INPUT]
    try:
        choice = input("\n> ")
    except KeyboardInterrupt:
        print("\n\n[*] CONNECTION SEVERED.")
        break

    # [LOGIC GATE START]
    if choice == "1":
        # THE JOURNAL PROTOCOL (Local Only - No Git Automation)
        slow_print("ENTER MISSION OBJECTIVE:")
        mission = input("> ")
        if mission == "": mission = "routine_update"
        
        # 1. Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | {mission}\n"
        
        # 2. Visual Confirmation
        print("\n--- STAGING ENTRY ---")
        print(log_entry.strip())
        
        confirm = input("SAVE TO DISK? [Y/n]: ").lower()
        if confirm != "n":
            with open("mission_log.txt", "a") as f:
                f.write(log_entry)
            print("\033[1;32m")
            slow_print("[+] ENTRY LOGGED. READY FOR MANUAL COMMIT.")
        else:
            slow_print("ENTRY DISCARDED.")

    elif choice == "2":
        target = input("ENTER TARGET: ")
        if target == "": target = "google.com"
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        subprocess.run(["ping", param, "2", target])

    elif choice == "3":
        target = input("ENTER TARGET DOMAIN: ")
        if target == "": target = "google.com"
        try:
            target_ip = socket.gethostbyname(target)
            slow_print(f"TARGET RESOLVED: {target_ip}")
            slow_print("INITIALIZING 100 THREADS...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                for port in range(1, 1025):
                    executor.submit(scan_port, target_ip, port)
            slow_print("SCAN COMPLETE.")
        except socket.gaierror:
            slow_print("ERROR: COULD NOT RESOLVE HOST.")

    elif choice == "4":
        slow_print("ENTER TARGET URL:")
        url = input("> ")
        if url == "": url = "https://www.amazon.com"
        if not url.startswith("http"): url = "https://" + url
        slow_print(f"CONNECTING TO {url}...")
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124')
            response = urllib.request.urlopen(req, timeout=5)
            html_content = response.read().decode('utf-8', errors='ignore')
            pattern = re.search('<title>(.*?)</title>', html_content, flags=re.IGNORECASE)
            if pattern:
                slow_print(f"TARGET IDENTIFIED: {pattern.group(1).strip()}")
            else:
                slow_print("WARNING: NO TITLE SIGNAL FOUND.")
        except Exception as e:
            slow_print(f"CONNECTION FAILED: {e}")

    elif choice == "5":
        target = input("ENTER DOMAIN (e.g., google.com): ")
        if target == "": target = "google.com"
        slow_print("CONTACTING ROOT SERVER (IANA)...")
        iana_response = raw_whois("whois.iana.org", target)
        referral = re.search(r'refer:\s*(.*)', iana_response, re.IGNORECASE)
        if referral:
            whois_server = referral.group(1).strip()
            slow_print(f"REDIRECTING TO: {whois_server}")
            print("---------------------------------")
            print(raw_whois(whois_server, target))
        else:
            print("---------------------------------")
            print(iana_response)
        slow_print("WHOIS DATA STREAM COMPLETE.")

    elif choice == "6":
        slow_print("GATHERING SYSTEM TELEMETRY...")
        time.sleep(1)
        print("---------------------------------")
        print(f"OS TYPE:     {platform.system()} {platform.release()}")
        print(f"OS VERSION:  {platform.version()}")
        print(f"MACHINE:     {platform.machine()}")
        print(f"HOSTNAME:    {socket.gethostname()}")
        print(f"MAC ADDRESS: {get_mac()}")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            internal_ip = s.getsockname()[0]
            s.close()
            print(f"INTERNAL IP: {internal_ip}")
        except:
            print("INTERNAL IP: UNKNOWN")
        try:
            external_ip = urllib.request.urlopen('https://api.ipify.org', timeout=3).read().decode('utf8')
            print(f"PUBLIC IP:   {external_ip}")
        except:
            print("PUBLIC IP:   CONNECTION TIMED OUT")
        print("---------------------------------")

    elif choice == "7":
        slow_print("ENTER TEXT TO HASH:")
        secret = input("> ")
        if secret == "": secret = "password123"
        md5_val = hashlib.md5(secret.encode()).hexdigest()
        sha256_val = hashlib.sha256(secret.encode()).hexdigest()
        print("---------------------------------")
        print(f"INPUT:    {secret}")
        print(f"MD5:      {md5_val}")
        print(f"SHA-256:  {sha256_val}")
        print("---------------------------------")
        slow_print("CRYPTOGRAPHIC SIGNATURES GENERATED.")

    elif choice == "8":
        slow_print("ENTER PASSWORD TO SIMULATE HACK:")
        target_password = input("> ")
        if target_password == "": target_password = "admin"
        target_hash = hashlib.md5(target_password.encode()).hexdigest()
        slow_print(f"TARGET HASH LOCKED: {target_hash}")
        wordlist = ["password", "123456", "admin", "welcome", "love", "secret", "god", "help", "letmein"]
        slow_print("INITIATING DICTIONARY ATTACK...")
        time.sleep(1)
        found = False
        start_time = time.time()
        for word in wordlist:
            guess_hash = hashlib.md5(word.encode()).hexdigest()
            print(f"TRYING: {word} \t [{guess_hash}]")
            time.sleep(0.1)
            if guess_hash == target_hash:
                end_time = time.time()
                print("\033[1;31m")
                print(f"\n[!] MATCH FOUND: {word}")
                print(f"TIME ELAPSED: {round(end_time - start_time, 2)} SECONDS")
                print("\033[1;32m")
                found = True
                break
        if not found:
            slow_print("\n[-] ATTACK FAILED. PASSWORD NOT IN DICTIONARY.")

    elif choice == "9":
        slow_print("ENTER TARGET CITY (e.g. London):")
        city = input("> ")
        if city == "": city = "London"
        city_encoded = urllib.parse.quote(city)
        slow_print(f"CONNECTING TO SATELLITE FEED FOR: {city.upper()}...")
        try:
            url = f"https://wttr.in/{city_encoded}?format=3"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124')
            response = urllib.request.urlopen(req, timeout=5)
            weather_data = response.read().decode('utf-8').strip()
            print("---------------------------------")
            print(f"DATA RECEIVED: {weather_data}")
            print("---------------------------------")
        except Exception as e:
            slow_print(f"CONNECTION ERROR: {e}")

    elif choice == "10":
        slow_print("INITIALIZING SOMATIC SENSORS (CTRL+C TO ABORT)...")
        time.sleep(1)
        print("-" * 65)
        print(f"{'TIMESTAMP':<20} | {'PRESSURE (Load)':<15} | {'VOLATILE MEM (MB)':<18}")
        print("-" * 65)
        try:
            while True:
                try:
                    with open("/proc/loadavg", "r") as f:
                        load_data = f.read().split()
                        load_1m = load_data[0]
                except FileNotFoundError:
                    load_1m = "N/A (WIN)"
                mem_used_mb = 0.0
                try:
                    mem_stats = {}
                    with open("/proc/meminfo", "r") as f:
                        for line in f:
                            parts = line.split()
                            key = parts[0].strip(":")
                            value = int(parts[1])
                            if key in ["MemTotal", "MemAvailable"]:
                                mem_stats[key] = value
                    if "MemTotal" in mem_stats and "MemAvailable" in mem_stats:
                        mem_used_kb = mem_stats["MemTotal"] - mem_stats["MemAvailable"]
                        mem_used_mb = mem_used_kb / 1024
                except FileNotFoundError:
                    pass 
                timestamp = datetime.now().strftime("%H:%M:%S")
                sys.stdout.write(f"\r{timestamp:<20} | {load_1m:<15} | {mem_used_mb:.2f} MB           ")
                sys.stdout.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[*] SENSORS DISENGAGED.")
            time.sleep(0.5)

    elif choice == "11":
        slow_print("SEVERING CONNECTION...")
        break 

    else:
        print("INVALID COMMAND")

print("\033[0m")