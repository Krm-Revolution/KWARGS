import requests
import os
import sys
import json
import time
import random
import threading
from datetime import datetime, timezone, timedelta
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

ses = requests.Session()

UA_LIST = [
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.154 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; V2025) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.118 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
]

COLORS = {
    'red': '91',
    'green': '92',
    'yellow': '93',
    'blue': '94',
    'magenta': '95',
    'cyan': '96',
    'white': '97',
    'grey': '90',
    'bold': '1',
    'underline': '4',
    'blink': '5'
}

class FacebookSpamBot:
    def __init__(self):
        self.tokens = []
        self.suspended_tokens = []
        self.running = True
        self.lock = threading.Lock()
        
    def get_ph_time(self):
        ph_tz = timezone(timedelta(hours=8))
        return datetime.now(ph_tz)
    
    def color_text(self, text, color_name='white'):
        color_code = COLORS.get(color_name, '97')
        return f"\033[{color_code}m{text}\033[0m"
    
    def print_banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        banner_art = """
    ╔═══════════════════════════════════════╗
    ║     ██████  ██       █████  ██ ██████  ║
    ║    ██       ██      ██   ██ ██ ██   ██ ║
    ║    ██   ███ ██      ███████ ██ ██████  ║
    ║    ██    ██ ██      ██   ██ ██ ██   ██ ║
    ║     ██████  ███████ ██   ██ ██ ██   ██ ║
    ╚═══════════════════════════════════════╝
        """
        
        colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
        for i, line in enumerate(banner_art.split('\n')):
            color = colors[i % len(colors)]
            print(self.color_text(line, color))
        
        print(self.color_text("\n┌─────────────────────────────────────┐", 'cyan'))
        print(self.color_text("│ Developer: glaiz                     │", 'green'))
        print(self.color_text("│ Facebook: @glaiz.official            │", 'green'))
        print(self.color_text("│ GitHub: @glaiz                       │", 'green'))
        print(self.color_text("│ Version: 3.0.0                       │", 'green'))
        print(self.color_text("└─────────────────────────────────────┘", 'cyan'))
        print()
    
    def loading_animation(self, duration=2, message="Processing"):
        chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for char in chars:
                sys.stdout.write(f'\r{self.color_text(message, "yellow")} {self.color_text(char, "cyan")}')
                sys.stdout.flush()
                time.sleep(0.1)
                if time.time() >= end_time:
                    break
        
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()
    
    def speak_text(self, text):
        try:
            subprocess.run(["espeak-ng", text, "-s", "150", "-p", "50"], 
                         check=True, 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        except:
            pass
    
    def get_user_input(self, prompt, color='cyan', speak=True):
        print(self.color_text(prompt, color), end=' ')
        user_input = input()
        if speak and user_input:
            self.speak_text(user_input)
        return user_input.strip()
    
    def validate_token(self, token):
        if token.startswith(('EAA', 'EAAG', 'EAAB')) and len(token) > 50:
            return True
        return False
    
    def save_database(self):
        try:
            with open('tokens.json', 'w') as f:
                json.dump(self.tokens, f, indent=2)
            return True
        except:
            return False
    
    def load_database(self):
        try:
            if os.path.exists('tokens.json'):
                with open('tokens.json', 'r') as f:
                    self.tokens = json.load(f)
            return len(self.tokens) > 0
        except:
            return False
    
    def add_tokens_manual(self):
        self.print_banner()
        print(self.color_text("\n[ ADD TOKENS TO DATABASE ]", 'yellow'))
        print(self.color_text("=" * 40, 'grey'))
        print(self.color_text("\nGet tokens using Token Getter extension on Kiwi Browser", 'cyan'))
        print(self.color_text("Token format: Starts with EAA, EAAG, or EAAB", 'yellow'))
        
        while True:
            try:
                num_tokens = int(self.get_user_input(
                    "How many tokens to add? ", 
                    'cyan'
                ))
                if num_tokens > 0:
                    break
                print(self.color_text("Please enter a positive number!", 'red'))
            except ValueError:
                print(self.color_text("Invalid input! Enter a number.", 'red'))
        
        added = 0
        for i in range(num_tokens):
            print(self.color_text(f"\n--- Token #{i+1} ---", 'magenta'))
            
            token = self.get_user_input(
                "Paste token:", 
                'green',
                speak=False
            )
            
            self.loading_animation(1, f"Validating token {i+1}")
            
            if self.validate_token(token):
                self.tokens.append(token)
                added += 1
                print(self.color_text(f"✓ Token validated: {token[:30]}...", 'green'))
            else:
                print(self.color_text("✗ Invalid token format!", 'red'))
                print(self.color_text("Token must start with EAA, EAAG, or EAAB and be >50 chars", 'yellow'))
        
        if added > 0:
            self.save_database()
            print(self.color_text(f"\n✓ Successfully added {added} tokens!", 'green'))
        else:
            print(self.color_text("\n✗ No valid tokens added!", 'red'))
        
        self.get_user_input("\nPress Enter to continue...", 'grey', speak=False)
    
    def view_database(self):
        self.print_banner()
        print(self.color_text("\n[ DATABASE MANAGEMENT ]", 'yellow'))
        print(self.color_text("=" * 40, 'grey'))
        
        if not self.load_database():
            print(self.color_text("\nNo database found!", 'red'))
            self.get_user_input("Press Enter to continue...", 'grey', speak=False)
            return
        
        total = len(self.tokens)
        print(self.color_text(f"\nTotal tokens: {total}", 'cyan'))
        
        if total == 0:
            print(self.color_text("Database is empty!", 'yellow'))
            self.get_user_input("Press Enter to continue...", 'grey', speak=False)
            return
        
        print(self.color_text("\nToken List:", 'green'))
        print(self.color_text("-" * 50, 'grey'))
        
        for i, token in enumerate(self.tokens, 1):
            print(self.color_text(f"{i}. {token[:30]}...", 'cyan'))
        
        print(self.color_text("\nOptions:", 'yellow'))
        print(self.color_text("1. Remove specific tokens", 'green'))
        print(self.color_text("2. Remove all tokens", 'red'))
        print(self.color_text("3. Return to main menu", 'blue'))
        
        choice = self.get_user_input("Choose (1-3):", 'cyan')
        
        if choice == '1':
            indices = self.get_user_input(
                "Enter numbers to remove (comma-separated):", 
                'green', 
                speak=False
            )
            
            try:
                to_remove = [int(x.strip())-1 for x in indices.split(',')]
                to_remove.sort(reverse=True)
                
                for idx in to_remove:
                    if 0 <= idx < len(self.tokens):
                        self.tokens.pop(idx)
                
                self.save_database()
                print(self.color_text(f"✓ Removed {len(to_remove)} tokens!", 'green'))
            except:
                print(self.color_text("✗ Invalid input!", 'red'))
        
        elif choice == '2':
            confirm = self.get_user_input(
                "Delete ALL tokens? (yes/no):", 
                'red'
            ).lower()
            
            if confirm == 'yes':
                self.tokens = []
                self.save_database()
                print(self.color_text("✓ Database cleared!", 'green'))
        
        self.get_user_input("\nPress Enter to continue...", 'grey', speak=False)
    
    def share_single(self, token, link, share_num, start_time):
        headers = {
            "user-agent": random.choice(UA_LIST),
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded"
        }
        
        try:
            time.sleep(random.uniform(1, 3))
            
            response = ses.post(
                f"https://graph.facebook.com/v17.0/me/feed",
                params={
                    "link": link,
                    "published": "0",
                    "access_token": token
                },
                headers=headers,
                timeout=15
            )
            
            data = response.json()
            
            if "id" in data:
                elapsed = str(datetime.now() - start_time).split('.')[0]
                print(self.color_text(
                    f"[{share_num:4d}] ✓ Shared successfully! [{elapsed}]", 
                    'green'
                ))
                return True
            else:
                error = data.get('error', {}).get('message', 'Unknown error')
                
                if any(word in error.lower() for word in ['suspended', 'blocked', 'rate limit', 'access token']):
                    print(self.color_text(f"[{share_num:4d}] ✗ Token suspended/invalid!", 'red'))
                    with self.lock:
                        if token not in self.suspended_tokens:
                            self.suspended_tokens.append(token)
                    return False
                else:
                    print(self.color_text(f"[{share_num:4d}] ✗ Failed: {error[:50]}...", 'yellow'))
                    return False
                    
        except requests.exceptions.Timeout:
            print(self.color_text(f"[{share_num:4d}] ✗ Timeout error!", 'red'))
        except requests.exceptions.ConnectionError:
            print(self.color_text(f"[{share_num:4d}] ✗ Connection error!", 'red'))
        except json.JSONDecodeError:
            print(self.color_text(f"[{share_num:4d}] ✗ Invalid response!", 'red'))
        except Exception as e:
            print(self.color_text(f"[{share_num:4d}] ✗ Error: {str(e)[:50]}...", 'red'))
        
        return False
    
    def sharing_session(self):
        self.print_banner()
        print(self.color_text("\n[ SHARING SESSION ]", 'yellow'))
        print(self.color_text("=" * 40, 'grey'))
        
        if not self.load_database() or not self.tokens:
            print(self.color_text("\nNo tokens in database!", 'red'))
            print(self.color_text("Please add tokens first.", 'yellow'))
            self.get_user_input("Press Enter to continue...", 'grey', speak=False)
            return
        
        total_tokens = len(self.tokens)
        print(self.color_text(f"\nLoaded {total_tokens} tokens from database", 'green'))
        
        while True:
            link = self.get_user_input(
                "\nEnter post link to share:", 
                'green',
                speak=False
            )
            
            if link.startswith(('http://', 'https://')):
                break
            print(self.color_text("Invalid link! Must start with http:// or https://", 'red'))
        
        while True:
            try:
                shares = int(self.get_user_input(
                    "How many shares to perform?",
                    'cyan'
                ))
                if shares > 0:
                    break
                print(self.color_text("Please enter a positive number!", 'red'))
            except ValueError:
                print(self.color_text("Invalid input! Enter a number.", 'red'))
        
        print(self.color_text("\n" + "═" * 50, 'grey'))
        print(self.color_text(f"Starting {shares} shares...", 'yellow'))
        print(self.color_text("═" * 50, 'grey'))
        
        start_time = datetime.now()
        self.suspended_tokens = []
        
        successful = 0
        failed = 0
        
        chunk_size = 100
        cooldown = 5
        
        with ThreadPoolExecutor(max_workers=30) as executor:
            for chunk_start in range(0, shares, chunk_size):
                chunk_end = min(chunk_start + chunk_size, shares)
                futures = []
                
                for share_num in range(chunk_start + 1, chunk_end + 1):
                    active_indices = [
                        i for i, t in enumerate(self.tokens) 
                        if t not in self.suspended_tokens
                    ]
                    
                    if not active_indices:
                        print(self.color_text("\n✗ All tokens suspended/invalid!", 'red'))
                        break
                    
                    idx = random.choice(active_indices)
                    
                    future = executor.submit(
                        self.share_single,
                        self.tokens[idx],
                        link,
                        share_num,
                        start_time
                    )
                    futures.append(future)
                
                for future in as_completed(futures):
                    if future.result():
                        successful += 1
                    else:
                        failed += 1
                
                if chunk_end < shares:
                    print(self.color_text(
                        f"\n⏳ Cooldown for {cooldown} seconds...", 
                        'yellow'
                    ))
                    time.sleep(cooldown)
        
        if self.suspended_tokens:
            print(self.color_text("\nCleaning suspended tokens...", 'yellow'))
            
            clean_tokens = []
            
            for token in self.tokens:
                if token not in self.suspended_tokens:
                    clean_tokens.append(token)
            
            self.tokens = clean_tokens
            self.save_database()
            
            print(self.color_text(
                f"Removed {len(self.suspended_tokens)} suspended tokens", 
                'green'
            ))
        
        elapsed = str(datetime.now() - start_time).split('.')[0]
        print(self.color_text("\n" + "═" * 50, 'grey'))
        print(self.color_text("SESSION COMPLETE!", 'yellow'))
        print(self.color_text("═" * 50, 'grey'))
        print(self.color_text(f"Time elapsed: {elapsed}", 'cyan'))
        print(self.color_text(f"Successful: {successful}", 'green'))
        print(self.color_text(f"Failed: {failed}", 'red'))
        
        if successful + failed > 0:
            success_rate = (successful/(successful+failed))*100
            print(self.color_text(f"Success rate: {success_rate:.1f}%", 'cyan'))
        
        self.get_user_input("\nPress Enter to continue...", 'grey', speak=False)
    
    def run(self):
        while self.running:
            self.print_banner()
            
            print(self.color_text("\n[ MAIN MENU ]", 'yellow'))
            print(self.color_text("═" * 40, 'grey'))
            print(self.color_text("1. 📝 Add Tokens to Database", 'green'))
            print(self.color_text("2. 📋 View/Manage Database", 'cyan'))
            print(self.color_text("3. 🚀 Start Sharing Session", 'magenta'))
            print(self.color_text("4. ❌ Exit Program", 'red'))
            print(self.color_text("═" * 40, 'grey'))
            
            choice = self.get_user_input("Select option (1-4):", 'yellow')
            
            if choice == '1':
                self.add_tokens_manual()
            elif choice == '2':
                self.view_database()
            elif choice == '3':
                self.sharing_session()
            elif choice == '4':
                print(self.color_text("\nThank you for using GLAIZ FB Tool!", 'green'))
                print(self.color_text("Goodbye! 👋", 'yellow'))
                self.speak_text("Goodbye!")
                self.running = False
            else:
                print(self.color_text("Invalid option! Please try again.", 'red'))
                time.sleep(1)

if __name__ == "__main__":
    try:
        if sys.version_info < (3, 6):
            print("\033[91mPlease use Python 3.6 or higher!\033[0m")
            sys.exit(1)
        
        bot = FacebookSpamBot()
        bot.run()
        
    except KeyboardInterrupt:
        print("\n\n\033[93mProgram interrupted by user!\033[0m")
        print("\033[92mGoodbye! 👋\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91mUnexpected error: {e}\033[0m")
        sys.exit(1)
