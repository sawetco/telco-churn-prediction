# Modeli yükleyip tahmin yapıyoruz.
import joblib
import numpy as np
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, 'models', 'model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'models', 'scaler.pkl'))
feature_names = joblib.load(os.path.join(BASE_DIR, 'models', 'feature_names.pkl'))

# pydantic field adı → gerçek feature adı eşleştirmesi
FIELD_MAP = {
    'MultipleLines_No_phone_service': 'MultipleLines_No phone service',
    'MultipleLines_Yes': 'MultipleLines_Yes',
    'InternetService_Fiber_optic': 'InternetService_Fiber optic',
    'InternetService_No': 'InternetService_No',
    'Contract_One_year': 'Contract_One year',
    'Contract_Two_year': 'Contract_Two year',
    'PaymentMethod_Credit_card_automatic': 'PaymentMethod_Credit card (automatic)',
    'PaymentMethod_Electronic_check': 'PaymentMethod_Electronic check',
    'PaymentMethod_Mailed_check': 'PaymentMethod_Mailed check',
}

def predict_churn(data: dict) -> dict:
    # field adlarını gerçek feature adlarına çevir
    mapped = {}
    for key, value in data.items():
        real_key = FIELD_MAP.get(key, key)
        mapped[real_key] = value

    # numpy array yerine DataFrame kullan → warning ortadan kalkar
    input_df = pd.DataFrame([mapped])[feature_names]

    input_scaled = scaler.transform(input_df)

    churn = int(model.predict(input_scaled)[0])
    probability = float(model.predict_proba(input_scaled)[0][1])

    message = "Bu müşteri ayrılabilir!" if churn == 1 else "Bu müşteri kalacak."

    return {
        "churn": churn,
        "probability": round(probability, 4),
        "message": message
    }