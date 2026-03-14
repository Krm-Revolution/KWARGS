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
version = "Version 1.0"

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
        rq1 = requests.get(url, headers=head, allow_redirects=True)
        rp1 = rq1.text.replace("\\", "")
        final_url = rq1.url
        if final_url == "https://accountscenter.facebook.com/profiles":
            pass
        else:
            return {"status": "fail", "message": "Cookie Invalid or Expired"}
        try:
            IG_uname = re.search(r'"identity_type"\s*:\s*"IG_USER".*?"username"\s*:\s*"([^"]+)"', str(rp1)).group(1)
        except AttributeError:
            return {"status": "fail", "message": "Instagram Account Not Linked"}
        try:
            uid = re.search(r'"actorID"\s*:\s*"(\d+)"', str(rp1)).group(1)
        except AttributeError:
            return {"status": "fail", "message": "Failed to get user_id"}
        return {"status": "success", "uid": uid, "ig_uname": IG_uname}
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def step1(cookie, uid):
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
        rq1 = requests.get(url, headers=head, timeout=40)
        rp1 = rq1.text.replace("\\", "")
        try:
            fb_dtsg = re.search(r'\["DTSGInitialData".*?\{[^}]*"token"\s*:\s*"([^"]+)"', str(rp1)).group(1)
            lsd = re.search(r'\["LSD".*?"token"\s*:\s*"([^"]+)"', str(rp1)).group(1)
            fbid_v2 = re.search(r'"__typename"\s*:\s*"XFBFXIGAccountInfo".*?"id"\s*:\s*"(\d+)"', str(rp1)).group(1)
        except AttributeError:
            return {"status": "fail", "message": "Cookie Invalid or Expired"}
        return {"status": "success", "DTSG": fb_dtsg, "LSD": lsd, "fbid_v2": fbid_v2}
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def step2(cookie, uid, DTSG, LSD):
    try:
        head = {
            "Host": "accountscenter.facebook.com",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://accountscenter.facebook.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-User": "?1"
        }
        variable = {"input": {"client_mutation_id": "1", "actor_id": uid, "enable_share_all_logins": False, "fdid": "device_id_fetch_datr"}}
        data = {
            "locale": "en_US",
            "__user": uid,
            "fb_dtsg": DTSG,
            "lsd": LSD,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useFXSSOChangeSettingMutation",
            "server_timestamps": "true",
            "doc_id": "9427448270675232",
            "av": uid,
            "variables": json.dumps(variable)
        }
        url = "https://accountscenter.facebook.com/api/graphql"
        rp1 = requests.post(url, data=data, headers=head).json()
        if "FXCALSettingsMutationReturnDataSuccessWithNodeConfig" in str(rp1):
            return {"status": "success"}
        else:
            return {"status": "fail", "message": "Please re-link Your Instagram Account"}
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def step3(cookie, uid, DTSG, LSD, fbid_v2):
    try:
        head = {
            "Host": "accountscenter.facebook.com",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://accountscenter.facebook.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-User": "?1"
        }
        variable = {
            "input": {
                "client_mutation_id": "1",
                "actor_id": uid,
                "enable_sso": True,
                "initiator_account": {"id": uid, "type": "FACEBOOK"},
                "target_account": {"id": fbid_v2, "type": "INSTAGRAM"},
                "fdid": "device_id_fetch_datr"
            }
        }
        data = {
            "locale": "en_US",
            "__user": uid,
            "fb_dtsg": DTSG,
            "lsd": LSD,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useFXSSOChangeDirectionalSSOMutation",
            "server_timestamps": "true",
            "doc_id": "9253258021410000",
            "av": uid,
            "variables": json.dumps(variable)
        }
        url = "https://accountscenter.facebook.com/api/graphql"
        rq1 = requests.post(url, data=data, headers=head)
        rp1 = json.loads(rq1.text)
        if "FXCALSettingsMutationErrorRequiresReauth" in str(rp1):
            return {"status": "fail", "message": "Please re-link Your Instagram Account"}
        else:
            if "connect" in str(rp1):
                sso_list = rp1["data"]["fxcal_settings_update_sso_status"]["updated_node"]["advanced_sso_settings"]["sso_status"]
                if "Can log in to" in str(sso_list[0]):
                    return {"status": "success"}
                else:
                    return {"status": "fail", "message": "Failed to synchronize Facebook to Insta"}
            else:
                return {"status": "fail", "message": "An unknown error occurred"}
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def step4(cookie, uid, DTSG, LSD, fbid_v2):
    try:
        head = {
            "Host": "accountscenter.facebook.com",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://accountscenter.facebook.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Accept-Language": "en-US,en",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-User": "?1"
        }
        variable = {
            "input": {
                "client_mutation_id": "1",
                "actor_id": uid,
                "enable_sso": True,
                "initiator_account": {"id": fbid_v2, "type": "INSTAGRAM"},
                "target_account": {"id": uid, "type": "FACEBOOK"},
                "fdid": "device_id_fetch_datr"
            }
        }
        data = {
            "locale": "en_US",
            "__user": uid,
            "fb_dtsg": DTSG,
            "lsd": LSD,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useFXSSOChangeDirectionalSSOMutation",
            "server_timestamps": "true",
            "doc_id": "9253258021410000",
            "av": uid,
            "variables": json.dumps(variable)
        }
        url = "https://accountscenter.facebook.com/api/graphql"
        rq1 = requests.post(url, data=data, headers=head)
        rp1 = json.loads(rq1.text)
        if "FXCALSettingsMutationErrorRequiresReauth" in str(rp1):
            return {"status": "fail", "message": "Please re-link Your Facebook Account"}
        else:
            if "connect" in str(rp1):
                sso_list = rp1["data"]["fxcal_settings_update_sso_status"]["updated_node"]["advanced_sso_settings"]["sso_status"]
                if "Can log in to" in str(sso_list[1]):
                    return {"status": "success"}
                else:
                    return {"status": "fail", "message": "Failed to synchronize Instagram to Facebook"}
            else:
                return {"status": "fail", "message": "An unknown error occurred"}
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def step5(cookie, uid, DTSG, LSD, fbid_v2, name):
    try:
        head = {
            "Host": "accountscenter.facebook.com",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://accountscenter.facebook.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Accept-Language": "en-US",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-User": "?1"
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
        rq1 = requests.post(url, data=data, headers=head)
        rp1 = json.loads(rq1.text)
        if "fxim_update_identity_name" and "fx_identity_management" in str(rp1):
            return {"status": "success"}
        elif "Please try again later." in str(rp1):
            return {"status": "fail", "message": "Sorry We can't change your name, please try again later"}
        elif "FXCALSettingsMutationErrorRequiresReauth" in str(rp1):
            return {"status": "fail", "message": "Please re-link Your Instagram Account"}
        else:
            return {"status": "fail", "message": "An unknown error occurred"}
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def step6(cookie, uid, DTSG, LSD, fbid_v2, name):
    try:
        head = {
            "Host": "accountscenter.facebook.com",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://accountscenter.facebook.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Accept-Language": "en-US",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-User": "?1"
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
        rq1 = requests.post(url, data=data, headers=head)
        rp1 = json.loads(rq1.text)
        if name in str(rp1):
            return {"status": "success"}
        elif "FXCALSettingsMutationErrorRequiresReauth" in str(rp1):
            return {"status": "fail", "message": "Please re-link Your Instagram Account"}
        elif "Please try again later." in str(rp1):
            return {"status": "fail", "message": "Sorry We can't change your name, please try again later"}
        else:
            return {"status": "fail", "message": "An unknown error occurred"}
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def main():
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
    if "success" in check["status"]:
        uid = check["uid"]
        ig_username = check["ig_uname"]
    elif "fail" in check["status"]:
        if "Cookie Invalid or Expired" in check['message']:
            print(f"{B}[{R}x{B}] Your cookie is invalid or expired{S}")
            exit()
        elif "Instagram Account Not Linked" in check["message"]:
            print(f"{B}[{R}x{B}] Please link an Instagram account first and try again{S}")
            exit()
        elif "Failed to get user_id" in check["message"]:
            print(f"{B}[{R}x{B}] Your cookie is invalid or expired{S}")
            exit()
        elif "Connection Error" in check["message"]:
            print(f"{B}[{R}x{B}] No internet connection{S}")
            exit()
        else:
            print(f"{B}[{R}x{B}] An unknown error occurred, please try again{S}")
            exit()
    print(f"{B}[{V}✓{B}] Your cookie is active...{S}")
    print(f"{B}[+] Getting your login tokens...{S}")
    s1 = step1(cookie=cookie, uid=uid)
    if "success" in s1["status"]:
        DTSG = s1["DTSG"]
        LSD = s1["LSD"]
        fbid_v2 = s1["fbid_v2"]
    elif "fail" in s1["status"]:
        if "Cookie Invalid or Expired" in s1["message"]:
            print(f"{B}[{R}x{B}] Your cookie is invalid or expired{S}")
            exit()
        elif "Connection Error" in s1["message"]:
            print(f"{B}[{R}x{B}] No internet connection{S}")
            exit()
        else:
            print(f"{B}[{R}x{B}] An unknown error occurred, please try again{S}")
            exit()
    s2 = step2(cookie=cookie, uid=uid, DTSG=DTSG, LSD=LSD)
    if "success" in s2["status"]:
        pass
    elif "fail" in s2["status"]:
        if "An unknown error occurred" in s2["message"]:
            print(f"{B}[{R}x{B}] An unknown error occurred{S}")
            exit()
        elif "Connection Error" in s2["message"]:
            print(f"{B}[{R}x{B}] No internet connection{S}")
            exit()
        else:
            print(f"{B}[{R}+{B}] An unknown error occurred, please try again{S}")
            exit()
    print(f"{B}[+] Synchronizing Facebook to Instagram...{S}")
    s3 = step3(cookie=cookie, uid=uid, DTSG=DTSG, LSD=LSD, fbid_v2=fbid_v2)
    if "success" in s3['status']:
        pass
    elif "fail" in s3["status"]:
        if "Please re-link Your Instagram Account" in s3["message"]:
            print(f"{B}[{R}x{B}] Please re-link your Instagram account{S}")
            print(f"{B}[{R}!{B}] Open this link in your browser:{S}")
            print(f"{C}https://accountscenter.facebook.com/connected_experiences/single_sign_on_dialog/{S}")
            exit()
        elif "Failed to synchronize Facebook to Insta" in s3["message"]:
            print(f"{B}[{R}x{B}] Synchronization failed{S}")
            exit()
        elif "Connection Error" in s3["message"]:
            print(f"{B}[{R}x{B}] No internet connection{S}")
            exit()
        else:
            print(f"{B}[{R}+{B}] An unknown error occurred, please try again{S}")
            exit()
    print(f"{B}[+] Synchronizing Instagram to Facebook...{S}")
    s4 = step4(cookie=cookie, uid=uid, DTSG=DTSG, LSD=LSD, fbid_v2=fbid_v2)
    if "success" in s4['status']:
        pass
    elif "fail" in s4["status"]:
        if "Please re-link Your Facebook Account" in s4["message"]:
            print(f"{B}[{R}x{B}] Please re-link your Facebook account{S}")
            print(f"{B}[{R}!{B}] Open this link in your browser:{S}")
            print(f"{C}https://accountscenter.facebook.com/connected_experiences/single_sign_on_dialog/{S}")
            exit()
        elif "Failed to synchronize Instagram to Facebook" in s4["message"]:
            print(f"{B}[{R}x{B}] Synchronization failed{S}")
            exit()
        elif "Connection Error" in s4["message"]:
            print(f"{B}[{R}x{B}] No internet connection{S}")
            exit()
        else:
            print(f"{B}[{R}+{B}] An unknown error occurred, please try again{S}")
            exit()
    print(f"{B}[{V}✓{B}] SSO Synchronization completed successfully!{S}")
    print()
    print(f"{B}[{V}!{B}] Instagram Username: {C}{ig_username}{S}")
    print(f"{B}[{V}!{B}] Facebook ID: {C}{uid}{S}")
    print()
    change_name = input(f"{B}[{R}?{B}] Do you want to change your name? (y/n): {V}")
    if change_name.lower() == 'y':
        new_name = input(f"{B}[{R}?{B}] Enter new name: {V}")
        print(f"{B}[+] Changing Instagram name to {C}{new_name}{B}...{S}")
        s5 = step5(cookie=cookie, uid=uid, DTSG=DTSG, LSD=LSD, fbid_v2=fbid_v2, name=new_name)
        if "success" in s5["status"]:
            print(f"{B}[{V}✓{B}] Name changed successfully on Instagram!{S}")
            print(f"{B}[+] Synchronizing name across accounts...{S}")
            s6 = step6(cookie=cookie, uid=uid, DTSG=DTSG, LSD=LSD, fbid_v2=fbid_v2, name=new_name)
            if "success" in s6["status"]:
                print(f"{B}[{V}✓{B}] Name synchronized successfully on both platforms!{S}")
            elif "fail" in s6["status"]:
                if "Please re-link Your Instagram Account" in s6["message"]:
                    print(f"{B}[{R}x{B}] Please re-link your Instagram account{S}")
                    print(f"{B}[{R}!{B}] Open this link in your browser:{S}")
                    print(f"{C}https://accountscenter.facebook.com/connected_experiences/single_sign_on_dialog/{S}")
                elif "Sorry We can't change your name, please try again later" in s6["message"]:
                    print(f"{B}[{R}x{B}] Cannot change name, try again later{S}")
                elif "Connection Error" in s6["message"]:
                    print(f"{B}[{R}x{B}] No internet connection{S}")
                else:
                    print(f"{B}[{R}x{B}] {s6['message']}{S}")
        elif "fail" in s5["status"]:
            if "Please re-link Your Instagram Account" in s5["message"]:
                print(f"{B}[{R}x{B}] Please re-link your Instagram account{S}")
                print(f"{B}[{R}!{B}] Open this link in your browser:{S}")
                print(f"{C}https://accountscenter.facebook.com/connected_experiences/single_sign_on_dialog/{S}")
            elif "Sorry We can't change your name, please try again later" in s5["message"]:
                print(f"{B}[{R}x{B}] Cannot change name, try again later{S}")
            elif "Connection Error" in s5["message"]:
                print(f"{B}[{R}x{B}] No internet connection{S}")
            else:
                print(f"{B}[{R}x{B}] {s5['message']}{S}")
    print()
    print(f"{B}[{V}✓{B}] Process completed!{S}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{B}[{R}!{B}] Process interrupted by user{S}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{B}[{R}!{B}] An error occurred: {e}{S}")
        sys.exit(1)
      ##HII THERE WHY U HERE DAWG?
