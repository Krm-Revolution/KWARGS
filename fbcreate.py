import os
import sys
import re
import time
import json
import pytz
import uuid
import requests
import bs4
import string
import faker
import random
from faker import Faker
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
try:
    import rich
except:
    os.system("pip install rich requests fake-useragent")
    import rich
from rich import print
from rich.tree import Tree
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Console
from rich.console import Group
from rich.align import Align
from rich.syntax import Syntax
from datetime import datetime
from time import sleep
from time import sleep as jeda
from time import strftime

folder_path = '/sdcard/Nexus'
try:
    os.makedirs(folder_path, exist_ok=True)
except:
    pass
os.system("clear")

R = "[bold red]"
G = "[bold green]"
Y = "[bold yellow]"
B = "[bold blue]"
M = "[bold magenta]"
P = "[bold violet]"
C = "[bold cyan]"
W = "[bold white]"
r = "\033[1;31m"
g = "\033[1;32m"
y = "\033[1;33m"
b = "\033[1;34m"
m = "\033[1;35m"
c = "\033[1;36m"
w = "\033[1;37m"

bulan = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June',
         '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}
tgl = datetime.now().day
bln = bulan[(str(datetime.now().month))]
thn = datetime.now().year
tanggal = (str(tgl) + ' ' + str(bln) + ' ' + str(thn))
waktu = strftime('%H:%M:%S')
hari = datetime.now().strftime("%A")

def lo(word):
    Rayhan = ["[\033[38;5;40m■\x1b[0m□□□□□□□□□]",
              "[\033[38;5;42m■■\x1b[0m□□□□□□□□]",
              "[\033[38;5;42m■■■\x1b[0m□□□□□□□]",
              "[\033[38;5;43m■■■■\x1b[0m□□□□□□]",
              "[\033[38;5;44m■■■■■\x1b[0m□□□□□]",
              "[\033[38;5;45m■■■■■■\x1b[0m□□□□]",
              "[\x1b[1;97m■■■■■■■\x1b[0m□□□]",
              "[\x1b[1;98m■■■■■■■■\x1b[0m□□]",
              "[\x1b[1;99m■■■■■■■■■\x1b[0m□]",
              "[\x1b[1;910m■■■■■■■■■■\x1b[0m]"]
    for i in range(5):
        for x in range(len(Rayhan)):
            sys.stdout.write(('\r{}{}').format(str(word), Rayhan[x]))
            time.sleep(0.1)
            sys.stdout.flush()

try:
    from fake_useragent import UserAgent
    ua = UserAgent()
except:
    os.system("pip install fake-useragent")
    from fake_useragent import UserAgent
    ua = UserAgent()

def ugenX():
    ualist = [ua.random for _ in range(50)]
    return str(random.choice(ualist))

def fake_name():
    first = Faker().first_name()
    last = Faker().last_name()
    return first, last

def fake_password():
    name = " ".join(fake_name()).replace(' ', '')
    jam = str(datetime.now().strftime("%X")).replace(':', '')
    namepassword = f'{name}.{jam}.{str(random.randrange(1000, 10000))}'
    return namepassword

def useragent_facebook():
    asus = ['ASUS_A002', 'ASUS_A002A', 'ASUS_AI2201', 'ASUS_I001D', 'ASUS_I002D', 'ASUS_I003D', 'ASUS_I004D', 'ASUS_I005D', 'ASUS_I006D', 'ASUS_I007D', 'ASUS_I01WD', 'ASUS_Z01QD']
    oppo = ["CPH1869", "CPH1929", "CPH2107", "CPH2238", "CPH2389", "CPH2401", "CPH2407", "CPH2413", "CPH2415", "CPH2417", "CPH2419", "CPH2455", "CPH2459"]
    oppo2 = ["OP4F97", "OP4BA5L1", "OP664D1", "OP5F11L1", "OP2A92", "OP8F17", "OPPOA16", "OPPOA15", "OPPOA11", "OPPOA73", "OPPOA37", "OPPOA53"]
    micromax = ['Micromax A064', 'Micromax A065', 'Micromax A066', 'Micromax A067', 'MICROMAX A068', 'Micromax A069', 'Micromax A110', 'Micromax A116', 'Micromax A120', 'Micromax A250']
    oneplus = ['NE2213', 'NE2217', 'NE2215', 'NE2210', 'CPH2423', 'CPH2411', 'ONEPLUS A3003', 'ONEPLUS A5000', 'ONEPLUS A6003', 'ONEPLUS A6010', 'GM1900', 'GM1901', 'GM1903']
    vivo = ['vivo 1809', 'vivo 1914', 'vivo 2010', 'vivo 2019', 'vivo 2023', 'VIVO 5', 'Vivo 6', 'Vivo 7 Pro', 'Vivo 8']
    vivo2 = ["vivo/iQOO 5 Pro", "vivo/iQOO 7", "vivo/iQOO Z5", "vivo/iQOO U3", "vivo/iQOO Neo 3", "vivo/iQOO 8", "vivo/iQOO 9"]
    poco = ['M2006C3MI', '211033MI', '22031116AI', '220333QPG', 'POCO C40', 'POCO F2 Pro', 'M2012K11AG', 'POCO F4', 'POCO M3', 'POCO M3 Pro']
    dpi = str(random.choice(['320dpi', '640dpi', '480dpi', '420dpi', '240dpi', '360dpi', '720dpi', '300dpi', '401dpi', '340dpi']))
    pxl = str(random.choice(['720x1280', '1440x2560', '1080x1920', '540x960', '1080x2076', '1080x2094', '1080x2220', '1200x1920', '1920x1080', '720x1440']))
    device_android = str(random.choice(["27/9", "27/10", "27/11", "27/12", "28/9", "28/10", "28/11", "29/9", "29/10", "30/10", "30/11", "31/9", "31/10"]))
    kode2 = (f'{random.randint(211111111, 399999999)}')
    versi_facebook = random.choice(["70.0.0.15.98", "80.0.0.20.101", "60.0.0.10.76", "85.0.0.25.100", "75.0.0.22.99", "72.0.0.18.94", "68.0.0.16.84", "78.0.0.14.97"])
    iphn = random.choice(["11,8", "12,1", "9,2", "13,3", "10,5", "12,8", "10,4", "13,1", "9,1", "11,2"])
    ios = random.choice(["iOS 14_4_1", "iOS 15_0", "iOS 12_1_3", "iOS 15_0_1", "iOS 14_7_1", "iOS 14_6", "iOS 13_5", "iOS 14_0_1"])
    scale = random.choice(["2.00", "3.00", "2.61", "2.00", "3.00"])
    gamut = random.choice(["display", "P3", "display", "wide", "P3"])
    return random.choice([
        f'Barcelona {versi_facebook} Android ({device_android}; {dpi}; {pxl}; ASUS MOBILITY LIMITED/asus; {str(random.choice(asus))}; {str(random.choice(asus))}; qcom; in_ID; {kode2})',
        f'Barcelona {versi_facebook} Android ({device_android}; {dpi}; {pxl}; OPPO MOBILITY LIMITED/oppo; {str(random.choice(oppo2))}; {str(random.choice(oppo))}; qcom; in_ID; {kode2})',
        f'Barcelona {versi_facebook} Android ({device_android}; {dpi}; {pxl}; MICROMAX MOBILITY LIMITED/micromax; {str(random.choice(micromax))}; {str(random.choice(micromax))}; qcom; in_ID; {kode2})',
        f'Barcelona {versi_facebook} Android ({device_android}; {dpi}; {pxl}; ONEPLUS MOBILITY LIMITED/oneplus; {str(random.choice(oneplus))}; {str(random.choice(oneplus))}; qcom; in_ID; {kode2})',
        f'Barcelona {versi_facebook} Android ({device_android}; {dpi}; {pxl}; VIVO MOBILITY LIMITED/vivo; {str(random.choice(vivo2))}; {str(random.choice(vivo))}; qcom; in_ID; {kode2})',
        f'Barcelona {versi_facebook} Android ({device_android}; {dpi}; {pxl}; POCO MOBILITY LIMITED/poco; {str(random.choice(poco))}; {str(random.choice(poco))}; qcom; in_ID; {kode2})',
        f"Barcelona {versi_facebook} (iPhone{iphn}; {ios}; in_ID; in_ID; scale={scale}; gamut={gamut}; {pxl}; {kode2})"
    ])

def extractor(data):
    try:
        soup = BeautifulSoup(data, "html.parser")
        data_dict = {}
        for inputs in soup.find_all("input"):
            name = inputs.get("name")
            value = inputs.get("value")
            if name:
                data_dict[name] = value
        return data_dict
    except Exception as e:
        return {"error": str(e)}

def dn():
    time.sleep(random.randint(3, 7))

def dnn():
    time.sleep(random.randint(10, 20))

def GetPhone():
    na = random.choice(['77', '78', '59'])
    ni = str(random.randrange(1000, 10000))
    nu = str(random.randrange(10000, 100000))
    nope = '+639%s%s%s' % (na, ni, nu)
    return nope

def GetEmails():
    nam1 = random.choice(['eka', 'dwi', 'tri', 'budi', 'indah', 'dewi'])
    nam2 = random.choice(['nurhayati', 'handoko', 'setiyani', 'susanto', 'permata'])
    nam3 = random.choice(['triatmaja', 'siagian', 'manopo', 'jayaningrat', 'widodo'])
    name = f'{nam1}{nam2}{nam3}'
    domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'gonetor.com'])
    nope = f'{name}@{domain}'
    return nope

def get_temp_plus():
    name = " ".join(fake_name()).replace(' ', '')
    jam = str(datetime.now().strftime("%X")).replace(':', '')
    domain = random.choice(['fexbox.org', 'fexpost.com', 'fextemp.com', 'chitthi.in'])
    email = f'{name}.{jam}.{str(random.randrange(1000, 10000))}@{domain}'
    return email

def get_facebook_profile_info(username):
    response = requests.get(f'https://www.facebook.com/{username}')
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        profile_name = soup.find('title').text
        if profile_name:
            return profile_name
        else:
            return "NAME NOT FOUND"
    else:
        return "PROFILE IS INACCESSIBLE"

def GetInfoProfile():
    try:
        with open('/sdcard/AUTO-k9/SUCCESS-OK-ID.txt', 'r') as file:
            usernames = file.readlines()
        for username in usernames:
            username = username.strip()
            if username:
                name = get_facebook_profile_info(username.split('|')[0])
                print(f"[bold green1] USERNAME : [bold green1]{username.split('|')[0]}\n[bold green1] NAME : [green]{name}")
    except FileNotFoundError:
        print("[bold red] SUCCESS-OK-ID.txt not found.")

def space():
    print("\n")

def randc():
    randcolor = random.choice([R, G, Y, B, M, P, C, W])
    return randcolor

def clear():
    os.system("clear")

logo = ("""
_____  _____  
     /\   / ____|/ ____| 
    /  \ | |    | (___   
   / /\ \| |     \___ \  
  / ____ \ |____ ____) | 
 /_/    \_\_____|_____/
 
 Our Telegram : https://t.me/Team_ACS_officials
""")
hx = (f""" </> Python Coded BY - ACS Orkon """)

def banner():
    os.system("clear")
    print(Panel(logo, subtitle="[bold red]● [bright_yellow]● [green1]●", subtitle_align='left', title="[bold red]● [bright_yellow]● [green1]●", title_align='right', width=102, padding=0, style="bold magenta2"))
    print(Panel(hx, width=100, padding=0, style="bold magenta2"))

def LMNx9create():
    banner()
    a = (" [green_yellow][[bold cyan1]1[green_yellow]][bold green1] AUTOMATIC FB TYPE CREATION\n [green_yellow][[bold cyan1]2[green_yellow]][bold green1] ADD PROFILE INFORMATION\n [green_yellow][[bold cyan1]0[green_yellow]][bold red] EXIT")
    print(Panel(a, subtitle="[bold magenta2]┌─", subtitle_align='left', style="bold magenta2"))
    anon = Console().input("   [bold magenta2]└──> ")
    if anon in ["1", "01"]:
        main()
    elif anon in ["2", "02"]:
        banner()
        GetInfoProfile()
    elif anon in ["0", "00"]:
        exit()
    else:
        print()
        print(Panel('[bold red]OPTION NOT FOUND IN MENU', subtitle="[bold red]● [bright_yellow]● [green1]●", subtitle_align='left', title="[bold red]● [bright_yellow]● [green1]●", title_align='right', width=102, padding=0, style="bold magenta2"))
        time.sleep(1)
        LMNx9create()

Ok, Cp = 0, 0

def progres(current, num_accounts, delay):
    for sleep_sec in range(int(delay), 0, -1):
        print(f'[bold magenta1]anon [bold white][[bold cyan]{current}[bold white]/[bold red]{num_accounts}[bold white]] SUCCESS-:[bold green1]{Ok}\r', end='\r')
        time.sleep(1)
        if current == num_accounts:
            break

def results():
    print(Panel(f"""[bold white]FINAL RESULTS\nSUCCESS : [bold green]{Ok}[/]\nCHECKPOINT : [bold red]{Cp}[/]\nRESULTS ARE SAVED TO THE RESULTS FOLDER""", subtitle="[bold red]● [bright_yellow]● [green1]●", subtitle_align='left', title="[bold red]● [bright_yellow]● [green1]●", title_align='right', width=102, padding=0, style="bold violet"))

def main():
    uid = None
    global Ok, Cp, passw, num_accounts, delay
    num_accounts = int(input("\033[1;37mHOW MANY ACC : "))
    delay = int(input("\033[1;37mDELAY TIME BETWEEN REQUESTS : "))
    banner()
    a = (" [green_yellow][[bold cyan1]1[green_yellow]][bold green1] DEFAULT PASSWORD\n [green_yellow][[bold cyan1]2[green_yellow]][bold green1] CUSTOM PASSWORD")
    print(Panel(a, subtitle="[bold magenta2]┌─", subtitle_align='left', style="bold magenta2"))
    LMNx9 = Console().input("   [bold magenta2]└──> ")
    if LMNx9 in ["1", "01"]:
        passw = fake_password()
    elif LMNx9 in ["2", "02"]:
        passw = input('\033[1;37mENTER CUSTOM PASSWORD : ')
    else:
        passw = fake_password()
    
    for make in range(int(num_accounts)):
        progres(make + 1, num_accounts, delay)
        ses = requests.Session()
        try:
            response = ses.get(
                url='https://m.facebook.com/reg',
                params={"_rdc": "1", "_rdr": "", "wtsid": "rdr_0t3qOXoIHbMS6isLw", "refsrc": "deprecated"},
                headers={'User-Agent': ugenX()}
            )
            formula = extractor(response.text)
            if "error" in formula:
                print(Panel(f"[bold red] ERROR GETTING FORM DATA", style="bold magenta2"))
                continue
        except Exception as e:
            print(Panel(f"[bold red] ERROR: {str(e)}", style="bold magenta2"))
            continue
            
        email2 = get_temp_plus()
        phone2 = GetPhone()
        email3 = GetEmails()
        firstname, lastname = fake_name()
        
        print(Panel(f"[bold white] ACCESSING FACEBOOK", style="bold magenta2"))
        dn()
        print(Panel(f"[bold white] REGISTERING ACCOUNT", style="bold magenta2"))
        dn()
        print(Panel(f"[bold white] FILLING UP CREDENTIALS", style="bold magenta2"))
        dn()
        print(Panel(f"[bold white] GETTING MAIL & GETTING PHONE", style="bold magenta2"))
        dn()
        print(Panel(f"[bold white] DUMMYPHONE : [bold green1]{phone2}", style="bold magenta2"))
        dn()
        print(Panel(f"[bold white] DUMMYEMAIL : [bold green1]{email3}", style="bold magenta2"))
        dn()
        print(Panel(f"[bold white] EMAIL : [bold green1]{email2}", style="bold magenta2"))
        dn()
        print(Panel(f"[bold white] FIRSTNAME : {firstname}", style="bold magenta2"))
        dn()
        print(Panel(f"[bold white] LASTNAME : {lastname}", style="bold magenta2"))
        dn()
        print(Panel(f"[bold white] PASSWORD : {passw}", style="bold magenta2"))
        dn()
        
        payload = {
            'ccp': "2",
            'reg_instance': str(formula.get("reg_instance", "")),
            'submission_request': "true",
            'helper': "",
            'reg_impression_id': str(formula.get("reg_impression_id", "")),
            'ns': "1",
            'zero_header_af_client': "",
            'app_id': "103",
            'logger_id': str(formula.get("logger_id", "")),
            'field_names[0]': "firstname",
            'firstname': firstname,
            'lastname': lastname,
            'field_names[1]': "birthday_wrapper",
            'birthday_day': str(random.randint(1, 28)),
            'birthday_month': str(random.randint(1, 12)),
            'birthday_year': str(random.randint(1992, 2009)),
            'age_step_input': "",
            'did_use_age': "false",
            'field_names[2]': "reg_email__",
            'reg_email__': email2,
            'reg_number__': phone2,
            'field_names[3]': "sex",
            'sex': "2",
            'preferred_pronoun': "",
            'custom_gender': "",
            'field_names[4]': "reg_passwd__",
            'name_suggest_elig': "false",
            'was_shown_name_suggestions': "false",
            'did_use_suggested_name': "false",
            'use_custom_gender': "false",
            'guid': "",
            'pre_form_step': "",
            'encpass': '#PWD_BROWSER:0:{}:{}'.format(str(time.time()).split('.')[0], f"{passw}"),
            'submit': "Sign Up",
            'fb_dtsg': str(formula.get("fb_dtsg", ":0:0")),
            'jazoest': str(formula.get("jazoest", "")),
            'lsd': str(formula.get("lsd", "")),
            '__dyn': "1ZaaAG1mxu1oz--0jG3qaw4kwbS1Lw9C0le0ue0QU",
            '__csr': "",
            '__req': "p",
            '__fmt': "1",
            '__a': "-H1lSX6ucxsegViw9lLO6uRx31-SpnBlUEDawD_8U7AY4kQ",
            '__user': "0"
        }
        
        headers = {
            "Host": "m.facebook.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": ugenX(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "dnt": "1",
            'Accept-Encoding': "gzip, deflate, br",
            'sec-ch-ua-platform': "\"Android\"",
            'sec-ch-ua': "\"Android WebView\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            'sec-ch-ua-mobile': "?1",
            'origin': "https://m.facebook.com",
            'x-requested-with': "mark.via.gp",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://m.facebook.com/reg/",
            'accept-language': "en-GB,en-US;q=0.9,en;q=0.8",
            'priority': "u=1, i"
        }
        
        url = 'https://m.facebook.com/reg/submit/'
        
        try:
            response = ses.post(url, data=payload, headers=headers)
            if "checkpoint" in str(response.url):
                print(Panel(f"[bold red] ACCOUNT DISABLED / CHECKPOINT", style="bold magenta2"))
                Cp += 1
            else:
                cookie = ";".join([f"{key}={value}" for key, value in ses.cookies.get_dict().items()])
                uid_match = re.search(r'c_user=(\d+)', cookie)
                if uid_match:
                    uid = uid_match.group(1)
                print(Panel(f"[bold green1] UID      : {uid}\n[bold green1] PASSWORD : {passw}\n[bold green1] COOKIE   : [bold green1]{cookie[:100]}...\n[bold green1] USERAGENT : [bold green1]{useragent_facebook()}", subtitle="[bold yellow] CREATE ", style="bold magenta2"))
                dn()
                Ok += 1
                with open('/sdcard/Nexus/SUCCESS-OK-ID.txt', 'a') as f:
                    f.write(f"{uid}|{passw}|{email2}|{phone2}|{firstname} {lastname}|{cookie}\n")
        except Exception as e:
            print(Panel(f"[bold red] ERROR: {str(e)}", style="bold magenta2"))
    
    results()

try:
    a = requests.get("http://ip-api.com/json/", timeout=5).json()
    xy = requests.get('https://api.ipify.org/', timeout=5).text
    co = a.get("country", "Unknown")
except:
    xy = "Unknown"
    co = "Unknown"

os.system('clear')
print('\r\r\r[bold blue]              YOUR IP:[bold green1]' + str(xy))
print('\r\r\r[bold yellow]              YOUR COUNTRY:[bold green1]' + str(co))
time.sleep(3)

if __name__ == "__main__":
    LMNx9create()
