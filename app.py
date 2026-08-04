import streamlit as st
import requests
import json

# 1. ضبط إعدادات الصفحة
st.set_page_config(page_title="فودافون كاش 2026", page_icon="🚀", layout="centered")

# 2. قائمة 20 كود تفعيل نشط
VALID_KEYS = {
    "AHMED-01": "نشط", "AHMED-02": "نشط", "AHMED-03": "نشط", "AHMED-04": "نشط",
    "AHMED-05": "نشط", "AHMED-06": "نشط", "AHMED-07": "نشط", "AHMED-08": "نشط",
    "AHMED-09": "نشط", "AHMED-10": "نشط", "AHMED-11": "نشط", "AHMED-12": "نشط",
    "AHMED-13": "نشط", "AHMED-14": "نشط", "AHMED-15": "نشط", "AHMED-16": "نشط",
    "AHMED-17": "نشط", "AHMED-18": "نشط", "AHMED-19": "نشط", "AHMED-20": "نشط"
}

# فحص التفعيل المسبق من الـ Session أو رابط المتصفح
query_params = st.query_params
saved_key = query_params.get("key", None)

if "is_activated" not in st.session_state:
    if saved_key in VALID_KEYS and VALID_KEYS[saved_key] == "نشط":
        st.session_state.is_activated = True
    else:
        st.session_state.is_activated = False

# 3. شاشة التفعيل
if not st.session_state.is_activated:
    st.title("🔑 تفعيل التطبيق (نسخة تجريبية)")
    user_key = st.text_input("أدخل كود الاشتراك للاختبار:", type="password")
    
    if st.button("تفعيل", use_container_width=True):
        if user_key in VALID_KEYS and VALID_KEYS[user_key] == "نشط":
            st.session_state.is_activated = True
            st.query_params["key"] = user_key  # حفظ التفعيل في المتصفح/الرابط
            st.success("تم التفعيل بنجاح! 🚀")
            st.rerun()
        else:
            st.error("كود التفعيل غير صحيح أو منتهي الصلاحية!")
    
    st.stop()

# =========================================================
# 4. الواجهة الرئيسية للتطبيق (تظهر وتظل مفتوحة دائماً)
# =========================================================

# خيار لإلغاء التفعيل وتسجيل الخروج في الشريط الجانبي
with st.sidebar:
    st.write("⚙️ الإعدادات")
    if st.button("🔒 إلغاء التفعيل (تسجيل خروج)"):
        st.session_state.is_activated = False
        st.query_params.clear()
        st.rerun()

st.title("🚀 فودافون كاش 2026")
st.subheader("شحن كروت الفكة والمارد")

PRODUCTS_DETAILS = {
    "Fakka_2.5_Unite": {"name": "فكة 2.5 جنيه", "price": "1.75", "units": "45 وحدة"},
    "Fakka_4.25_Unite": {"name": "فكة 4.25 جنيه", "price": "2.97", "units": "190 وحدة"},
    "Fakka_5_Unite": {"name": "فكة 5 جنيه", "price": "3.50", "units": "225 وحدة"},
    "Fakka_7_Unite": {"name": "فكة 7 جنيه", "price": "4.90", "units": "300 وحدة"},
    "Fakka_9_Unite": {"name": "فكة 9 جنيه", "price": "6.30", "units": "400 وحدة"},
    "Fakka_10_Unite": {"name": "فكة 10 جنيه", "price": "7.00", "units": "450 وحدة"},
    "Fakka_10.5_Unite": {"name": "فكة 10.5 جنيه", "price": "7.35", "units": "400 وحدة + 50MB"},
    "Fakka_12_Unite": {"name": "فكة 12 جنيه", "price": "8.40", "units": "425 وحدة"},
    "Fakka_13.5_Unite": {"name": "فكة 13.5 جنيه", "price": "9.45", "units": "625 وحدة"},
    "Fakka_15_Unite": {"name": "فكة 15 جنيه", "price": "10.50", "units": "550 وحدة"},
    "Fakka_15.5_Unite": {"name": "فكة 15.5 جنيه", "price": "10.85", "units": "625 وحدة"},
    "Fakka_17.5_Unite": {"name": "فكة 17.5 جنيه", "price": "12.25", "units": "650 وحدة"},
    "Fakka_20_Unite": {"name": "فكة 20 جنيه", "price": "14.0", "units": "750 وحدة"},
    "Mared_10_Minuts": {"name": "مارد 10 دقايق", "price": "متغير", "units": "10 دقائق"},
    "Mared_10_Flexs": {"name": "مارد 10 فليكس", "price": "متغير", "units": "10 فليكس"},
    "Mared_10_Social": {"name": "مارد 10 سوشيال", "price": "متغير", "units": "10 سوشيال"},
}

selected_product_name = st.selectbox(
    "اختر الكرت المطلوب لشحنه:",
    options=list(PRODUCTS_DETAILS.keys()),
    format_func=lambda x: f"{PRODUCTS_DETAILS[x]['name']} ({PRODUCTS_DETAILS[x]['price']} ج - {PRODUCTS_DETAILS[x]['units']})"
)

st.write("---")

receiver = st.text_input("📱 رقم مستلم الشحن (11 رقم):", max_chars=11)
pin = st.text_input("🔒 الرقم السري للمحفظة:", type="password", max_chars=6)

if st.button("تأكيد الشحن 🚀", use_container_width=True):
    if not (receiver.startswith("01") and len(receiver) == 11):
        st.error("❌ رقم الهاتف غير صحيح!")
    elif not pin:
        st.error("❌ يرجى إدخال الرقم السري!")
    else:
        with st.spinner("⏳ جاري تنفيذ عملية الشحن..."):
            common_headers = {
                'User-Agent': "okhttp/4.12.0",
                'clientId': "AnaVodafoneAndroid",
                'Accept-Language': "ar",
                'x-agent-operatingsystem': "14",
                'x-agent-version': "2026.7.1",
                'x-agent-build': "1200",
                'digitalId': "26S0M71T0I2RK"
            }
            try:
                url_seamless = "http://mobile.vodafone.com.eg/checkSeamless/realms/vf-realm/protocol/openid-connect/auth?client_id=ana-vodafone-app-seamless"
                res1 = requests.get(url_seamless, headers=common_headers, timeout=15)
                s_data = res1.json()
                seamless_token = s_data.get('seamlessToken')
                sender_msisdn = s_data.get('msisdn')

                url_token = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
                auth_headers = common_headers.copy()
                auth_headers.update({'silentLogin': "true", 'seamlessToken': seamless_token, 'firstTimeLogin': "true"})
                res2 = requests.post(url_token, data={'grant_type': "password", 'client_secret': "b86e30a8-ae29-467a-a71f-65c73f2ff5e3", 'client_id': "cash-app"}, headers=auth_headers, timeout=15)
                access_token = res2.json().get('access_token')

                url_order = "https://mobile.vodafone.com.eg/services/dxl/pom/productOrder"
                payload_order = {
                    "channel": {"name": "MobileApp"},
                    "orderItem": [{
                        "action": "insert", "id": selected_product_name,
                        "product": {
                            "characteristic": [{"name": "PaymentMethod", "value": "VFCash"}, {"name": "USE_EMONEY", "value": "False"}, {"name": "MerchantCode", "value": ""}],
                            "id": selected_product_name,
                            "relatedParty": [{"id": str(sender_msisdn), "name": "MSISDN", "role": "Subscriber"}, {"id": receiver, "name": "Receiver", "role": "Receiver"}]
                        },
                        "@type": selected_product_name, "eCode": 0
                    }],
                    "relatedParty": [{"id": pin, "name": "pin", "role": "Requestor"}],
                    "@type": "CashFakkaAndMared"
                }
                order_headers = common_headers.copy()
                order_headers.update({'Accept': "application/json", 'Content-Type': "application/json", 'api-host': "ProductOrderingManagement", 'useCase': "CashFakkaAndMared", 'api-version': "v2", 'msisdn': f'0{sender_msisdn}', 'Authorization': f"Bearer {access_token}"})

                res3 = requests.post(url_order, data=json.dumps(payload_order), headers=order_headers, timeout=20)
                result = res3.json()

                if result.get('state') == 'Completed' or result.get('complete'):
                    st.success("🎉 تم الشحن بنجاح!")
                else:
                    msg = result.get('message') or result.get('description') or "فشل الشحن"
                    st.error(f"❌ {msg}")
            except Exception as err:
                st.error(f"❌ خطأ بالاتصال: {str(err)}")
