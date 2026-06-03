import subprocess
import sys
import os
import time

def install_dependencies():
    packages = [
        "python",
        "python-pip",
        "termux-api",
        "binutils",
        "build-essential",
        "rust",
        "cargo",
        "cmake",
        "libffi",
        "openssl",
        "openjdk-17"
    ]
    
    for pkg in packages:
        subprocess.run(f"pkg install {pkg} -y", shell=True)
    
    subprocess.run("pip install --upgrade pip setuptools wheel", shell=True)
    
    pip_packages = [
        "SpeechRecognition",
        "pyttsx3==2.90",
        "google-generativeai",
        "cryptography==41.0.7",
        "cffi==1.16.0",
        "pycparser==2.21"
    ]
    
    for pkg in pip_packages:
        subprocess.run(f"pip install {pkg} --no-deps || pip install {pkg}", shell=True)
    
    subprocess.run("pip install pyttsx3 google-generativeai SpeechRecognition", shell=True)

try:
    import speech_recognition as sr
    import google.generativeai as genai
    import pyttsx3
except ImportError:
    install_dependencies()
    import speech_recognition as sr
    import google.generativeai as genai
    import pyttsx3

import json
import re
from datetime import datetime

GEMINI_API_KEY = "AIzaSyC5FqED85-vHdCgUEQ_YWCNXc1wZshvXBQ"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

recognizer = sr.Recognizer()

engine = None
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 0.9)
except:
    pass

BLOCKED_PATTERNS = [
    r'\brm\b', r'\bdelete\b', r'\bremove\b', r'\bmv\b', r'\bcp\b',
    r'\bchmod\b', r'\bchown\b', r'\bmount\b', r'\bumount\b',
    r'\bfdisk\b', r'\bmkfs\b', r'\bdd\b', r'\bformat\b',
    r'\breboot\b', r'\bshutdown\b', r'\bpoweroff\b',
    r'/system', r'/data', r'/root', r'/etc'
]

def speak(text):
    if engine:
        try:
            engine.say(str(text)[:200])
            engine.runAndWait()
        except:
            print(f"JARVIS: {text}")
    else:
        print(f"JARVIS: {text}")

def listen():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        command = recognizer.recognize_google(audio).lower()
        print(f"You: {command}")
        return command
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        speak("Network error")
        return None
    except:
        return None

def is_safe_command(command):
    command_lower = command.lower()
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command_lower):
            return False
    return True

def shizuku_execute(cmd):
    try:
        result = subprocess.run(
            f"sh -c 'export CLASSPATH=/data/local/tmp/shizuku.dex && app_process /system/bin com.rosan.su.SuShell {cmd}'",
            shell=True, capture_output=True, text=True, timeout=10
        )
        return result.stdout if result.stdout else result.stderr
    except:
        return None

def tap(x, y):
    shizuku_execute(f"input tap {x} {y}")

def swipe(x1, y1, x2, y2, duration=300):
    shizuku_execute(f"input swipe {x1} {y1} {x2} {y2} {duration}")

def type_text(text):
    text = text.replace(" ", "%s").replace("'", "\\'")
    shizuku_execute(f"input text '{text}'")

def key_event(code):
    shizuku_execute(f"input keyevent {code}")

def open_app(package_name):
    shizuku_execute(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")

def get_packages():
    result = shizuku_execute("pm list packages")
    return result if result else ""

def find_package(query):
    packages = get_packages()
    if packages:
        for line in packages.split('\n'):
            if "package:" in line and query.lower() in line.lower():
                return line.replace("package:", "").strip()
    return None

def send_facebook_message(contact, message):
    open_app("com.facebook.katana")
    time.sleep(3)
    tap(540, 2200)
    time.sleep(1)
    type_text(contact)
    time.sleep(2)
    tap(540, 400)
    time.sleep(2)
    tap(540, 2000)
    time.sleep(1)
    type_text(message)
    time.sleep(1)
    key_event(66)
    speak(f"Message sent to {contact}")

def write_facebook_post(text):
    open_app("com.facebook.katana")
    time.sleep(3)
    tap(540, 2000)
    time.sleep(2)
    tap(540, 1800)
    time.sleep(1)
    type_text(text)
    time.sleep(1)
    tap(980, 200)
    speak("Post shared")

def youtube_search_play(query):
    open_app("com.google.android.youtube")
    time.sleep(3)
    tap(950, 150)
    time.sleep(2)
    type_text(query)
    time.sleep(1)
    key_event(66)
    time.sleep(2)
    tap(540, 600)
    speak(f"Playing {query}")

def youtube_control(action):
    if action == "play_pause":
        key_event(85)
    elif action == "next":
        key_event(87)
    elif action == "previous":
        key_event(88)
    elif action == "vol_up":
        key_event(24)
    elif action == "vol_down":
        key_event(25)

def open_tiktok():
    open_app("com.ss.android.ugc.trill")
    time.sleep(4)

def tiktok_scroll(direction="next"):
    if direction == "next":
        swipe(540, 1500, 540, 400, 200)
    else:
        swipe(540, 400, 540, 1500, 200)

def tiktok_interact(action):
    if action == "pause":
        tap(540, 1200)
    elif action == "like":
        tap(900, 1400)
    elif action == "comment":
        tap(540, 2000)
    elif action == "share":
        tap(980, 1400)

def tiktok_search(query):
    open_tiktok()
    time.sleep(4)
    tap(950, 150)
    time.sleep(1)
    type_text(query)
    time.sleep(1)
    key_event(66)
    time.sleep(2)
    tap(540, 600)

def spotify_search_play(query):
    open_app("com.spotify.music")
    time.sleep(4)
    tap(950, 150)
    time.sleep(1)
    type_text(query)
    time.sleep(1)
    key_event(66)
    time.sleep(2)
    tap(540, 500)
    time.sleep(2)
    tap(540, 600)
    speak(f"Playing {query}")

def spotify_control(action):
    if action == "play_pause":
        key_event(85)
    elif action == "next":
        key_event(87)
    elif action == "previous":
        key_event(88)
    elif action == "vol_up":
        key_event(24)
    elif action == "vol_down":
        key_event(25)
    elif action == "like":
        tap(900, 1700)

def adjust_volume(level):
    for _ in range(int(level/10)):
        key_event(24)

def lower_volume(level):
    for _ in range(int(level/10)):
        key_event(25)

def set_brightness(level):
    shizuku_execute(f"settings put system screen_brightness {level}")

def toggle_flashlight():
    status = shizuku_execute("cat /sys/class/leds/flashlight/brightness")
    if status and "1" in str(status):
        shizuku_execute("echo 0 > /sys/class/leds/flashlight/brightness")
    else:
        shizuku_execute("echo 1 > /sys/class/leds/flashlight/brightness")

def take_screenshot():
    shizuku_execute("screencap -p /sdcard/screenshot.png")

def get_clipboard():
    result = shizuku_execute("cmd clipboard get-text")
    return result if result else "Clipboard empty"

def set_clipboard(text):
    shizuku_execute(f"cmd clipboard set-text '{text}'")

def call_contact(contact):
    contacts = shizuku_execute("content query --uri content://contacts/phones/")
    if contacts:
        for line in contacts.split('\n'):
            if contact.lower() in line.lower():
                number_match = re.search(r'number=([\d+]+)', line)
                if number_match:
                    number = number_match.group(1)
                    shizuku_execute(f"am start -a android.intent.action.CALL -d tel:{number}")
                    return f"Calling {contact}"
    return "Contact not found"

def send_sms(contact, message):
    contacts = shizuku_execute("content query --uri content://contacts/phones/")
    if contacts:
        for line in contacts.split('\n'):
            if contact.lower() in line.lower():
                number_match = re.search(r'number=([\d+]+)', line)
                if number_match:
                    number = number_match.group(1)
                    shizuku_execute(f"service call isms 7 i32 1 s16 '{number}' s16 null s16 '{message}' s16 null s16 null")
                    return f"SMS sent to {contact}"
    return "Contact not found"

def get_battery():
    result = shizuku_execute("dumpsys battery | grep level")
    return f"Battery {result}" if result else "Cannot get battery"

def toggle_wifi():
    shizuku_execute("svc wifi enable")
    time.sleep(1)
    status = shizuku_execute("dumpsys wifi | grep 'Wi-Fi is'")
    if "enabled" in str(status):
        shizuku_execute("svc wifi disable")
    else:
        shizuku_execute("svc wifi enable")

def toggle_bluetooth():
    shizuku_execute("svc bluetooth enable")
    time.sleep(1)
    status = shizuku_execute("settings get global bluetooth_on")
    if "1" in str(status):
        shizuku_execute("svc bluetooth disable")
    else:
        shizuku_execute("svc bluetooth enable")

def get_time_date():
    return datetime.now().strftime("%I:%M %p, %B %d %Y")

def get_storage():
    result = shizuku_execute("df -h /sdcard")
    return result[:300] if result else "Cannot get storage"

def process_command(command):
    prompt = f"""
    Parse this voice command and return ONLY valid JSON:
    {{"action": "action_name", "params": {{}}, "response": "reply text"}}
    
    Available actions:
    open_app, youtube_search, youtube_play, youtube_pause, youtube_next, 
    youtube_previous, youtube_vol_up, youtube_vol_down,
    tiktok_open, tiktok_search, tiktok_scroll, tiktok_pause, tiktok_like,
    tiktok_comment, tiktok_share, tiktok_previous,
    spotify_search, spotify_play, spotify_pause, spotify_next, spotify_previous,
    spotify_vol_up, spotify_vol_down, spotify_like,
    facebook_message, facebook_post,
    call_contact, send_sms,
    volume_up, volume_down, mute, set_brightness,
    flashlight, screenshot, clipboard_get, clipboard_set,
    battery, wifi_toggle, bluetooth_toggle,
    time_date, storage, go_home, go_back, recent_apps, lock_screen, help
    
    Command: {command}
    """
    
    try:
        response = model.generate_content(prompt)
        clean = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(clean)
    except:
        return {"action": "unknown", "response": "I didn't understand"}

def execute_action(action_data):
    action = action_data.get("action")
    params = action_data.get("params", {})
    
    actions_map = {
        "open_app": lambda: open_app(find_package(params.get("app_name", "")) or params.get("app_name", "")),
        "youtube_search": lambda: youtube_search_play(params.get("query", "")),
        "youtube_play": lambda: youtube_control("play_pause"),
        "youtube_pause": lambda: youtube_control("play_pause"),
        "youtube_next": lambda: youtube_control("next"),
        "youtube_previous": lambda: youtube_control("previous"),
        "youtube_vol_up": lambda: youtube_control("vol_up"),
        "youtube_vol_down": lambda: youtube_control("vol_down"),
        "tiktok_open": lambda: open_tiktok(),
        "tiktok_search": lambda: tiktok_search(params.get("query", "")),
        "tiktok_scroll": lambda: tiktok_scroll("next"),
        "tiktok_previous": lambda: tiktok_scroll("previous"),
        "tiktok_pause": lambda: tiktok_interact("pause"),
        "tiktok_like": lambda: tiktok_interact("like"),
        "tiktok_comment": lambda: tiktok_interact("comment"),
        "tiktok_share": lambda: tiktok_interact("share"),
        "spotify_search": lambda: spotify_search_play(params.get("query", "")),
        "spotify_play": lambda: spotify_control("play_pause"),
        "spotify_pause": lambda: spotify_control("play_pause"),
        "spotify_next": lambda: spotify_control("next"),
        "spotify_previous": lambda: spotify_control("previous"),
        "spotify_vol_up": lambda: spotify_control("vol_up"),
        "spotify_vol_down": lambda: spotify_control("vol_down"),
        "spotify_like": lambda: spotify_control("like"),
        "facebook_message": lambda: send_facebook_message(params.get("contact", ""), params.get("message", "")),
        "facebook_post": lambda: write_facebook_post(params.get("text", "")),
        "call_contact": lambda: call_contact(params.get("contact", "")),
        "send_sms": lambda: send_sms(params.get("contact", ""), params.get("message", "")),
        "volume_up": lambda: key_event(24),
        "volume_down": lambda: key_event(25),
        "mute": lambda: key_event(164),
        "set_brightness": lambda: set_brightness(int(params.get("level", 128))),
        "flashlight": lambda: toggle_flashlight(),
        "screenshot": lambda: take_screenshot(),
        "clipboard_get": lambda: get_clipboard(),
        "clipboard_set": lambda: set_clipboard(params.get("text", "")),
        "battery": lambda: get_battery(),
        "wifi_toggle": lambda: toggle_wifi(),
        "bluetooth_toggle": lambda: toggle_bluetooth(),
        "time_date": lambda: get_time_date(),
        "storage": lambda: get_storage(),
        "go_home": lambda: key_event(3),
        "go_back": lambda: key_event(4),
        "recent_apps": lambda: key_event(187),
        "lock_screen": lambda: key_event(26),
        "help": lambda: "All functions available. Ask me anything."
    }
    
    if action in actions_map:
        result = actions_map[action]()
        if result:
            return str(result)
        return action_data.get("response", "Done")
    return action_data.get("response", "Action not available")

def check_shizuku():
    result = shizuku_execute("echo test")
    if result and "test" in result:
        return True
    print("Shizuku not running. Start Shizuku app first.")
    speak("Please start Shizuku app and enable service")
    return False

def main():
    print("Initializing JARVIS...")
    
    if not check_shizuku():
        sys.exit(1)
    
    speak("Jarvis online. All systems operational.")
    
    while True:
        command = listen()
        
        if not command:
            continue
        
        if any(word in command for word in ["exit", "quit", "goodbye", "shutdown"]):
            speak("Shutting down. Goodbye.")
            break
        
        if not is_safe_command(command):
            speak("Security restriction active")
            continue
        
        action_data = process_command(command)
        result = execute_action(action_data)
        
        if result:
            speak(str(result)[:200])

if __name__ == "__main__":
    main()
