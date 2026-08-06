import requests
import json
import sys
import os
import time

# ---------- الألوان والتنسيقات ----------
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[38;5;46m"
LIGHT_GREEN = "\033[38;5;118m"
WHITE = "\033[38;5;255m"
YELLOW = "\033[38;5;226m"
CYAN = "\033[38;5;51m"
MAGENTA = "\033[38;5;201m"
RED = "\033[38;5;196m"
GRAY = "\033[38;5;244m"

# ---------- بيانات المنتجات (محدثة 2026) ----------
PRODUCTS_DETAILS = {
    "Fakka_2.5_Unite": {"name": "فكة 2.5 جنيه", "price": "1.75", "units": "45 وحدة", "duration": "يوم واحد"},
    "Fakka_4.25_Unite": {"name": "فكة 4.25 جنيه", "price": "2.97", "units": "190 وحدة", "duration": "يوم واحد"},
    "Fakka_5_Unite": {"name": "فكة 5 جنيه", "price": "3.50", "units": "225 وحدة", "duration": "يوم واحد"},
    "Fakka_6_NewUnite": {"name": "فكة 6 جنيه", "price": "سعر متغير", "units": "غير محدد", "duration": "يوم واحد"},
    "Fakka_7_Unite": {"name": "فكة 7 جنيه", "price": "4.90", "units": "300 وحدة", "duration": "3 أيام"},
    "Fakka_9_Unite": {"name": "فكة 9 جنيه", "price": "6.30", "units": "400 وحدة", "duration": "4 أيام"},
    "Fakka_10_Unite": {"name": "فكة 10 جنيه", "price": "7.00", "units": "450 وحدة", "duration": "7 أيام"},
    "Fakka_10_NewUnite": {"name": "فكة 10 جنيه (new)", "price": "غير معروف", "units": "غير معروف", "duration": "غير معروف"},
    "Fakka_10.5_Unite": {"name": "فكة 10.5 جنيه", "price": "7.35", "units": "400 وحدة + 50MB", "duration": "7 أيام"},
    "Fakka_11.5_Unite": {"name": "فكة 11.5 جنيه", "price": "غير معروف", "units": "غير معروف", "duration": "غير معروف"},
    "Fakka_12_Unite": {"name": "فكة 12 جنيه", "price": "8.40", "units": "425 وحدة", "duration": "7 أيام"},
    "Fakka_12.5_Unite": {"name": "فكة 12.5 جنيه", "price": "سعر متغير", "units": "غير محدد", "duration": "غير محددة"},
    "Fakka_13_Unite": {"name": "فكة 13 جنيه", "price": "9.10", "units": "غير محدد", "duration": "7 أيام"},
    "Fakka_13.5_Unite": {"name": "فكة 13.5 جنيه", "price": "9.45", "units": "625 وحدة", "duration": "7 أيام"},
    "Fakka_15_Unite": {"name": "فكة 15 جنيه", "price": "10.50", "units": "550 وحدة", "duration": "7 أيام"},
    "Fakka_15_NewUnite": {"name": "فكة 15 جنيه (new)", "price": "غير معروف", "units": "غير معروف", "duration": "غير معروف"},
    "Fakka_15.5_Unite": {"name": "فكة 15.5 جنيه", "price": "10.85", "units": "625 وحدة", "duration": "7 أيام"},
    "Fakka_16.5_Unite": {"name": "فكة 16.5 جنيه", "price": "11.55", "units": "غير محدد", "duration": "10 أيام"},
    "Fakka_17.5_Unite": {"name": "فكة 17.5 جنيه", "price": "12.25", "units": "650 وحدة", "duration": "10 أيام"},
    "Fakka_19.5_NewUnite": {"name": "فكة 19.5 جنيه (new)", "price": "13.65", "units": "غير محدد", "duration": "10 أيام"},
    "Fakka_20_Unite": {"name": "فكة 20 جنيه", "price": "14.0", "units": "750 وحدة", "duration": "10 أيام"},
    "Fakka_26_Unite": {"name": "فكة 26 جنيه", "price": "18.20", "units": "غير محدد", "duration": "شهر"},
    "Mared_10_Minuts": {"name": "مارد 10 دقايق", "price": "سعر متغير", "units": "10 دقائق", "duration": "يوم واحد"},
    "Mared_10_Flexs": {"name": "مارد 10 فليكس", "price": "سعر متغير", "units": "10 فليكس", "duration": "يوم واحد"},
    "Mared_10_Social": {"name": "مارد 10 سوشيال", "price": "سعر متغير", "units": "10 سوشيال", "duration": "يوم واحد"},
}

FAKKA_PRODUCTS = [
    ("فكة 2.5 جنيه", "Fakka_2.5_Unite"), ("فكة 4.25 جنيه", "Fakka_4.25_Unite"),
    ("فكة 5 جنيه", "Fakka_5_Unite"), ("فكة 6 جنيه", "Fakka_6_NewUnite"),
    ("فكة 7 جنيه", "Fakka_7_Unite"), ("فكة 9 جنيه", "Fakka_9_Unite"),
    ("فكة 10 جنيه", "Fakka_10_Unite"), ("فكة 10 جنيه (new)", "Fakka_10_NewUnite"),
    ("فكة 10.5 جنيه", "Fakka_10.5_Unite"), ("فكة 11.5 جنيه", "Fakka_11.5_Unite"),
    ("فكة 12 جنيه", "Fakka_12_Unite"), ("Fakka_12.5 جنيه", "Fakka_12.5_Unite"),
    ("فكة 13 جنيه", "Fakka_13_Unite"), ("Fakka_13.5 جنيه", "Fakka_13.5_Unite"),
    ("فكة 15 جنيه", "Fakka_15_Unite"), ("فكة 15 جنيه (new)", "Fakka_15_NewUnite"),
    ("فكة 15.5 جنيه", "Fakka_15.5_Unite"), ("فكة 16.5 جنيه", "Fakka_16.5_Unite"),
    ("فكة 17.5 جنيه", "Fakka_17.5_Unite"), ("فكة 19.5 جنيه (new)", "Fakka_19.5_NewUnite"),
    ("فكة 20 جنيه", "Fakka_20_Unite"), ("فكة 26 جنيه", "Fakka_26_Unite"),
]
MARED_PRODUCTS = [
    ("مارد 10 دقايق", "Mared_10_Minuts"),
    ("مارد 10 فليكس", "Mared_10_Flexs"),
    ("مارد 10 سوشيال", "Mared_10_Social"),
]
ALL_PRODUCTS = FAKKA_PRODUCTS + MARED_PRODUCTS

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(f"\n{GREEN}{BOLD}╔" + "═"*58 + "╗")
    print(f"║{YELLOW}{BOLD}          🚀  نظام شحن فودافون كاش المطور 2026  🚀          {GREEN}║")
    print(f"╚" + "═"*58 + f"╝{RESET}")

def print_product_box(index, product_id):
    details = PRODUCTS_DETAILS.get(product_id, {})
    name = details.get('name', 'غير معروف')
    price = details.get('price', 'غير معروف')
    units = details.get('units', 'غير معروف')
    duration = details.get('duration', 'غير معروف')
    price_str = f"{price} ج" if price not in ["سعر متغير", "غير معروف"] else price
    print(f"{GREEN}╔" + "═"*58 + "╗")
    print(f"║ {WHITE}{BOLD}[{index:02}]{RESET} {YELLOW}{BOLD}{name:<46}{GREEN} ║")
    print(f"╠" + "─"*58 + "╣")
    print(f"║ {WHITE}💰 السعر   : {CYAN}{price_str:<45}{GREEN} ║")
    print(f"║ {WHITE}📊 الوحدات : {MAGENTA}{units:<45}{GREEN} ║")
    print(f"║ {WHITE}⏰ المدة   : {LIGHT_GREEN}{duration:<45}{GREEN} ║")
    print(f"╚" + "═"*58 + "╝{RESET}")

def safe_request(method, url, step_name, **kwargs):
    try:
        response = requests.request(method, url, **kwargs)
        if response.status_code not in [200, 201]:
            print(f"\n{RED}❌ خطأ من السيرفر ({response.status_code}) في خطوة: {step_name}{RESET}")
            return None
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"\n{RED}❌ الرد المستلم ليس بتنسيق JSON في خطوة: {step_name}{RESET}")
            return None
            
    except Exception as e:
        print(f"\n{RED}❌ حدث خطأ غير متوقع: {str(e)}{RESET}")
    return None

def main():
    clear_screen()
    print_header()
    print(f"\n{WHITE}{BOLD}📦 قائمة الكروت المتاحة:{RESET}\n")
    for i, (name, pid) in enumerate(ALL_PRODUCTS, 1):
        print_product_box(i, pid)
    
    print(f"\n{GREEN}" + "═"*60 + f"{RESET}")
    while True:
        try:
            choice_str = input(f"{WHITE}{BOLD}🔢 أدخل رقم الكرت المطلوب: {RESET}")
            if not choice_str: continue
            choice = int(choice_str)
            if 1 <= choice <= len(ALL_PRODUCTS):
                product_name, product_id = ALL_PRODUCTS[choice-1]
                break
            else:
                print(f"{RED}❌ الرقم يجب أن يكون بين 1 و {len(ALL_PRODUCTS)}{RESET}")
        except ValueError:
            print(f"{RED}❌ يرجى إدخال رقم صحيح.{RESET}")

    print(f"\n{GREEN}{BOLD}✅ تم اختيار: {WHITE}{product_name}{RESET}")

    print(f"\n{CYAN}{BOLD}📱 بيانات المستلم:{RESET}")
    receiver = input(f"{WHITE}   أدخل رقم الهاتف (11 رقم): {RESET}").strip()
    if not (receiver.startswith("01") and len(receiver) == 11):
        print(f"{RED}❌ رقم غير صحيح.{RESET}")
        return

    pin = input(f"{WHITE}🔒 أدخل الرقم السري للمحفظة: {RESET}").strip()

    print(f"\n{YELLOW}⏳ جاري الاتصال الآمن بسيرفرات فودافون 2026...{RESET}")

    common_headers = {
        'User-Agent': "okhttp/4.12.0",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'clientId': "AnaVodafoneAndroid",
        'Accept-Language': "ar",
        'x-agent-operatingsystem': "14",
        'x-agent-version': "2026.7.1",
        'x-agent-build': "1200",
        'digitalId': "26S0M71T0I2RK"
    }

    # 1. Seamless Login[span_1](start_span)[span_1](end_span)
    url_seamless = "http://mobile.vodafone.com.eg/checkSeamless/realms/vf-realm/protocol/openid-connect/auth?client_id=ana-vodafone-app-seamless"
    seamless_data = safe_request('GET', url_seamless, "تسجيل الدخول التلقائي", headers=common_headers, timeout=20)
    if not seamless_data: return
    seamless_token = seamless_data.get('seamlessToken')
    sender_msisdn = seamless_data.get('msisdn')

    # 2. Access Token[span_2](start_span)[span_2](end_span)
    url_token = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    auth_headers = common_headers.copy()
    auth_headers.update({'silentLogin': "true", 'seamlessToken': seamless_token, 'firstTimeLogin': "true"})
    token_data = safe_request('POST', url_token, "الحصول على صلاحية الوصول", data={'grant_type': "password", 'client_secret': "b86e30a8-ae29-467a-a71f-65c73f2ff5e3", 'client_id': "cash-app"}, headers=auth_headers, timeout=20)
    if not token_data: return
    access_token = token_data.get('access_token')

    # 3. Product Order[span_3](start_span)[span_3](end_span)
    url_order = "https://mobile.vodafone.com.eg/services/dxl/pom/productOrder"
    payload_order = {
        "channel": {"name": "MobileApp"},
        "orderItem": [{
            "action": "insert", "id": product_id,
            "product": {
                "characteristic": [{"name": "PaymentMethod", "value": "VFCash"}, {"name": "USE_EMONEY", "value": "False"}, {"name": "MerchantCode", "value": ""}],
                "id": product_id,
                "relatedParty": [{"id": str(sender_msisdn), "name": "MSISDN", "role": "Subscriber"}, {"id": receiver, "name": "Receiver", "role": "Receiver"}]
            },
            "@type": product_id, "eCode": 0
        }],
        "relatedParty": [{"id": pin, "name": "pin", "role": "Requestor"}],
        "@type": "CashFakkaAndMared"
    }
    order_headers = common_headers.copy()
    order_headers.update({'Accept': "application/json", 'Content-Type': "application/json", 'api-host': "ProductOrderingManagement", 'useCase': "CashFakkaAndMared", 'api-version': "v2", 'msisdn': f'0{sender_msisdn}', 'Authorization': f"Bearer {access_token}"})

    result = safe_request('POST', url_order, "تنفيذ عملية الشحن", data=json.dumps(payload_order), headers=order_headers, timeout=25)
    
    if result:
        if result.get('state') == 'Completed' or result.get('complete'):
            print(f"\n{GREEN}{BOLD}🎉 مبروك! تم الشحن بنجاح.{RESET}")
        else:
            msg = result.get('message') or result.get('description') or "رصيد غير كافي أو خطأ في البيانات"
            print(f"\n{RED}❌ فشل الشحن: {msg}{RESET}")

if __name__ == "__main__":
    main()
