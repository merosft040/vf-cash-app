import streamlit as st
import requests
import json
from supabase import create_client, Client

# 1. ضبط إعدادات الصفحة
st.set_page_config(page_title="فودافون كاش 2026", page_icon="🚀", layout="centered")

# 2. الاتصال بقاعدة بيانات Supabase
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("⚠️ يرجى ضبط مفاتيح Supabase في Secrets أولاً!")
    st.stop()

# 3. التحقق من الكود الموجود في الرابط مباشرة
query_params = st.query_params
saved_key = query_params.get("key", "")

is_activated = False

if saved_key:
    try:
        response = supabase.table("activations").select("*").eq("key_code", saved_key.strip()).execute()
        if response.data:
            is_activated = True
    except:
        pass

# 4. شاشة التفعيل (لو مفيش كود صالح في الرابط)
if not is_activated:
    st.title("🔑 تفعيل التطبيق (نسخة سحابية)")
    user_key = st.text_input("أدخل كود الاشتراك للاختبار:", type="password")
    
    if st.button("تفعيل", use_container_width=True):
        if user_key:
            clean_key = user_key.strip()
            try:
                response = supabase.table("activations").select("*").eq("key_code", clean_key).execute()
                data = response.data
                
                if data:
                    st.query_params["key"] = clean_key
                    st.success("تم التفعيل بنجاح! جاري فتح التطبيق...")
                    st.rerun()
                else:
                    st.error("❌ كود التفعيل غير صحيح أو غير موجود بالقاعدة!")
            except Exception as db_err:
                st.error(f"❌ خطأ في قاعدة البيانات: {db_err}")
        else:
            st.warning("يرجى كتابة الكود!")
    st.stop()

# =========================================================
# 5. الواجهة الرئيسية للتطبيق
# =========================================================

with st.sidebar:
    st.write("⚙️ الإعدادات")
    st.success("🟢 التطبيق مفعل ودائم")
    if st.button("تسجيل الخروج / مسح التفعيل"):
        st.query_params.clear()
        st.rerun()

st.title("🚀 فودافون كاش 2026")
st.subheader("شحن كروت الفكة والمارد")

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

ALL_PRODUCTS = [
    ("فكة 2.5 جنيه", "Fakka_2.5_Unite"), ("فكة 4.25 جنيه", "Fakka_4.25_Unite"),
    ("فكة 5 جنيه", "Fakka_5_Unite"), ("فكة 6 جنيه", "Fakka_6_NewUnite"),
    ("فكة 7 جنيه", "Fakka_7_Unite"), ("فكة 9 جنيه", "Fakka_9_Unite"),
    ("فكة 10 جنيه", "Fakka_10_Unite"), ("فكة 10 جنيه (new)", "Fakka_10_NewUnite"),
    ("فكة 10.5 جنيه", "Fakka_10.5_Unite"), ("فكة 11.5 جنيه", "Fakka_11.5_Unite"),
    ("فكة 12 جنيه", "Fakka_12_Unite"), ("فكة 12.5 جنيه", "Fakka_12.5_Unite"),
    ("فكة 13 جنيه", "Fakka_13_Unite"), ("فكة 13.5 جنيه", "Fakka_13.5_Unite"),
    ("فكة 15 جنيه", "Fakka_15_Unite"), ("فكة 15 جنيه (new)", "Fakka_15_NewUnite"),
    ("فكة 15.5 جنيه", "Fakka_15.5_Unite"), ("فكة 16.5 جنيه", "Fakka_16.5_Unite"),
    ("فكة 17.5 جنيه", "Fakka_17.5_Unite"), ("فكة 19.5 جنيه (new)", "Fakka_19.5_NewUnite"),
    ("فكة 20 جنيه", "Fakka_20_Unite"), ("فكة 26 جنيه", "Fakka_26_Unite"),
    ("مارد 10 دقايق", "Mared_10_Minuts"), ("مارد 10 فليكس", "Mared_10_Flexs"),
    ("مارد 10 سوشيال", "Mared_10_Social")
]

selected_product_name, product_id = st.selectbox(
    "اختر الكرت المطلوب لشحنه:",
    options=ALL_PRODUCTS,
    format_func=lambda x: f"{x[0]} ({PRODUCTS_DETAILS.get(x[1], {}).get('price', '')} ج)"
)

st.write("---")

receiver = st.text_input("📱 رقم مستلم الشحن (11 رقم)", max_chars=11)
pin = st.text_input("🔒 الرقم السري للمحفظة", type="password", max_chars=6)

def safe_request(session, method, url, step_name, **kwargs):
    try:
        response = session.request(method, url, **kwargs)
        if response.status_code not in [200, 201]:
            st.error(f"❌ خطأ من السيرفر ({response.status_code}) في خطوة: {step_name}")
            return None
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error(f"❌ الرد المستلم ليس بتنسيق JSON في خطوة: {step_name} (النص: {response.text[:150]})")
            return None
    except Exception as e:
        st.error(f"❌ حدث خطأ غير متوقع في {step_name}: {str(e)}")
        return None

if st.button("تأكيد الشحن 🚀", use_container_width=True):
    if not (receiver.startswith("01") and len(receiver) == 11):
        st.error("❌ رقم الهاتف غير صحيح!")
    elif not pin:
        st.error("❌ يرجى إدخال الرقم السري!")
    else:
        with st.spinner("⏳ جاري الاتصال الآمن بسيرفرات فودافون 2026..."):
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

            # استخدام Session لتثبيت الاتصال وتجاوز الحظر السحابي
            session = requests.Session()

            # 1. Seamless Login
            url_seamless = "https://mobile.vodafone.com.eg/checkSeamless/realms/vf-realm/protocol/openid-connect/auth?client_id=ana-vodafone-app-seamless"
            seamless_data = safe_request(session, 'GET', url_seamless, "تسجيل الدخول التلقائي", headers=common_headers, timeout=20, allow_redirects=True)
            
            if seamless_data:
                seamless_token = seamless_data.get('seamlessToken')
                sender_msisdn = seamless_data.get('msisdn')

                if seamless_token and sender_msisdn:
                    # 2. Access Token
                    url_token = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
                    auth_headers = common_headers.copy()
                    auth_headers.update({'silentLogin': "true", 'seamlessToken': seamless_token, 'firstTimeLogin': "true"})
                    token_data = safe_request(session, 'POST', url_token, "الحصول على صلاحية الوصول", data={'grant_type': "password", 'client_secret': "b86e30a8-ae29-467a-a71f-65c73f2ff5e3", 'client_id': "cash-app"}, headers=auth_headers, timeout=20)
                    
                    if token_data:
                        access_token = token_data.get('access_token')
                        
                        if access_token:
                            # 3. Product Order
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

                            result = safe_request(session, 'POST', url_order, "تنفيذ عملية الشحن", data=json.dumps(payload_order), headers=order_headers, timeout=25)
                            
                            if result:
                                if result.get('state') == 'Completed' or result.get('complete'):
                                    st.success("🎉 مبروك! تم الشحن بنجاح.")
                                else:
                                    msg = result.get('message') or result.get('description') or "رصيد غير كافي أو خطأ في البيانات"
                                    st.error(f"❌ فشل الشحن: {msg}")
