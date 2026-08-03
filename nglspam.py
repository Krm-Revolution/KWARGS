import random
import string
import requests
import os
from pystyle import Colors, Colorate
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

def ngl():
    def deviceId():
        characters = string.ascii_lowercase + string.digits
        part1 = ''.join(random.choices(characters, k=8))
        part2 = ''.join(random.choices(characters, k=4))
        part3 = ''.join(random.choices(characters, k=4))
        part4 = ''.join(random.choices(characters, k=4))
        part5 = ''.join(random.choices(characters, k=12))
        return f"{part1}-{part2}-{part3}-{part4}-{part5}"
    
    def getProxy():
        try:
            with open('proxies.txt', 'r') as file:
                proxies_list = [line.strip() for line in file.readlines() if line.strip()]
                if not proxies_list:
                    print(R + "[-]" + W + " Error: proxies.txt is empty")
                    return None
                random_proxy = random.choice(proxies_list)
                return {'http': random_proxy, 'https': random_proxy}
        except FileNotFoundError:
            print(R + "[-]" + W + " Error: proxies.txt not found")
            return None
        
    R = '\033[31m'
    G = '\033[32m'
    W = '\033[0m'

    os.system('cls' if os.name == 'nt' else 'clear')

    print(Colorate.Vertical(Colors.blue_to_purple,"""
        ░██████╗███╗░░░███╗░█████╗░██╗░░██╗███████╗
        ██╔════╝████╗░████║██╔══██╗██║░██╔╝██╔════╝
        ╚█████╗░██╔████╔██║███████║█████═╝░█████╗░░
        ░╚═══██╗██║╚██╔╝██║██╔══██║██╔═██╗░██╔══╝░░
        ██████╔╝██║░╚═╝░██║██║░░██║██║░╚██╗███████╗
        ╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝  
    """))
    
    nglusername = input(Colorate.Vertical(Colors.blue_to_purple,"Username: "))
    message = input(Colorate.Vertical(Colors.blue_to_purple,"Message: "))
    Count = int(input(Colorate.Vertical(Colors.blue_to_purple,"Count: ")))
    delay = float(input(Colorate.Vertical(Colors.blue_to_purple,"Delay between requests (enter 0 if you want the fastest in seconds): ")))
    use_proxy = input(Colorate.Vertical(Colors.blue_to_purple, "Use proxy? (y/n): ")).lower()

    proxies = getProxy() if use_proxy == "y" else None

    print(Colorate.Vertical(Colors.green_to_blue,"**********************************************************"))

    value = 0
    notsend = 0
    current_device_id = deviceId()
    
    while value < Count:
        current_ua = random.choice(USER_AGENTS)
        
        headers = {
            'Host': 'ngl.link',
            'sec-ch-ua': '"Google Chrome";v="120", "Chromium";v="120", "Not=A?Brand";v="24"',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': current_ua,
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://ngl.link',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://ngl.link/{nglusername}',
            'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        data = {
            'username': nglusername,
            'question': message,
            'deviceId': current_device_id,
            'gameSlug': '',
            'referrer': '',
        }

        try:
            response = requests.post('https://ngl.link/api/submit', headers=headers, data=data, proxies=proxies, timeout=10)
            if response.status_code == 200:
                notsend = 0
                value += 1
                print(G + "[+]" + W + " Send =>" + G + " {}".format(value) + W)
            else:
                notsend += 1
                print(R + "[-]" + W + " Not Send (Status: {})".format(response.status_code))
                
            if notsend >= 4:
                print(R + "[!]" + W + " Changing device ID and proxy")
                current_device_id = deviceId()
                notsend = 0
                if use_proxy == "y":
                    proxies = getProxy()

            time.sleep(delay)

        except requests.exceptions.ProxyError:
            print(R + "[-]" + W + " Bad Proxy, switching")
            if use_proxy == "y":
                proxies = getProxy()
        except requests.exceptions.ConnectionError:
            print(R + "[-]" + W + " Connection Error, retrying")
            time.sleep(2)
        except requests.exceptions.Timeout:
            print(R + "[-]" + W + " Request Timeout")
            if use_proxy == "y":
                proxies = getProxy()
        except Exception as e:
            print(R + "[-]" + W + " Error: {}".format(str(e)))

ngl()
