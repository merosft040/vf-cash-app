import requests
import json
import streamlit as st

# ---------- إعدادات الصفحة ----------
st.set_page_config(
    page_title="نظام شحن فودافون كاش",
    page_icon="🚀",
    layout="centered"
)

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
    ("فكة 12 جنيه", "Fakka_12_Unite"), ("فكة 12.5 جنيه", "Fakka_12.5_Unite"),
    ("فكة 13 جنيه", "Fakka_13_Unite"), ("فكة 13.5 جنيه", "Fakka_13.5_Unite"),
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

# خريطة الأسماء للاختيار السهل
product_options = {name: pid for name, pid in ALL_PRODUCTS}

# واجهة المستخدم
st.markdown("<h1 style='text-align: center; color: #ff3333;'>🚀 كاش 2026 🚀</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>شحن كروت الفكة والمارد</h3>", unsafe_allow_html=True)
st.divider()

# اختيار الكرت
selected_product_name = st.selectbox("اختر الكرت المطلوب لشحنه:", list(product_options.keys()))
product_id = product_options[selected_product_name]

# عرض تفاصيل الكرت المختار
details = PRODUCTS_DETAILS.get(product_id, {})
st.info(f"💰 السعر: {details.get('price')} ج | 📊 الوحدات: {details.get('units')} | ⏰ المدة: {details.get('duration')}")

# المدخلات
sender_msisdn = st.text_input("أدخل رقم المرسل (رقمك 11 رقم):", max_chars=11)
receiver = st.text_input("رقم مستلم الشحن (11 رقم):", max_chars=11)
pin = st.text_input("الرقم السري للمحفظة:", type="password", max_chars=6)
seamless_token = st.text_input("أدخل الـ Seamless Token (اختياري):", type="password")

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

if st.button("🚀 تأكيد الشحن"):
    if not sender_msisdn or not receiver or not pin:
        st.error("❌ برجاء إدخال جميع البيانات المطلوبة (رقم المرسل، رقم المستلم، والرقم السري).")
    elif not (receiver.startswith("01") and len(receiver) == 11):
        st.error("❌ رقم المستلم غير صحيح.")
    else:
        with st.spinner("⏳ جاري الاتصال الآمن بسيرفرات فودافون..."):
            try:
                # 1. الحصول على Access Token
                url_token = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
                auth_headers = common_headers.copy()
                auth_headers.update({'silentLogin': "true", 'seamlessToken': seamless_token, 'firstTimeLogin': "true"})
                
                token_response = requests.post(url_token, data={
                    'grant_type': "password", 
                    'client_secret': "b86e30a8-ae29-467a-a71f-65c73f2ff5e3", 
                    'client_id': "cash-app"
                }, headers=auth_headers, timeout=20)
                
                if token_response.status_code not in [200, 201]:
                    st.error(f"❌ خطأ من السيرفر ({token_response.status_code}) في جلب الصلاحية.")
                else:
                    token_data = token_response.json()
                    access_token = token_data.get('access_token')

                    # 2. تنفيذ أمر الشحن
                    url_order = "https://mobile.vodafone.com.eg/services/dxl/pom/productOrder"
                    formatted_sender = str(sender_msisdn).replace('01', '1', 1) if sender_msisdn.startswith('0') else sender_msisdn
                    
                    payload_order = {
                        "channel": {"name": "MobileApp"},
                        "orderItem": [{
                            "action": "insert", "id": product_id,
                            "product": {
                                "characteristic": [{"name": "PaymentMethod", "value": "VFCash"}, {"name": "USE_EMONEY", "value": "False"}, {"name": "MerchantCode", "value": ""}],
                                "id": product_id,
                                "relatedParty": [{"id": formatted_sender, "name": "MSISDN", "role": "Subscriber"}, {"id": receiver, "name": "Receiver", "role": "Receiver"}]
                            },
                            "@type": product_id, "eCode": 0
                        }],
                        "relatedParty": [{"id": pin, "name": "pin", "role": "Requestor"}],
                        "@type": "CashFakkaAndMared"
                    }
                    
                    order_headers = common_headers.copy()
                    order_headers.update({
                        'Accept': "application/json", 
                        'Content-Type': "application/json", 
                        'api-host': "ProductOrderingManagement", 
                        'useCase': "CashFakkaAndMared", 
                        'api-version': "v2", 
                        'msisdn': sender_msisdn, 
                        'Authorization': f"Bearer {access_token}"
                    })

                    order_response = requests.post(url_order, data=json.dumps(payload_order), headers=order_headers, timeout=25)
                    
                    if order_response.status_code in [200, 201]:
                        result = order_response.json()
                        if result.get('state') == 'Completed' or result.get('complete'):
                            st.success("🎉 مبروك! تم الشحن بنجاح.")
                        else:
                            msg = result.get('message') or result.get('description') or "رصيد غير كافي أو خطأ في البيانات"
                            st.error(f"❌ فشل الشحن: {msg}")
                    else:
                        st.error(f"❌ خطأ من السيرفر ({order_response.status_code}) أثناء تنفيذ عملية الشحن.")
            
            except Exception as e:
                st.error(f"❌ حدث خطأ غير متوقع: {str(e)}")
