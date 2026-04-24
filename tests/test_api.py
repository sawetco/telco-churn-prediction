"""FastAPI predict endpoint testleri."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Health check endpoint testi."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Telco Churn" in data["message"]


def test_predict_churn_high_risk():
    """Yüksek riskli müşteri (kısa tenure, fiber, aylık sözleşme) testi."""
    payload = {
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
        "TotalCharges": 151.65,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "churn" in data
    assert "probability" in data
    assert "message" in data
    assert data["churn"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0
    # Bu profil yüksek riskli olmalı
    assert data["churn"] == 1


def test_predict_churn_low_risk():
    """Düşük riskli müşteri (uzun tenure, iki yıllık sözleşme) testi."""
    payload = {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "Yes",
        "tenure": 60,
        "PhoneService": "Yes",
        "MultipleLines": "Yes",
        "InternetService": "DSL",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "Yes",
        "DeviceProtection": "Yes",
        "TechSupport": "Yes",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Two year",
        "PaperlessBilling": "No",
        "PaymentMethod": "Bank transfer (automatic)",
        "MonthlyCharges": 50.0,
        "TotalCharges": 3000.0,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["churn"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0
    # Bu profil düşük riskli olmalı
    assert data["churn"] == 0


def test_predict_response_format():
    """API yanıt formatı testi."""
    payload = {
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 12,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 50.0,
        "TotalCharges": 600.0,
    }
    response = client.post("/predict", json=payload)
    data = response.json()

    # Tüm gerekli alanlar mevcut mu?
    assert isinstance(data["churn"], int)
    assert isinstance(data["probability"], float)
    assert isinstance(data["message"], str)
    assert data["probability"] == round(data["probability"], 4)
