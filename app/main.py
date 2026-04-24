# API Uygulaması
from fastapi import FastAPI
from app.schemas import CustomerInput, PredictionOutput
from app.model import predict_churn

app = FastAPI(
    title="Telco Churn Prediction API",
    description="Müşteri kaybı tahmin servisi. Ham müşteri verisini alır, churn tahmini döndürür.",
    version="2.0.0"
)


@app.get("/")
def root():
    return {"message": "Telco Churn Prediction API çalışıyor!", "version": "2.0.0"}


@app.post("/predict", response_model=PredictionOutput)
def predict(customer: CustomerInput):
    result = predict_churn(customer.model_dump())
    return result
