# Modeli yükleyip tahmin yapıyoruz.
# API artık ham veriyi alır, preprocessing burada yapılır.
import joblib
import os
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, 'models', 'model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'models', 'scaler.pkl'))
feature_names = joblib.load(os.path.join(BASE_DIR, 'models', 'feature_names.pkl'))


def preprocess(data: dict) -> pd.DataFrame:
    """Ham müşteri verisini modelin beklediği formata dönüştürür.

    Notebook'taki preprocessing adımlarının aynısını uygular:
    1. Binary encoding (Yes/No -> 1/0)
    2. One-hot encoding (kategorik sutunlar)
    3. Feature siralamasini model ile eslestir
    """
    row = {}

    # gender: Male=1, Female=0
    row['gender'] = 1 if data['gender'] == 'Male' else 0

    # Sayisal degerler
    row['SeniorCitizen'] = data['SeniorCitizen']
    row['tenure'] = data['tenure']
    row['MonthlyCharges'] = data['MonthlyCharges']
    row['TotalCharges'] = data['TotalCharges']

    # Binary encoding: Yes -> 1, No -> 0, No internet/phone service -> 0
    binary_fields = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling',
                     'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                     'TechSupport', 'StreamingTV', 'StreamingMovies']
    for field in binary_fields:
        row[field] = 1 if data[field] == 'Yes' else 0

    # One-Hot Encoding: MultipleLines
    ml = data['MultipleLines']
    row['MultipleLines_No phone service'] = 1 if ml == 'No phone service' else 0
    row['MultipleLines_Yes'] = 1 if ml == 'Yes' else 0

    # One-Hot Encoding: InternetService
    # drop_first=True -> DSL dusuruldu, kalanlar: Fiber optic, No
    inet = data['InternetService']
    row['InternetService_Fiber optic'] = 1 if inet == 'Fiber optic' else 0
    row['InternetService_No'] = 1 if inet == 'No' else 0

    # One-Hot Encoding: Contract
    # drop_first=True -> Month-to-month dusuruldu
    contract = data['Contract']
    row['Contract_One year'] = 1 if contract == 'One year' else 0
    row['Contract_Two year'] = 1 if contract == 'Two year' else 0

    # One-Hot Encoding: PaymentMethod
    # drop_first=True -> Bank transfer (automatic) dusuruldu
    payment = data['PaymentMethod']
    row['PaymentMethod_Credit card (automatic)'] = 1 if payment == 'Credit card (automatic)' else 0
    row['PaymentMethod_Electronic check'] = 1 if payment == 'Electronic check' else 0
    row['PaymentMethod_Mailed check'] = 1 if payment == 'Mailed check' else 0

    # DataFrame olustur ve feature siralamasini eslestir
    input_df = pd.DataFrame([row])
    input_df = input_df[feature_names]

    return input_df


def predict_churn(data: dict) -> dict:
    """Ham müşteri verisinden churn tahmini üretir."""
    input_df = preprocess(data)
    input_scaled = scaler.transform(input_df)

    churn = int(model.predict(input_scaled)[0])
    probability = float(model.predict_proba(input_scaled)[0][1])

    message = "Bu müşteri ayrılabilir!" if churn == 1 else "Bu müşteri kalacak."

    return {
        "churn": churn,
        "probability": round(probability, 4),
        "message": message
    }
