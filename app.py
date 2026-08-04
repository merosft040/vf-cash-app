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

# 3. التحقق من حالة التفعيل في جلسة المتصفح
if "is_activated" not in st.session_state:
    st.session_state.is_activated = False

# 4. شاشة التفعيل (تظهر فقط لو لم يتم التفعيل في الجلسة الحالية)
if not st.session_state.is_activated:
    st.title("🔑 تفعيل التطبيق (نسخة سحابية)")
    user_key = st.text_input("أدخل كود الاشتراك للاختبار:", type="password")
    
    if st.button("تفعيل", use_container_width=True):
        if user_key:
            clean_key = user_key.strip()
            try:
                response = supabase.table("activations").select("*").eq("key_code", clean_key).execute()
                data = response.data
                
                if data:
                    # حفظ التفعيل في الجلسة الحالية
                    st.session_state.is_activated = True
                    st.success("تم التفعيل بنجاح! 🚀")
                    st.rerun()
                else:
                    st.error("❌ كود التفعيل غير صحيح أو غير موجود بالقاعدة!")
            except Exception as db_err:
                st.error(f"❌ خطأ في قاعدة البيانات: {db_err}")
        else:
            st.warning("يرجى كتابة الكود!")
    st.stop()

# =========================================================
# 5. الواجهة الرئيسية للتطبيق (تظهر مباشرة بعد التفعيل)
# =========================================================

with st.sidebar:
    st.write("⚙️ الإعدادات")
    st.success("🟢 التطبيق مفعل ودائم")
    if st.button("إلغاء التفعيل / تسجيل الخروج"):
        st.session_state.is_activated = False
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
                *# بقية الهيدرز...*
            }
            try:
                # عمليات الشحن كما هي
                st.success("🎉 تم الشحن بنجاح!")
            except Exception as err:
                st.error(f"❌ خطأ بالاتصال: {str(err)}")
