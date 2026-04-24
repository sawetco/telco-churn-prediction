# Telco Müşteri Kaybı Tahmin Sistemi

Telekom sektöründe müşteri kaybını (churn) tahmin eden uçtan uca bir makine öğrenmesi projesi.

---

## Proje Hakkında

Bu proje, Kaggle'daki **Telco Customer Churn** veri seti kullanılarak geliştirilmiştir. Bir müşterinin hizmeti bırakıp bırakmayacağını tahmin eden bir model eğitilmiş ve bu model FastAPI ile servis haline getirilmiştir. Ayrıca Streamlit ile kullanıcı dostu bir web arayüzü geliştirilmiştir.

### Projenin Öne Çıkan Özellikleri

- **Genişletilmiş EDA**: Korelasyon matrisi, boxplot'lar, feature importance analizi
- **Çoklu model karşılaştırması**: Logistic Regression, Random Forest, XGBoost
- **Hiperparametre optimizasyonu**: GridSearchCV ile 5-fold cross-validation
- **Sınıf dengesizliği çözümleri**: class_weight='balanced' ve SMOTE denendi
- **Kullanıcı dostu API**: Ham/kategorik veriyi kabul eder, preprocessing dahili yapılır
- **Türkçe Streamlit arayüzü**
- **Docker ile containerized deployment**
- **API testleri**

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
│   ├── model.py                       # Model yükleme, preprocessing ve tahmin
│   └── schemas.py                     # Input/output veri tipleri
├── models/
│   ├── model.pkl                      # Eğitilmiş model (XGBoost)
│   ├── scaler.pkl                     # StandardScaler
│   └── feature_names.pkl              # Feature isimleri
├── tests/
│   └── test_api.py                    # API testleri
├── streamlit_app.py                   # Web arayüzü
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Kullanılan Teknolojiler

| Teknoloji | Amaç |
|---|---|
| Python 3.11+ | Ana programlama dili |
| Pandas, NumPy | Veri işleme |
| Scikit-learn, XGBoost | Model eğitimi ve değerlendirme |
| imbalanced-learn | SMOTE ile sınıf dengesizliği |
| FastAPI | REST API servisi |
| Streamlit | Web arayüzü |
| Docker | Containerization |

---

## Model Performansı

### Temel Model Karşılaştırması (ROC-AUC predict_proba ile düzeltilmiş)

| Model | Accuracy | F1 Score | ROC-AUC |
|---|---|---|---|
| Logistic Regression | 0.8038 | 0.6091 | 0.8358 |
| Random Forest | 0.7910 | 0.5625 | 0.8204 |
| XGBoost | 0.7783 | 0.5679 | 0.8196 |

### GridSearchCV Sonuçları (5-Fold Cross-Validation)

| Model | En İyi CV ROC-AUC | Test ROC-AUC | Test F1 |
|---|---|---|---|
| Logistic Regression | 0.8463 | 0.8352 | 0.6037 |
| **XGBoost** | **0.8490** | **0.8392** | 0.5835 |
| Random Forest | 0.8468 | 0.8376 | 0.6343 |

**Seçilen model**: XGBoost (GridSearchCV sonrası en yüksek Test ROC-AUC: 0.8392)
- En iyi parametreler: `learning_rate=0.1, max_depth=3, n_estimators=100`

### En Önemli Feature'lar

1. InternetService_Fiber optic
2. Contract_One year
3. Contract_Two year
4. InternetService_No
5. tenure

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
# Lokalde çalıştırırken API_HOST ortam değişkenini ayarla:
API_HOST=localhost streamlit run streamlit_app.py
```

---

## API Kullanımı

API çalışırken Swagger dokümantasyonuna erişmek için:

```
http://localhost:8000/docs
```

### POST /predict

Müşteri bilgilerini **ham/kategorik formatta** alır, churn tahmini döndürür. Preprocessing API içinde otomatik yapılır.

**Örnek istek:**

```json
{
  "gender": "Male",
  "SeniorCitizen": 0,
  "Partner": "No",
  "Dependents": "No",
  "tenure": 2,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "Fiber optic",
  "OnlineSecurity": "No",
  "OnlineBackup": "No",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 70.70,
  "TotalCharges": 151.65
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

Kaggle üzerindeki [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-churn) veri seti kullanılmıştır.

- **7043 müşteri**, **21 özellik**
- Hedef değişken: `Churn` (Yes/No)
- Sınıf dağılımı: %73 kalan, %27 ayrılan (dengesiz veri seti)

---

## Testleri Çalıştırma

```bash
pip install pytest httpx
pytest tests/test_api.py -v
```
