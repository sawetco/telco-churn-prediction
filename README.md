# Telco Müşteri Kaybı Tahmin Sistemi

Telekom sektöründe müşteri kaybını (churn) tahmin eden uçtan uca bir makine öğrenmesi projesi.

---

## Proje Hakkında

Bu proje, Kaggle'daki **Telco Customer Churn** veri seti kullanılarak geliştirilmiştir. Bir müşterinin hizmeti bırakıp bırakmayacağını tahmin eden bir model eğitilmiş ve bu model FastAPI ile servis haline getirilmiştir. Ayrıca Streamlit ile kullanıcı dostu bir web arayüzü geliştirilmiştir.

---

## Proje Yapısı

```
telco-churn-prediction/
├── data/
│   └── telco_customer_churn.csv       # Ham veri seti
├── notebooks/
│   └── eda_and_training.ipynb         # Keşifsel veri analizi ve model eğitimi
├── app/
│   ├── main.py                        # FastAPI uygulaması
│   ├── model.py                       # Model yükleme ve tahmin fonksiyonu
│   └── schemas.py                     # Input/output veri tipleri
├── models/
│   ├── model.pkl                      # Eğitilmiş model
│   ├── scaler.pkl                     # StandardScaler
│   └── feature_names.pkl              # Feature isimleri
├── streamlit_app.py                   # Web arayüzü
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Kullanılan Teknolojiler

| Teknoloji | Amaç |
|---|---|
| Python 3.11 | Ana programlama dili |
| Pandas, NumPy | Veri işleme |
| Scikit-learn, XGBoost | Model eğitimi |
| FastAPI | REST API servisi |
| Streamlit | Web arayüzü |
| Docker | Containerization |

---

## Model Performansı

3 farklı model denenmiş ve karşılaştırılmıştır:

| Model | Accuracy | F1 Score | ROC-AUC |
|---|---|---|---|
| Logistic Regression | 0.8038 | 0.6091 | **0.7308** |
| Random Forest | 0.7910 | 0.5625 | 0.6999 |
| XGBoost | 0.7783 | 0.5679 | 0.7048 |

En yüksek ROC-AUC skoruna sahip **Logistic Regression** modeli seçilmiştir.

---

## Kurulum ve Çalıştırma

### Yöntem 1: Docker ile (Önerilen)

Docker Desktop'ın çalıştığından emin ol, ardından:

```bash
docker-compose up --build
```

- **API:** http://localhost:8000/docs
- **UI:** http://localhost:8501

### Yöntem 2: Klasik Kurulum

Gereksinimleri yükle:

```bash
pip install -r requirements.txt
```

FastAPI'yi başlat (Terminal 1):

```bash
uvicorn app.main:app --reload
```

Streamlit arayüzünü başlat (Terminal 2):

```bash
streamlit run streamlit_app.py
```

---

## API Kullanımı

API çalışırken Swagger dokümantasyonuna erişmek için:

```
http://localhost:8000/docs
```

### POST /predict

Müşteri bilgilerini alır, churn tahmini döndürür.

**Örnek istek:**

```json
{
  "gender": 1,
  "SeniorCitizen": 0,
  "Partner": 0,
  "Dependents": 0,
  "tenure": 2,
  "PhoneService": 1,
  "OnlineSecurity": 0,
  "OnlineBackup": 0,
  "DeviceProtection": 0,
  "TechSupport": 0,
  "StreamingTV": 0,
  "StreamingMovies": 0,
  "PaperlessBilling": 1,
  "MonthlyCharges": 70.70,
  "TotalCharges": 151.65,
  "MultipleLines_No phone service": 0,
  "MultipleLines_Yes": 0,
  "InternetService_Fiber optic": 1,
  "InternetService_No": 0,
  "Contract_One year": 0,
  "Contract_Two year": 0,
  "PaymentMethod_Credit card (automatic)": 0,
  "PaymentMethod_Electronic check": 1,
  "PaymentMethod_Mailed check": 0
}
```

**Örnek yanıt:**

```json
{
  "churn": 1,
  "probability": 0.6836,
  "message": "Bu müşteri ayrılabilir!"
}
```

---

## Veri Seti

Kaggle üzerindeki [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) veri seti kullanılmıştır.

- **7043 müşteri**, **21 özellik**
- Hedef değişken: `Churn` (Yes/No)
- Sınıf dağılımı: %73 kalan, %27 ayrılan