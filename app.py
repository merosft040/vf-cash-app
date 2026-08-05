                # ... (جزء جلب التوكن زي ما هو فوق) ...

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
                
                # فحص الرد قبل تحويله لـ JSON لتجنب انهيار التطبيق
                if not res3.text.strip():
                    st.error("❌ السيرفر أرجع ردًا فارغًا (قد يكون هناك حظر مؤقت للـ IP أو ضغط على السيرفر).")
                else:
                    try:
                        result = res3.json()
                        if result.get('state') == 'Completed' or result.get('complete'):
                            st.success("🎉 تم الشحن بنجاح!")
                        else:
                            msg = result.get('message') or result.get('description') or "فشل الشحن"
                            st.error(f"❌ {msg}")
                    except json.JSONDecodeError:
                        st.error(f"❌ رد غير مسجل من السيرفر: {res3.text[:150]}")

            except Exception as err:
                st.error(f"❌ خطأ بالاتصال: {str(err)}")
