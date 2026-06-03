import os
import subprocess
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import json
import re
import time
from datetime import datetime

GEMINI_API_KEY = "AIzaSyC5FqED85-vHdCgUEQ_YWCNXc1wZshvXBQ"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 0.9)

BLOCKED_PATTERNS = [
    r'\brm\b', r'\bdelete\b', r'\bremove\b', r'\bmv\b', r'\bcp\b',
    r'\bchmod\b', r'\bchown\b', r'\bmount\b', r'\bumount\b',
    r'\bfdisk\b', r'\bmkfs\b', r'\bdd\b', r'\bformat\b',
    r'\breboot\b', r'\bshutdown\b', r'\bpoweroff\b',
    r'/system', r'/data', r'/root', r'/etc'
]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    try:
        return recognizer.recognize_google(audio).lower()
    except:
        return None

def is_safe_command(command):
    command_lower = command.lower()
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command_lower):
            return False
    return True

def execute_shizuku(cmd):
    try:
        result = subprocess.run(
            f"sh -c 'export CLASSPATH=/data/local/tmp/shizuku.dex && app_process /system/bin com.rosan.su.SuShell {cmd}'",
            shell=True, capture_output=True, text=True, timeout=10
        )
        return result.stdout if result.stdout else result.stderr
    except:
        return None

def execute_adb(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout if result.stdout else result.stderr
    except:
        return None

def tap(x, y):
    execute_shizuku(f"input tap {x} {y}")

def swipe(x1, y1, x2, y2, duration=300):
    execute_shizuku(f"input swipe {x1} {y1} {x2} {y2} {duration}")

def type_text(text):
    text = text.replace(" ", "%s").replace("'", "\\'")
    execute_shizuku(f"input text '{text}'")

def key_event(code):
    execute_shizuku(f"input keyevent {code}")

def open_app(package_name):
    execute_shizuku(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")

def get_installed_packages():
    return execute_shizuku("pm list packages")

def search_package(query):
    packages = get_installed_packages()
    if packages:
        for line in packages.split('\n'):
            if "package:" in line and query.lower() in line.lower():
                return line.replace("package:", "").strip()
    return None

def get_contacts():
    contacts = execute_shizuku("content query --uri content://contacts/phones/")
    return contacts

def send_facebook_message(contact_name, message):
    open_app("com.facebook.katana")
    time.sleep(3)
    tap(540, 2200)
    time.sleep(1)
    type_text(contact_name)
    time.sleep(2)
    tap(540, 400)
    time.sleep(2)
    tap(540, 2000)
    time.sleep(1)
    type_text(message)
    time.sleep(1)
    key_event(66)
    speak(f"Message sent to {contact_name}")

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

def open_youtube_search(query):
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

def youtube_play_pause():
    key_event(85)

def youtube_next():
    key_event(87)

def youtube_previous():
    key_event(88)

def youtube_volume_up():
    key_event(24)

def youtube_volume_down():
    key_event(25)

def open_tiktok():
    open_app("com.ss.android.ugc.trill")
    time.sleep(4)

def tiktok_scroll_next():
    swipe(540, 1500, 540, 400, 200)

def tiktok_scroll_previous():
    swipe(540, 400, 540, 1500, 200)

def tiktok_pause():
    tap(540, 1200)

def tiktok_like():
    tap(900, 1400)

def tiktok_comment():
    tap(540, 2000)

def tiktok_share():
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

def open_spotify():
    open_app("com.spotify.music")
    time.sleep(4)

def spotify_search_play(query):
    open_spotify()
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

def spotify_play_pause():
    key_event(85)

def spotify_next():
    key_event(87)

def spotify_previous():
    key_event(88)

def spotify_volume_up():
    key_event(24)

def spotify_volume_down():
    key_event(25)

def spotify_like():
    tap(900, 1700)

def adjust_volume(level):
    for _ in range(level):
        key_event(24)

def lower_volume(level):
    for _ in range(level):
        key_event(25)

def mute_volume():
    key_event(164)

def unmute_volume():
    key_event(164)

def set_brightness(level):
    execute_shizuku(f"settings put system screen_brightness {level}")

def get_brightness():
    return execute_shizuku("settings get system screen_brightness")

def call_contact(contact_name):
    contacts = get_contacts()
    if contacts:
        for line in contacts.split('\n'):
            if contact_name.lower() in line.lower():
                number_match = re.search(r'number=([\d+]+)', line)
                if number_match:
                    number = number_match.group(1)
                    execute_shizuku(f"am start -a android.intent.action.CALL -d tel:{number}")
                    return f"Calling {contact_name}"
    return "Contact not found"

def send_sms(contact_name, message):
    contacts = get_contacts()
    if contacts:
        for line in contacts.split('\n'):
            if contact_name.lower() in line.lower():
                number_match = re.search(r'number=([\d+]+)', line)
                if number_match:
                    number = number_match.group(1)
                    execute_shizuku(f"service call isms 7 i32 1 s16 '{number}' s16 null s16 '{message}' s16 null s16 null")
                    return f"SMS sent to {contact_name}"
    return "Contact not found"

def open_camera():
    execute_shizuku("am start -a android.media.action.STILL_IMAGE_CAMERA")

def take_photo():
    key_event(27)

def open_gallery():
    execute_shizuku("am start -a android.intent.action.VIEW -t image/*")

def get_battery_info():
    return execute_shizuku("dumpsys battery | grep level")

def get_wifi_status():
    return execute_shizuku("dumpsys wifi | grep 'Wi-Fi is'")

def toggle_wifi():
    execute_shizuku("svc wifi enable")
    time.sleep(1)
    status = get_wifi_status()
    if "enabled" in str(status):
        execute_shizuku("svc wifi disable")
    else:
        execute_shizuku("svc wifi enable")

def toggle_bluetooth():
    execute_shizuku("svc bluetooth enable")
    time.sleep(1)
    status = execute_shizuku("settings get global bluetooth_on")
    if "1" in str(status):
        execute_shizuku("svc bluetooth disable")
    else:
        execute_shizuku("svc bluetooth enable")

def toggle_flashlight():
    status = execute_shizuku("cat /sys/class/leds/flashlight/brightness")
    if status and "1" in status:
        execute_shizuku("echo 0 > /sys/class/leds/flashlight/brightness")
    else:
        execute_shizuku("echo 1 > /sys/class/leds/flashlight/brightness")

def take_screenshot():
    execute_shizuku("screencap -p /sdcard/screenshot.png")

def get_clipboard():
    return execute_shizuku("cmd clipboard get-text")

def set_clipboard(text):
    execute_shizuku(f"cmd clipboard set-text '{text}'")

def get_time_date():
    return datetime.now().strftime("%I:%M %p, %B %d %Y")

def get_storage_info():
    return execute_shizuku("df -h /sdcard")

def get_system_info():
    cpu = execute_shizuku("cat /proc/cpuinfo | grep 'Hardware'")
    mem = execute_shizuku("cat /proc/meminfo | grep 'MemTotal'")
    return f"CPU: {cpu}\nMemory: {mem}"

def go_home():
    key_event(3)

def go_back():
    key_event(4)

def recent_apps():
    key_event(187)

def notifications():
    swipe(540, 10, 540, 800, 200)

def quick_settings():
    swipe(540, 10, 540, 400, 100)

def lock_screen():
    execute_shizuku("input keyevent 26")

def process_command_with_ai(command):
    prompt = f"""
    You are a mobile voice assistant. Parse command and return JSON:
    {{"action": "action_name", "params": {{}}, "response": "response text"}}
    
    Available actions:
    open_app, open_youtube, youtube_play, youtube_pause, youtube_next, youtube_previous,
    youtube_volume_up, youtube_volume_down, youtube_search,
    open_tiktok, tiktok_scroll, tiktok_pause, tiktok_like, tiktok_comment, tiktok_share,
    tiktok_search, tiktok_next, tiktok_previous,
    open_spotify, spotify_search, spotify_play, spotify_pause, spotify_next, spotify_previous,
    spotify_volume_up, spotify_volume_down, spotify_like,
    facebook_message, facebook_post,
    send_sms, call_contact,
    volume_up, volume_down, mute, unmute, set_volume, set_brightness,
    open_camera, take_photo, open_gallery,
    battery_status, wifi_toggle, bluetooth_toggle, flashlight_toggle,
    screenshot, clipboard_get, clipboard_set,
    time_date, storage_info, system_info,
    go_home, go_back, recent_apps, notifications, quick_settings, lock_screen,
    help
    
    Command: {command}
    
    For open_app: extract app name to params.app_name
    For facebook_message: extract contact to params.contact and message to params.message
    For facebook_post: extract text to params.text
    For youtube_search: extract query to params.query
    For tiktok_search: extract query to params.query
    For spotify_search: extract query to params.query
    For send_sms: extract contact to params.contact and message to params.message
    For call_contact: extract contact to params.contact
    For set_volume: extract level (0-100) to params.level
    For set_brightness: extract level (0-255) to params.level
    For clipboard_set: extract text to params.text
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
    
    if action == "open_app":
        query = params.get("app_name", "")
        pkg = search_package(query)
        if pkg:
            open_app(pkg)
            return f"Opening {query}"
        return "App not found"
    
    elif action == "facebook_message":
        send_facebook_message(params.get("contact", ""), params.get("message", ""))
        return f"Message sent to {params.get('contact', 'contact')}"
    
    elif action == "facebook_post":
        write_facebook_post(params.get("text", ""))
        return "Post shared"
    
    elif action == "open_youtube":
        open_app("com.google.android.youtube")
        time.sleep(3)
        return "YouTube opened"
    
    elif action == "youtube_search":
        open_youtube_search(params.get("query", ""))
        return f"Searching {params.get('query', '')}"
    
    elif action == "youtube_play":
        youtube_play_pause()
        return "Playing"
    
    elif action == "youtube_pause":
        youtube_play_pause()
        return "Paused"
    
    elif action == "youtube_next":
        youtube_next()
        return "Next video"
    
    elif action == "youtube_previous":
        youtube_previous()
        return "Previous video"
    
    elif action == "youtube_volume_up":
        youtube_volume_up()
        return "Volume up"
    
    elif action == "youtube_volume_down":
        youtube_volume_down()
        return "Volume down"
    
    elif action == "open_tiktok":
        open_tiktok()
        return "TikTok opened"
    
    elif action == "tiktok_scroll":
        tiktok_scroll_next()
        return "Scrolling"
    
    elif action == "tiktok_next":
        tiktok_scroll_next()
        return "Next video"
    
    elif action == "tiktok_previous":
        tiktok_scroll_previous()
        return "Previous video"
    
    elif action == "tiktok_pause":
        tiktok_pause()
        return "Paused"
    
    elif action == "tiktok_like":
        tiktok_like()
        return "Liked"
    
    elif action == "tiktok_comment":
        tiktok_comment()
        return "Opening comments"
    
    elif action == "tiktok_share":
        tiktok_share()
        return "Opening share"
    
    elif action == "tiktok_search":
        tiktok_search(params.get("query", ""))
        return f"Searching {params.get('query', '')}"
    
    elif action == "open_spotify":
        open_spotify()
        return "Spotify opened"
    
    elif action == "spotify_search":
        spotify_search_play(params.get("query", ""))
        return f"Playing {params.get('query', '')}"
    
    elif action == "spotify_play":
        spotify_play_pause()
        return "Playing"
    
    elif action == "spotify_pause":
        spotify_play_pause()
        return "Paused"
    
    elif action == "spotify_next":
        spotify_next()
        return "Next track"
    
    elif action == "spotify_previous":
        spotify_previous()
        return "Previous track"
    
    elif action == "spotify_volume_up":
        spotify_volume_up()
        return "Volume up"
    
    elif action == "spotify_volume_down":
        spotify_volume_down()
        return "Volume down"
    
    elif action == "spotify_like":
        spotify_like()
        return "Track liked"
    
    elif action == "send_sms":
        result = send_sms(params.get("contact", ""), params.get("message", ""))
        return result
    
    elif action == "call_contact":
        result = call_contact(params.get("contact", ""))
        return result
    
    elif action == "volume_up":
        key_event(24)
        return "Volume increased"
    
    elif action == "volume_down":
        key_event(25)
        return "Volume decreased"
    
    elif action == "mute":
        mute_volume()
        return "Muted"
    
    elif action == "unmute":
        unmute_volume()
        return "Unmuted"
    
    elif action == "set_volume":
        level = int(params.get("level", 50))
        current = int(execute_shizuku("settings get system volume_music_speaker") or "10")
        diff = level // 6 - current
        if diff > 0:
            for _ in range(diff):
                key_event(24)
        else:
            for _ in range(abs(diff)):
                key_event(25)
        return f"Volume set to {level}%"
    
    elif action == "set_brightness":
        level = int(params.get("level", 128))
        set_brightness(level)
        return f"Brightness set to {level}"
    
    elif action == "open_camera":
        open_camera()
        return "Camera opened"
    
    elif action == "take_photo":
        take_photo()
        return "Photo taken"
    
    elif action == "open_gallery":
        open_gallery()
        return "Gallery opened"
    
    elif action == "battery_status":
        info = get_battery_info()
        return f"Battery {info}" if info else "Cannot get battery"
    
    elif action == "wifi_toggle":
        toggle_wifi()
        return "WiFi toggled"
    
    elif action == "bluetooth_toggle":
        toggle_bluetooth()
        return "Bluetooth toggled"
    
    elif action == "flashlight_toggle":
        toggle_flashlight()
        return "Flashlight toggled"
    
    elif action == "screenshot":
        take_screenshot()
        return "Screenshot saved"
    
    elif action == "clipboard_get":
        text = get_clipboard()
        return text if text else "Clipboard empty"
    
    elif action == "clipboard_set":
        set_clipboard(params.get("text", ""))
        return "Text copied to clipboard"
    
    elif action == "time_date":
        return get_time_date()
    
    elif action == "storage_info":
        info = get_storage_info()
        return info[:300] if info else "Cannot get storage"
    
    elif action == "system_info":
        return get_system_info()[:300]
    
    elif action == "go_home":
        go_home()
        return "Home"
    
    elif action == "go_back":
        go_back()
        return "Back"
    
    elif action == "recent_apps":
        recent_apps()
        return "Recent apps"
    
    elif action == "notifications":
        notifications()
        return "Notifications"
    
    elif action == "quick_settings":
        quick_settings()
        return "Quick settings"
    
    elif action == "lock_screen":
        lock_screen()
        return "Screen locked"
    
    elif action == "help":
        return "I can control YouTube, TikTok, Spotify, Facebook, send messages, make calls, adjust volume, brightness, camera, flashlight, WiFi, Bluetooth, take screenshots, manage clipboard and more"
    
    return "Action not implemented"

def main():
    speak("Jarvis online. All systems ready")
    
    while True:
        command = listen()
        
        if not command:
            continue
        
        if any(word in command for word in ["exit", "quit", "shutdown", "goodbye"]):
            speak("Goodbye")
            break
        
        if not is_safe_command(command):
            speak("Security restriction active")
            continue
        
        action_data = process_command_with_ai(command)
        result = execute_action(action_data)
        
        if result:
            speak(str(result)[:200])

if __name__ == "__main__":
    main()
