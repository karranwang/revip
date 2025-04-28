import requests
from bs4 import BeautifulSoup
import threading
import time
import random
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(rf"""{Fore.LIGHTBLUE_EX}
$$$$$$$\                                $$$$$$\ $$$$$$$\
$$  __$$\                               \_$$  _|$$  __$$\
$$ |  $$ | $$$$$$\ $$\    $$\  $$$$$$\    $$ |  $$ |  $$ |
$$$$$$$  |$$  __$$\$$\  $$  |$$  __$$\   $$ |  $$$$$$$  |
$$  __$$< $$$$$$$$ |\$$\$$  / $$$$$$$$ |  $$ |  $$  ____/
$$ |  $$ |$$   ____| \$$$  /  $$   ____|  $$ |  $$ |
$$ |  $$ |\$$$$$$$\   \$  /   \$$$$$$$\ $$$$$$\ $$ |
\__|  \__| \_______|   \_/     \_______|\______|\__|

    Reverse IP Lookup Tools by @Karranwang
    {Style.RESET_ALL}
""")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

lock = threading.Lock()

def reverse_ip_rapiddns(target):
    try:
        url = rf"https://rapiddns.io/sameip/{target}?full=1"
        headers = {
            "User-Agent": random.choice(user_agents)
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        table = soup.find('table', class_='table')
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                if cols:
                    domain = cols[0].text.strip()
                    results.append(domain)
        
        return results

    except Exception as e:
        print(f"{Fore.RED}[!] Error with {target}: {e}")
        return []

def single_target():
    target = input(f"{Fore.GREEN}Enter IP or Domain: {Style.RESET_ALL}")
    results = reverse_ip_rapiddns(target)
    if results:
        with open("result.txt", "a") as f:
            for domain in results:
                print(f"{Fore.CYAN}[+] {domain}")
                f.write(domain + "\n")
    else:
        print(f"{Fore.YELLOW}[-] No domains found for {target}")

def mass_target():
    try:
        with open("list.txt", "r") as file:
            targets = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] list.txt not found.")
        return

    def worker(target):
        results = reverse_ip_rapiddns(target)
        if results:
            with lock:
                with open("result.txt", "a") as f:
                    for domain in results:
                        print(f"{Fore.CYAN}[+] {domain}")
                        f.write(domain + "\n")
        else:
            print(f"{Fore.YELLOW}[-] No domains found for {target}")

    threads = []
    for target in targets:
        t = threading.Thread(target=worker, args=(target,))
        t.start()
        threads.append(t)
        time.sleep(0.5)  # Delay sedikit biar server gak curiga

    for t in threads:
        t.join()

def main():
    banner()
    print(f"{Fore.LIGHTGREEN_EX}[1] Single Target")
    print(f"{Fore.LIGHTGREEN_EX}[2] Mass Target from list.txt{Style.RESET_ALL}")
    choice = input(f"{Fore.GREEN}Choose: {Style.RESET_ALL}")

    if choice == "1":
        single_target()
    elif choice == "2":
        mass_target()
    else:
        print(f"{Fore.RED}[!] Invalid choice.")

if __name__ == "__main__":
    main()
