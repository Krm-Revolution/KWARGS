import requests, os, re, sys, json, time, hashlib
from pathlib import Path
from datetime import datetime
import pytz
from rich.console import Console
from rich.panel import Panel

console = Console()
ses = requests.Session()

VERSION = "1.0"
AUTHOR = "SIEGFRIED SAMÁ"
TOOL_NAME = "SPAMSHARE"

def _vx():
    _k = "ce3a5d93cfa6dca73a0fb3548ea9626e"
    _a = hashlib.md5(AUTHOR.encode('utf-8')).hexdigest()
    return _a == _k

def _dx(h):
    return bytes.fromhex(h).decode('utf-8')

def banner():
    console.print()
    console.print("[bold bright_cyan]    ═══════════════════════════════════════════════════════════")
    console.print("[bold bright_cyan]              █████╗ ██╗   ██╗████████╗ ██████╗ ")
    console.print("[bold bright_cyan]             ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗")
    console.print("[bold bright_cyan]             ███████║██║   ██║   ██║   ██║   ██║")
    console.print("[bold bright_cyan]             ██╔══██║██║   ██║   ██║   ██║   ██║")
    console.print("[bold bright_cyan]             ██║  ██║╚██████╔╝   ██║   ╚██████╔╝")
    console.print("[bold bright_cyan]             ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ")
    console.print()
    console.print("[bold bright_cyan]         ███████╗██╗  ██╗ █████╗ ██████╗ ███████╗")
    console.print("[bold bright_cyan]         ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔════╝")
    console.print("[bold bright_cyan]         ███████╗███████║███████║██████╔╝█████╗  ")
    console.print("[bold bright_cyan]         ╚════██║██╔══██║██╔══██║██╔══██╗██╔══╝  ")
    console.print("[bold bright_cyan]         ███████║██║  ██║██║  ██║██║  ██║███████╗")
    console.print("[bold bright_cyan]         ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝")
    console.print("[bold bright_cyan]    ═══════════════════════════════════════════════════════════")
    console.print()

    if not _vx():
        console.print(f"[bold bright_red]    {_dx('626f626f206368616e67652063726564697473207061')}[/bold bright_red]")
        console.print()
        time.sleep(3)
        sys.exit(1)

    info = f"""[bold bright_yellow]AUTHOR  »[/bold bright_yellow] [bright_magenta]{AUTHOR}
[bold bright_yellow]TOOL    »[/bold bright_yellow] [bright_cyan]{TOOL_NAME}
[bold bright_yellow]VERSION »[/bold bright_yellow] [bright_green]{VERSION}"""

    console.print(Panel(info, border_style="bright_yellow", width=70, padding=(0, 2)))
    console.print()

def menu_logo():
    os.system("clear" if os.name == "posix" else "cls")
    banner()

def get_ph_time():
    ph_tz = pytz.timezone('Asia/Manila')
    ph_time = datetime.now(ph_tz)
    return ph_time.strftime("%I:%M:%S %p")

def login():
    if os.path.exists("token.txt"):
        os.remove("token.txt")
    if os.path.exists("cookie.txt"):
        os.remove("cookie.txt")

    menu_logo()

    status_info = "[bold bright_cyan]TAKE COOKIES FROM KIWI BROWSER."
    console.print(Panel(status_info, title='[bold bright_yellow]AUTHENTICATION', style="bright_cyan", width=70))

    cookie = console.input("[bold bright_cyan] └──> [bold bright_white]ENTER COOKIE: ")

    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36",
            "referer": "https://www.facebook.com/",
            "host": "business.facebook.com",
            "origin": "https://business.facebook.com",
            "upgrade-insecure-requests": "1",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "content-type": "text/html; charset=utf-8",
            "cookie": cookie
        }

        data = ses.get("https://business.facebook.com/business_locations", headers=headers)

        find_token = re.search(r"(EAAG\w+)", data.text)
        token = find_token.group(1)

        with open("token.txt", "w") as f:
            f.write(token)
        with open("cookie.txt", "w") as f:
            f.write(cookie)

        console.print(Panel("[bold bright_green]LOGIN SUCCESSFUL! ACCESS TOKEN SAVED.", style="bright_green", width=45))
        time.sleep(2)
        start_sharing()

    except Exception:
        if os.path.exists("token.txt"):
            os.remove("token.txt")
        if os.path.exists("cookie.txt"):
            os.remove("cookie.txt")

        console.print(Panel("[bold bright_red]INVALID COOKIE! PLEASE TRY AGAIN.", title="[bold bright_red]ERROR", style="bright_red", width=45))
        time.sleep(2)
        login()

def start_sharing():
    try:
        if not os.path.exists("token.txt") or not os.path.exists("cookie.txt"):
            login()
            return

        token = open("token.txt","r").read()
        cok = open("cookie.txt","r").read()
        cookie = {"cookie":cok}

        menu_logo()

        user_data = ses.get(f"https://b-graph.facebook.com/me?fields=name,id&access_token={token}", cookies=cookie).json()
        name = user_data.get("name", "UNKNOWN USER")
        uid = user_data.get("id", "UNKNOWN ID")

        session_info = f"""[bold bright_yellow]ACCOUNT »[/bold bright_yellow] [bright_cyan]{name}
[bold bright_yellow]USER ID »[/bold bright_yellow] [bright_cyan]{uid}"""

        console.print(Panel(session_info, border_style="bright_yellow", width=70, padding=(0, 2)))
        console.print()

        console.print("[bold bright_cyan] ┌─[[bold bright_white]POST LINK[/bold bright_cyan]]")
        link = console.input("[bold bright_cyan] └──> : ")

        console.print("[bold bright_cyan] ┌─[[bold bright_white]AMOUNT[/bold bright_cyan]]")
        amount = int(console.input("[bold bright_cyan] └──> : "))

        console.print("[bold bright_cyan] ┌─[[bold bright_white]SHARE DELAY (SECONDS)[/bold bright_cyan]]")
        console.print("[bold bright_cyan] │  [dim bright_white]OPTIONS: 0.5S | 1S | 1.5S | 2S")
        delay_input = console.input("[bold bright_cyan] └──> : ")

        try:
            delay_time = float(delay_input)
        except ValueError:
            console.print("[bold bright_red]✗ INVALID NUMBER")
            time.sleep(1)
            return start_sharing()

        console.print()
        console.print(Panel(f"[bold bright_green]STARTING PROCESS FOR {amount} SHARES...", style="bright_green", width=70))
        console.print()

        count = 0
        success_count = 0
        fail_count = 0

        next_share_time = time.time()

        for i in range(amount):
            count += 1

            current_time = time.time()
            wait_time = next_share_time - current_time
            if wait_time > 0:
                time.sleep(wait_time)

            response = ses.post(f"https://b-graph.facebook.com/v13.0/me/feed?link={link}&published=0&access_token={token}", cookies=cookie).json()

            timestamp = get_ph_time()

            if "id" in response:
                success_count += 1
                raw_id = response.get("id")
                post_id = raw_id.split('_')[-1] if '_' in raw_id else raw_id

                console.print(f"[bright_white]{timestamp}[/bright_white] [bold bright_cyan]#{count:03d}[/bold bright_cyan] [bold bright_green]✓[/bold bright_green] [bright_white]SHARED[/bright_white] [bright_cyan]➜[/bright_cyan] [bright_yellow]{post_id}")
            else:
                fail_count += 1
                err_msg = response.get("error", {}).get("message", "SHARING BLOCKED OR COOKIE EXPIRED.")
                console.print(f"[bright_white]{timestamp}[/bright_white] [bold bright_red]#{count:03d}[/bold bright_red] [bold bright_red]✗[/bold bright_red] [bright_white]FAILED[/bright_white] [bright_red]➜[/bright_red] [bright_red]{err_msg[:40]}")
                break

            next_share_time += delay_time

        console.print()

        summary = f"""[bold bright_yellow]TOTAL   »[/bold bright_yellow] [bright_white]{count}
[bold bright_yellow]SUCCESS »[/bold bright_yellow] [bright_green]{success_count}
[bold bright_yellow]FAILED  »[/bold bright_yellow] [bright_red]{fail_count}"""

        console.print(Panel(summary, title="[bold bright_green]SUMMARY", border_style="bright_green", width=70, padding=(0, 2)))
        console.print()

        action = console.input("[bold bright_cyan]╰─➤ [bright_white]SHARE MORE? [Y/N]: ").strip().upper()

        if action in ['Y', 'YES', '']:
            start_sharing()
        else:
            console.print("\n[bright_white]GOODBYE!")
            sys.exit(0)

    except Exception as e:
        console.print(Panel(f"[bold bright_red]ERROR: {str(e)}", style="bright_red", width=70))
        time.sleep(2)
        login()


if __name__ == "__main__":
    login()
