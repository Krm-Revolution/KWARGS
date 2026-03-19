import requests
import os
import re
import sys
import json
import time
import random
import threading
from datetime import datetime, timezone, timedelta
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

# Global session object
ses = requests.Session()

# Extended user agent list for better randomization
UA_LIST = [
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.154 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; V2025) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.118 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
]

# Color codes dictionary for consistent usage
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
        self.cookies_list = []
        self.suspended_cookies = []
        self.running = True
        self.lock = threading.Lock()
        
    def get_ph_time(self):
        """Get current Philippine time (UTC+8)"""
        ph_tz = timezone(timedelta(hours=8))
        return datetime.now(ph_tz)
    
    def color_text(self, text, color_name='white'):
        """Apply color to text using color name"""
        color_code = COLORS.get(color_name, '97')
        return f"\033[{color_code}m{text}\033[0m"
    
    def print_banner(self):
        """Display animated banner with gradient effect"""
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
        
        # Gradient effect
        colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
        for i, line in enumerate(banner_art.split('\n')):
            color = colors[i % len(colors)]
            print(self.color_text(line, color))
        
        print(self.color_text("\n┌─────────────────────────────────────┐", 'cyan'))
        print(self.color_text("│ Developer: glaiz                     │", 'green'))
        print(self.color_text("│ Facebook: @glaiz.official            │", 'green'))
        print(self.color_text("│ GitHub: @glaiz                       │", 'green'))
        print(self.color_text("│ Version: 2.0.0                       │", 'green'))
        print(self.color_text("└─────────────────────────────────────┘", 'cyan'))
        print()
    
    def loading_animation(self, duration=2, message="Processing"):
        """Show loading animation for specified duration"""
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
        """Convert text to speech using espeak-ng"""
        try:
            subprocess.run(["espeak-ng", text, "-s", "150", "-p", "50"], 
                         check=True, 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass  # Silently fail if TTS not available
    
    def get_user_input(self, prompt, color='cyan', speak=True):
        """Get user input with optional TTS"""
        print(self.color_text(prompt, color), end=' ')
        user_input = input()
        if speak and user_input:
            self.speak_text(user_input)
        return user_input.strip()
    
    def validate_cookie_format(self, cookie_string):
        """Validate cookie string format"""
        try:
            cookies = {}
            for item in cookie_string.split(';'):
                if '=' in item:
                    key, value = item.strip().split('=', 1)
                    cookies[key] = value
            return cookies if cookies else None
        except:
            return None
    
    def extract_token(self, cookies):
        """Extract access token from Facebook business page"""
        headers = {
            "user-agent": random.choice(UA_LIST),
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.5",
            "accept-encoding": "gzip, deflate",
            "connection": "keep-alive",
            "upgrade-insecure-requests": "1"
        }
        
        try:
            response = ses.get(
                "https://business.facebook.com/business_locations",
                headers=headers,
                cookies=cookies,
                timeout=15,
                allow_redirects=True
            )
            
            # Search for EAAG token pattern
            token_patterns = [
                r'(EAAG\w+)',
                r'(EAA[A-Za-z0-9]+)',
                r'(EAAB\w+)'
            ]
            
            for pattern in token_patterns:
                matches = re.findall(pattern, response.text)
                if matches:
                    return matches[0]
            
            return None
            
        except requests.exceptions.RequestException:
            return None
    
    def save_database(self):
        """Save tokens and cookies to files"""
        try:
            with open('tokens.json', 'w') as f:
                json.dump(self.tokens, f, indent=2)
            with open('cookies.json', 'w') as f:
                json.dump(self.cookies_list, f, indent=2)
            return True
        except:
            return False
    
    def load_database(self):
        """Load tokens and cookies from files"""
        try:
            if os.path.exists('tokens.json'):
                with open('tokens.json', 'r') as f:
                    self.tokens = json.load(f)
            if os.path.exists('cookies.json'):
                with open('cookies.json', 'r') as f:
                    self.cookies_list = json.load(f)
            return len(self.tokens) > 0
        except:
            return False
    
    def add_cookies_manual(self):
        """Manually add cookies to database"""
        self.print_banner()
        print(self.color_text("\n[ ADD COOKIES TO DATABASE ]", 'yellow'))
        print(self.color_text("=" * 40, 'grey'))
        
        while True:
            try:
                num_cookies = int(self.get_user_input(
                    "How many cookies to add? ", 
                    'cyan'
                ))
                if num_cookies > 0:
                    break
                print(self.color_text("Please enter a positive number!", 'red'))
            except ValueError:
                print(self.color_text("Invalid input! Enter a number.", 'red'))
        
        added = 0
        for i in range(num_cookies):
            print(self.color_text(f"\n--- Cookie #{i+1} ---", 'magenta'))
            
            cookie_string = self.get_user_input(
                "Paste cookie string:", 
                'green',
                speak=False
            )
            
            self.loading_animation(2, f"Processing cookie {i+1}")
            
            cookies = self.validate_cookie_format(cookie_string)
            if not cookies:
                print(self.color_text("✗ Invalid cookie format!", 'red'))
                continue
            
            token = self.extract_token(cookies)
            if token:
                self.tokens.append(token)
                self.cookies_list.append(cookies)
                added += 1
                print(self.color_text(f"✓ Token extracted: {token[:20]}...", 'green'))
            else:
                print(self.color_text("✗ Failed to extract token!", 'red'))
        
        if added > 0:
            self.save_database()
            print(self.color_text(f"\n✓ Successfully added {added} cookies!", 'green'))
        else:
            print(self.color_text("\n✗ No valid cookies added!", 'red'))
        
        self.get_user_input("\nPress Enter to continue...", 'grey', speak=False)
    
    def view_database(self):
        """View and manage cookie database"""
        self.print_banner()
        print(self.color_text("\n[ DATABASE MANAGEMENT ]", 'yellow'))
        print(self.color_text("=" * 40, 'grey'))
        
        if not self.load_database():
            print(self.color_text("\nNo database found!", 'red'))
            self.get_user_input("Press Enter to continue...", 'grey', speak=False)
            return
        
        total = len(self.cookies_list)
        print(self.color_text(f"\nTotal cookies: {total}", 'cyan'))
        
        if total == 0:
            print(self.color_text("Database is empty!", 'yellow'))
            self.get_user_input("Press Enter to continue...", 'grey', speak=False)
            return
        
        print(self.color_text("\nCookie List:", 'green'))
        print(self.color_text("-" * 50, 'grey'))
        
        for i, (token, cookie) in enumerate(zip(self.tokens, self.cookies_list), 1):
            print(self.color_text(f"{i}. Token: {token[:20]}...", 'cyan'))
            print(self.color_text(f"   Keys: {', '.join(cookie.keys())[:50]}...", 'grey'))
        
        print(self.color_text("\nOptions:", 'yellow'))
        print(self.color_text("1. Remove specific cookies", 'green'))
        print(self.color_text("2. Remove all cookies", 'red'))
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
                        self.cookies_list.pop(idx)
                
                self.save_database()
                print(self.color_text(f"✓ Removed {len(to_remove)} cookies!", 'green'))
            except:
                print(self.color_text("✗ Invalid input!", 'red'))
        
        elif choice == '2':
            confirm = self.get_user_input(
                "Delete ALL cookies? (yes/no):", 
                'red'
            ).lower()
            
            if confirm == 'yes':
                self.tokens = []
                self.cookies_list = []
                self.save_database()
                print(self.color_text("✓ Database cleared!", 'green'))
        
        self.get_user_input("\nPress Enter to continue...", 'grey', speak=False)
    
    def share_single(self, token, cookie, link, share_num, start_time):
        """Share a single post"""
        headers = {
            "user-agent": random.choice(UA_LIST),
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded"
        }
        
        try:
            # Random delay to avoid detection
            time.sleep(random.uniform(1, 3))
            
            response = ses.post(
                f"https://graph.facebook.com/v17.0/me/feed",
                params={
                    "link": link,
                    "published": "0",
                    "access_token": token
                },
                headers=headers,
                cookies=cookie,
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
                
                if any(word in error.lower() for word in ['suspended', 'blocked', 'rate limit']):
                    print(self.color_text(f"[{share_num:4d}] ✗ Account suspended!", 'red'))
                    with self.lock:
                        if cookie not in self.suspended_cookies:
                            self.suspended_cookies.append(cookie)
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
        """Main sharing session"""
        self.print_banner()
        print(self.color_text("\n[ SHARING SESSION ]", 'yellow'))
        print(self.color_text("=" * 40, 'grey'))
        
        # Load database
        if not self.load_database() or not self.tokens:
            print(self.color_text("\nNo cookies in database!", 'red'))
            print(self.color_text("Please add cookies first.", 'yellow'))
            self.get_user_input("Press Enter to continue...", 'grey', speak=False)
            return
        
        total_cookies = len(self.tokens)
        print(self.color_text(f"\nLoaded {total_cookies} cookies from database", 'green'))
        
        # Get post link
        print(self.color_text("\nPost Link Examples:", 'cyan'))
        print(self.color_text("• Facebook post: https://facebook.com/username/posts/123...", 'grey'))
        print(self.color_text("• Video link: https://fb.watch/xxxxx/", 'grey'))
        
        while True:
            link = self.get_user_input(
                "\nEnter post link to share:", 
                'green',
                speak=False
            )
            
            if link.startswith(('http://', 'https://')):
                break
            print(self.color_text("Invalid link! Must start with http:// or https://", 'red'))
        
        # Get share count
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
        self.suspended_cookies = []
        
        successful = 0
        failed = 0
        
        # Process in chunks to avoid rate limiting
        chunk_size = 100
        cooldown = 5
        
        with ThreadPoolExecutor(max_workers=30) as executor:
            for chunk_start in range(0, shares, chunk_size):
                chunk_end = min(chunk_start + chunk_size, shares)
                futures = []
                
                for share_num in range(chunk_start + 1, chunk_end + 1):
                    # Filter out suspended cookies
                    active_indices = [
                        i for i, c in enumerate(self.cookies_list) 
                        if c not in self.suspended_cookies
                    ]
                    
                    if not active_indices:
                        print(self.color_text("\n✗ All accounts suspended!", 'red'))
                        break
                    
                    # Randomly select active cookie
                    idx = random.choice(active_indices)
                    
                    future = executor.submit(
                        self.share_single,
                        self.tokens[idx],
                        self.cookies_list[idx],
                        link,
                        share_num,
                        start_time
                    )
                    futures.append(future)
                
                # Wait for chunk to complete
                for future in as_completed(futures):
                    if future.result():
                        successful += 1
                    else:
                        failed += 1
                
                # Cooldown between chunks
                if chunk_end < shares:
                    print(self.color_text(
                        f"\n⏳ Cooldown for {cooldown} seconds...", 
                        'yellow'
                    ))
                    time.sleep(cooldown)
        
        # Remove suspended cookies
        if self.suspended_cookies:
            print(self.color_text("\nCleaning suspended accounts...", 'yellow'))
            
            clean_tokens = []
            clean_cookies = []
            
            for i, cookie in enumerate(self.cookies_list):
                if cookie not in self.suspended_cookies:
                    clean_tokens.append(self.tokens[i])
                    clean_cookies.append(cookie)
            
            self.tokens = clean_tokens
            self.cookies_list = clean_cookies
            self.save_database()
            
            print(self.color_text(
                f"Removed {len(self.suspended_cookies)} suspended accounts", 
                'green'
            ))
        
        # Show statistics
        elapsed = str(datetime.now() - start_time).split('.')[0]
        print(self.color_text("\n" + "═" * 50, 'grey'))
        print(self.color_text("SESSION COMPLETE!", 'yellow'))
        print(self.color_text("═" * 50, 'grey'))
        print(self.color_text(f"Time elapsed: {elapsed}", 'cyan'))
        print(self.color_text(f"Successful: {successful}", 'green'))
        print(self.color_text(f"Failed: {failed}", 'red'))
        
        # Avoid division by zero
        if successful + failed > 0:
            success_rate = (successful/(successful+failed))*100
            print(self.color_text(f"Success rate: {success_rate:.1f}%", 'cyan'))
        
        self.get_user_input("\nPress Enter to continue...", 'grey', speak=False)
    
    def run(self):
        """Main program loop"""
        while self.running:
            self.print_banner()
            
            print(self.color_text("\n[ MAIN MENU ]", 'yellow'))
            print(self.color_text("═" * 40, 'grey'))
            print(self.color_text("1. 📝 Add Cookies to Database", 'green'))
            print(self.color_text("2. 📋 View/Manage Database", 'cyan'))
            print(self.color_text("3. 🚀 Start Sharing Session", 'magenta'))
            print(self.color_text("4. ❌ Exit Program", 'red'))
            print(self.color_text("═" * 40, 'grey'))
            
            choice = self.get_user_input("Select option (1-4):", 'yellow')
            
            if choice == '1':
                self.add_cookies_manual()
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

# Main execution - FIXED HERE
if __name__ == "__main__":
    try:
        # Check Python version
        if sys.version_info < (3, 6):
            print("\033[91mPlease use Python 3.6 or higher!\033[0m")
            sys.exit(1)
        
        # Create and run bot
        bot = FacebookSpamBot()
        bot.run()
        
    except KeyboardInterrupt:
        print("\n\n\033[93mProgram interrupted by user!\033[0m")
        print("\033[92mGoodbye! 👋\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91mUnexpected error: {e}\033[0m")
        print("\033[93mPlease report this issue to the developer.\033[0m")
        sys.exit(1)
