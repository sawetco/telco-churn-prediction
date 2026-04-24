import streamlit as st
import requests

st.set_page_config(page_title="Telco Churn Prediction", page_icon="📡", layout="centered")

st.title("Telco Müşteri Kaybı Tahmin Sistemi")
st.markdown("Müşteri bilgilerini girerek ayrılıp ayrılmayacağını tahmin edin.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Kişisel Bilgiler")
    gender = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    senior = st.selectbox("Yaşlı Vatandaş mı?", ["Hayır", "Evet"])
    partner = st.selectbox("Eşi var mı?", ["Hayır", "Evet"])
    dependents = st.selectbox("Bakmakla yükümlü kişi var mı?", ["Hayır", "Evet"])
    tenure = st.slider("Kaç aydır müşteri?", 0, 72, 12)

with col2:
    st.subheader("Sözleşme Bilgileri")
    contract = st.selectbox("Sözleşme Tipi", ["Aylık", "Yıllık", "İki Yıllık"])
    paperless = st.selectbox("Kağıtsız Fatura?", ["Hayır", "Evet"])
    payment = st.selectbox("Ödeme Yöntemi", [
        "Elektronik Çek",
        "Posta Çeki", 
        "Banka Transferi (Otomatik)",
        "Kredi Kartı (Otomatik)"
    ])
    monthly = st.number_input("Aylık Ücret ($)", 0.0, 200.0, 65.0)
    total = st.number_input("Toplam Ücret ($)", 0.0, 10000.0, 1000.0)

st.divider()
st.subheader("Hizmet Bilgileri")

col3, col4 = st.columns(2)

with col3:
    phone = st.selectbox("Telefon Hizmeti", ["Hayır", "Evet"])
    multiple_lines = st.selectbox("Birden Fazla Hat", ["Hayır", "Evet", "Telefon hizmeti yok"])
    internet = st.selectbox("İnternet Hizmeti", ["DSL", "Fiber", "Yok"])
    online_security = st.selectbox("Online Güvenlik", ["Hayır", "Evet"])
    online_backup = st.selectbox("Online Yedekleme", ["Hayır", "Evet"])

with col4:
    device_protection = st.selectbox("Cihaz Koruma", ["Hayır", "Evet"])
    tech_support = st.selectbox("Teknik Destek", ["Hayır", "Evet"])
    streaming_tv = st.selectbox("TV Yayını", ["Hayır", "Evet"])
    streaming_movies = st.selectbox("Film Yayını", ["Hayır", "Evet"])

st.divider()

def encode(val):
    return 1 if val == "Evet" else 0

if st.button("Tahmin Et", use_container_width=True, type="primary"):
    payload = {
        "gender": 1 if gender == "Erkek" else 0,
        "SeniorCitizen": encode(senior),
        "Partner": encode(partner),
        "Dependents": encode(dependents),
        "tenure": tenure,
        "PhoneService": encode(phone),
        "OnlineSecurity": encode(online_security),
        "OnlineBackup": encode(online_backup),
        "DeviceProtection": encode(device_protection),
        "TechSupport": encode(tech_support),
        "StreamingTV": encode(streaming_tv),
        "StreamingMovies": encode(streaming_movies),
        "PaperlessBilling": encode(paperless),
        "MonthlyCharges": monthly,
        "TotalCharges": total,
        "MultipleLines_No phone service": 1 if multiple_lines == "Telefon hizmeti yok" else 0,
        "MultipleLines_Yes": 1 if multiple_lines == "Evet" else 0,
        "InternetService_Fiber optic": 1 if internet == "Fiber" else 0,
        "InternetService_No": 1 if internet == "Yok" else 0,
        "Contract_One year": 1 if contract == "Yıllık" else 0,
        "Contract_Two year": 1 if contract == "İki Yıllık" else 0,
        "PaymentMethod_Credit card (automatic)": 1 if payment == "Kredi Kartı (Otomatik)" else 0,
        "PaymentMethod_Electronic check": 1 if payment == "Elektronik Çek" else 0,
        "PaymentMethod_Mailed check": 1 if payment == "Posta Çeki" else 0,
    }

    with st.spinner("Tahmin yapılıyor..."):
        try:
            response = requests.post("http://api:8000/predict", json=payload)
            result = response.json()

            st.divider()

            if result["churn"] == 1:
                st.error(f"⚠️ Bu müşteri ayrılabilir!")
            else:
                st.success(f"✅ Bu müşteri kalacak.")

            st.metric("Ayrılma Olasılığı", f"%{round(result['probability'] * 100, 1)}")

        except Exception as e:
            st.error(f"API'ye bağlanılamadı: {e}. FastAPI çalışıyor mu?")