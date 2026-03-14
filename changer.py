import requests
import json
import re
import random
import uuid
import base64
import time
import os
import sys

R = '\033[1;91m'
V = '\033[1;92m'
B = '\033[1;97m'
S = '\033[0m'
C = '\033[96m'
v = '\033[7;92m'
r = '\033[7;91m'
c = '\033[7;96m'
j = '\033[7;33m'
cy = "\033[38;5;50m"
rr = "\033[38;5;196m"
vv = "\033[38;5;46m"
jj = "\033[38;5;226m"
bb = "\033[38;5;15m"

logo = f'''
{rr}'    ███████╗███╗   ███╗ ██████╗      ██╗██╗███████╗    
{vv}'    ██╔════╝████╗ ████║██╔═══██╗     ██║██║██╔════╝    
{cy}'    █████╗  ██╔████╔██║██║   ██║     ██║██║█████╗      
{bb}'    ██╔══╝  ██║╚██╔╝██║██║   ██║██   ██║██║██╔══╝      
{jj}'    ███████╗██║ ╚═╝ ██║╚██████╔╝╚█████╔╝██║███████╗    
'    ╚══════╝╚═╝     ╚═╝ ╚═════╝  ╚════╝ ╚═╝╚══════╝   {S}'''

fb_link = "https://www.facebook.com/profile.php?id=61583439715339"
version = "Version 2.0 (Final Fixed)"

def clear():
    os.system('clear' if 'linux' in sys.platform.lower() else 'cls')

def platform():
    plat = sys.platform.lower()
    return plat

def checking(cookie):
    try:
        head = {
            "Host": "accountscenter.facebook.com",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-User": "?1"
        }
        url = "https://accountscenter.facebook.com/profiles"
        rq1 = requests.get(url, headers=head, allow_redirects=True, timeout=30)
        rp1 = rq1.text.replace("\\", "")
        final_url = rq1.url
        
        if final_url != "https://accountscenter.facebook.com/profiles":
            return {"status": "fail", "message": "Cookie Invalid or Expired"}
        
        # Get Instagram username
        ig_match = re.search(r'"identity_type"\s*:\s*"IG_USER".*?"username"\s*:\s*"([^"]+)"', str(rp1))
        if not ig_match:
            return {"status": "fail", "message": "Instagram Account Not Linked"}
        IG_uname = ig_match.group(1)
        
        # Get Facebook UID
        uid_match = re.search(r'"actorID"\s*:\s*"(\d+)"', str(rp1))
        if not uid_match:
            return {"status": "fail", "message": "Failed to get user_id"}
        uid = uid_match.group(1)
        
        return {"status": "success", "uid": uid, "ig_uname": IG_uname}
        
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except requests.exceptions.Timeout:
        return {"status": "fail", "message": "Request Timeout"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def get_tokens(cookie, uid):
    try:
        head = {
            "Host": "accountscenter.facebook.com",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-User": "?1"
        }
        url = f"https://accountscenter.facebook.com/connected_experiences/single_sign_on_dialog/{uid}"
        rq1 = requests.get(url, headers=head, timeout=30)
        rp1 = rq1.text.replace("\\", "")
        
        # Extract tokens
        dtsg_match = re.search(r'\["DTSGInitialData".*?\{[^}]*"token"\s*:\s*"([^"]+)"', str(rp1))
        lsd_match = re.search(r'\["LSD".*?"token"\s*:\s*"([^"]+)"', str(rp1))
        fbid_match = re.search(r'"__typename"\s*:\s*"XFBFXIGAccountInfo".*?"id"\s*:\s*"(\d+)"', str(rp1))
        
        if not all([dtsg_match, lsd_match, fbid_match]):
            return {"status": "fail", "message": "Failed to get tokens - Cookie may be invalid"}
            
        fb_dtsg = dtsg_match.group(1)
        lsd = lsd_match.group(1)
        fbid_v2 = fbid_match.group(1)
        
        return {"status": "success", "DTSG": fb_dtsg, "LSD": lsd, "fbid_v2": fbid_v2}
        
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except requests.exceptions.Timeout:
        return {"status": "fail", "message": "Request Timeout"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def change_instagram_name(cookie, uid, DTSG, LSD, fbid_v2, name):
    try:
        head = {
            "Host": "accountscenter.facebook.com",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://accountscenter.facebook.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept": "*/*",
            "Accept-Language": "en-US",
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "no-cache"
        }
        
        variable = {
            "client_mutation_id": str(uuid.uuid4()),
            "family_device_id": "device_id_fetch_datr",
            "identity_ids": [fbid_v2],
            "full_name": name,
            "first_name": name,
            "middle_name": "",
            "last_name": "",
            "interface": "FB_WEB"
        }
        
        data = {
            "locale": "en_US",
            "fb_api_caller_class": "RelayModern",
            "fb_dtsg": DTSG,
            "lsd": LSD,
            "fb_api_req_friendly_name": "useFXIMUpdateNameMutation",
            "variables": json.dumps(variable),
            "av": uid,
            "__user": uid,
            "server_timestamps": "true",
            "doc_id": "28573275658982428"
        }
        
        url = "https://accountscenter.facebook.com/api/graphql"
        response = requests.post(url, data=data, headers=head, timeout=30)
        
        try:
            rp1 = response.json()
        except:
            return {"status": "fail", "message": "Invalid response from server"}
        
        if "data" in rp1 and rp1["data"] is not None:
            return {"status": "success"}
        elif "errors" in rp1:
            error_msg = rp1["errors"][0].get("message", "Unknown error")
            if "try again later" in error_msg.lower():
                return {"status": "fail", "message": "Cannot change name, try again later"}
            elif "reauth" in error_msg.lower() or "relink" in error_msg.lower():
                return {"status": "fail", "message": "Please re-link your accounts"}
            else:
                return {"status": "fail", "message": f"Error: {error_msg}"}
        else:
            return {"status": "fail", "message": "Unknown error occurred"}
            
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except requests.exceptions.Timeout:
        return {"status": "fail", "message": "Request Timeout"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def sync_name_across_accounts(cookie, uid, DTSG, LSD, fbid_v2, name):
    try:
        head = {
            "Host": "accountscenter.facebook.com",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://accountscenter.facebook.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept": "*/*",
            "Accept-Language": "en-US",
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "no-cache"
        }
        
        variable = {
            "client_mutation_id": str(uuid.uuid4()),
            "accounts_to_sync": [fbid_v2, uid],
            "resources_to_sync": ["NAME", "PROFILE_PHOTO"],
            "resources_to_unsync": None,
            "scale": 3,
            "source_of_truth_array": [{"resource_source": "IG"}, {"resource_source": "FB"}],
            "source_account": uid,
            "family_device_id": "device_id_fetch_datr",
            "username_unsync_params": None,
            "platform": "FACEBOOK",
            "sync_logging_params": {"client_flow_type": "IM_SETTINGS"},
            "interface": "FB_WEB",
            "feta_profile_sync": False
        }
        
        data = {
            "locale": "en_US",
            "fb_dtsg": DTSG,
            "__user": uid,
            "variables": json.dumps(variable),
            "av": uid,
            "fb_api_req_friendly_name": "useFXIMUpdateNameMutation",
            "fb_api_caller_class": "RelayModern",
            "server_timestamps": "true",
            "doc_id": "9388416374608398"
        }
        
        url = "https://accountscenter.facebook.com/api/graphql"
        response = requests.post(url, data=data, headers=head, timeout=30)
        
        try:
            rp1 = response.json()
        except:
            return {"status": "fail", "message": "Invalid response from server"}
        
        if "data" in rp1 and rp1["data"] is not None:
            return {"status": "success"}
        elif "errors" in rp1:
            error_msg = rp1["errors"][0].get("message", "Unknown error")
            if "try again later" in error_msg.lower():
                return {"status": "fail", "message": "Cannot sync name, try again later"}
            elif "reauth" in error_msg.lower() or "relink" in error_msg.lower():
                return {"status": "fail", "message": "Please re-link your accounts"}
            else:
                return {"status": "fail", "message": f"Error: {error_msg}"}
        else:
            return {"status": "fail", "message": "Unknown error occurred"}
            
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except requests.exceptions.Timeout:
        return {"status": "fail", "message": "Request Timeout"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def main():
    try:
        clear()
        print(logo)
        print(f"{B}FB: {C}{fb_link}{S}")
        print(f"{B}{version}{S}")
        print("-" * 50)
        print()
        
        cookie = input(f"{B}[{R}?{B}] Facebook Cookie: {V}")
        
        clear()
        print(logo)
        print(f"{B}FB: {C}{fb_link}{S}")
        print(f"{B}{version}{S}")
        print("-" * 50)
        print()
        
        print(f"{B}[+] Verifying your Facebook cookie...{S}")
        check = checking(cookie=cookie)
        
        if check["status"] != "success":
            error_msgs = {
                "Cookie Invalid or Expired": "Your cookie is invalid or expired",
                "Instagram Account Not Linked": "Please link an Instagram account first and try again",
                "Failed to get user_id": "Your cookie is invalid or expired",
                "Connection Error": "No internet connection",
                "Request Timeout": "Request timeout, please try again"
            }
            print(f"{B}[{R}x{B}] {error_msgs.get(check['message'], check['message'])}{S}")
            return
        
        uid = check["uid"]
        ig_username = check["ig_uname"]
        
        print(f"{B}[{V}✓{B}] Your cookie is active{S}")
        print(f"{B}[+] Getting access tokens...{S}")
        
        tokens = get_tokens(cookie=cookie, uid=uid)
        
        if tokens["status"] != "success":
            error_msgs = {
                "Failed to get tokens - Cookie may be invalid": "Your cookie is invalid or expired",
                "Connection Error": "No internet connection",
                "Request Timeout": "Request timeout, please try again"
            }
            print(f"{B}[{R}x{B}] {error_msgs.get(tokens['message'], tokens['message'])}{S}")
            return
        
        DTSG = tokens["DTSG"]
        LSD = tokens["LSD"]
        fbid_v2 = tokens["fbid_v2"]
        
        print(f"{B}[{V}✓{B}] Tokens obtained successfully{S}")
        print()
        print(f"{B}[{V}!{B}] Instagram Username: {C}{ig_username}{S}")
        print(f"{B}[{V}!{B}] Facebook ID: {C}{uid}{S}")
        print(f"{B}[{V}!{B}] Instagram Account ID: {C}{fbid_v2}{S}")
        print()
        
        change_name = input(f"{B}[{R}?{B}] Do you want to change your Instagram name? (y/n): {V}")
        
        if change_name.lower() == 'y':
            new_name = input(f"{B}[{R}?{B}] Enter new name: {V}")
            
            print(f"{B}[+] Changing Instagram name to {C}{new_name}{B}...{S}")
            name_change = change_instagram_name(
                cookie=cookie, uid=uid, DTSG=DTSG, LSD=LSD, 
                fbid_v2=fbid_v2, name=new_name
            )
            
            if name_change["status"] == "success":
                print(f"{B}[{V}✓{B}] Name changed successfully on Instagram!{S}")
                
                print(f"{B}[+] Syncing name across both platforms...{S}")
                sync = sync_name_across_accounts(
                    cookie=cookie, uid=uid, DTSG=DTSG, LSD=LSD,
                    fbid_v2=fbid_v2, name=new_name
                )
                
                if sync["status"] == "success":
                    print(f"{B}[{V}✓{B}] Name synced successfully on both platforms!{S}")
                else:
                    error_msgs = {
                        "Cannot sync name, try again later": "Cannot sync name, try again later",
                        "Please re-link your accounts": "Please re-link your accounts",
                        "Connection Error": "No internet connection",
                        "Request Timeout": "Request timeout, please try again"
                    }
                    print(f"{B}[{R}x{B}] {error_msgs.get(sync['message'], sync['message'])}{S}")
                    print(f"{B}[{V}!{B}] Name was changed on Instagram but may not be synced to Facebook{S}")
            else:
                error_msgs = {
                    "Cannot change name, try again later": "Cannot change name, try again later",
                    "Please re-link your accounts": "Please re-link your accounts",
                    "Connection Error": "No internet connection",
                    "Request Timeout": "Request timeout, please try again"
                }
                print(f"{B}[{R}x{B}] {error_msgs.get(name_change['message'], name_change['message'])}{S}")
        
        print()
        print(f"{B}[{V}✓{B}] Process completed successfully!{S}")
        
    except KeyboardInterrupt:
        print(f"\n{B}[{R}!{B}] Process interrupted by user{S}")
    except Exception as e:
        print(f"\n{B}[{R}!{B}] An error occurred: {e}{S}")

if __name__ == "__main__":
    main()
