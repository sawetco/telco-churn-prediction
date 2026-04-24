import streamlit as st
import requests
import os

st.set_page_config(page_title="Telco Churn Prediction", page_icon="📡", layout="centered")

st.title("Telco Müşteri Kaybı Tahmin Sistemi")
st.markdown("Müşteri bilgilerini girerek ayrılıp ayrılmayacağını tahmin edin.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Kişisel Bilgiler")
    gender = st.selectbox("Cinsiyet", ["Male", "Female"])
    senior = st.selectbox("Yaşlı Vatandaş mı?", ["No", "Yes"])
    partner = st.selectbox("Eşi var mı?", ["No", "Yes"])
    dependents = st.selectbox("Bakmakla yükümlü kişi var mı?", ["No", "Yes"])
    tenure = st.slider("Kaç aydır müşteri?", 0, 72, 12)

with col2:
    st.subheader("Sözleşme Bilgileri")
    contract = st.selectbox("Sözleşme Tipi", ["Month-to-month", "One year", "Two year"])
    paperless = st.selectbox("Kağıtsız Fatura?", ["No", "Yes"])
    payment = st.selectbox("Ödeme Yöntemi", [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ])
    monthly = st.number_input("Aylık Ücret ($)", 0.0, 200.0, 65.0)
    total = st.number_input("Toplam Ücret ($)", 0.0, 10000.0, 1000.0)

st.divider()
st.subheader("Hizmet Bilgileri")

col3, col4 = st.columns(2)

with col3:
    phone = st.selectbox("Telefon Hizmeti", ["No", "Yes"])
    multiple_lines = st.selectbox("Birden Fazla Hat", ["No", "Yes", "No phone service"])
    internet = st.selectbox("İnternet Hizmeti", ["DSL", "Fiber optic", "No"])
    online_security = st.selectbox("Online Güvenlik", ["No", "Yes", "No internet service"])
    online_backup = st.selectbox("Online Yedekleme", ["No", "Yes", "No internet service"])

with col4:
    device_protection = st.selectbox("Cihaz Koruma", ["No", "Yes", "No internet service"])
    tech_support = st.selectbox("Teknik Destek", ["No", "Yes", "No internet service"])
    streaming_tv = st.selectbox("TV Yayını", ["No", "Yes", "No internet service"])
    streaming_movies = st.selectbox("Film Yayını", ["No", "Yes", "No internet service"])

st.divider()

# API URL: Docker ortaminda "api", lokalde "localhost"
API_HOST = os.environ.get("API_HOST", "api")
API_URL = f"http://{API_HOST}:8000/predict"

if st.button("Tahmin Et", use_container_width=True, type="primary"):
    # Ham/kategorik veriyi dogrudan gonder - preprocessing API tarafinda yapilir
    payload = {
        "gender": gender,
        "SeniorCitizen": 1 if senior == "Yes" else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple_lines,
        "InternetService": internet,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total,
    }

    with st.spinner("Tahmin yapılıyor..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            st.divider()

            if result["churn"] == 1:
                st.error(f"⚠️ Bu müşteri ayrılabilir!")
            else:
                st.success(f"✅ Bu müşteri kalacak.")

            st.metric("Ayrılma Olasılığı", f"%{round(result['probability'] * 100, 1)}")

        except requests.exceptions.ConnectionError:
            st.error(f"API'ye bağlanılamadı. FastAPI çalışıyor mu? (URL: {API_URL})")
        except requests.exceptions.HTTPError as e:
            st.error(f"API hatası: {e.response.text}")
        except Exception as e:
            st.error(f"Beklenmeyen hata: {e}")
