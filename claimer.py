import requests
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

print(f"{Fore.CYAN}Made by LightCyan01{Style.RESET_ALL}")

payload = {'username': 'USERNAME HERE'}
headers = {'Authorization': 'TOKEN HERE'}

def send_request(url, headers, payload):
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} {Fore.RED}[ERROR] {e}{Style.RESET_ALL}\n")
        raise

def claim_username(url, headers, payload):
    try:
        # Check if token is valid
        r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
        if r.status_code == 200:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} {Fore.GREEN}[SUCCESS] Token is valid.{Style.RESET_ALL}\n")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} {Fore.RED}[ERROR] Your token is invalid.{Style.RESET_ALL}\n")
            return

        while True:
            r = send_request(url, headers, payload)
            if r.status_code == 200:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp} {Fore.GREEN}[SUCCESS] Claimed username.{Style.RESET_ALL}\n")
                break
            elif r.status_code == 429:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp} {Fore.RED}[ERROR] Too many attempts. Retrying in {r.headers.get('Retry-After')} seconds.{Style.RESET_ALL}\n")
                time.sleep(int(r.headers.get('Retry-After')))
            elif r.status_code == 401:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp} {Fore.RED}[ERROR] 401 - Unauthorized. Retrying in 30 minutes.{Style.RESET_ALL}\n")
                time.sleep(30 * 60)
            elif r.status_code == 400 and 'username' in r.json():
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp} {Fore.RED}[ERROR] Username '{payload['username']}' is taken.{Style.RESET_ALL}\n")
                return
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp} {Fore.RED}[ERROR] {r.status_code} (will re-attempt). Retrying in 30 minutes.{Style.RESET_ALL}\n")
                time.sleep(30 * 60)
    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} {Fore.RED}[ERROR] {e}{Style.RESET_ALL}\n")
        print(f"{timestamp} {Fore.RED}[ERROR] Connection error (will re-attempt). Retrying in 30 minutes.{Style.RESET_ALL}\n")
        time.sleep(30 * 60)

url = 'https://discord.com/api/v9/users/@me/pomelo'

claim_username(url, headers, payload)