# API'ye gelen ve giden verilerin şeklini tanımlıyoruz.
# API artık ham/kategorik veriyi kabul eder, preprocessing dahili yapılır.
from pydantic import BaseModel, Field
from typing import Optional


class CustomerInput(BaseModel):
    """Müşteri bilgileri - ham/kategorik veri formatında."""
    gender: str = Field(description="Male veya Female", examples=["Male", "Female"])
    SeniorCitizen: int = Field(description="Yaşlı vatandaş mı? (0 veya 1)", ge=0, le=1)
    Partner: str = Field(description="Eşi var mı? (Yes/No)", examples=["Yes", "No"])
    Dependents: str = Field(description="Bakmakla yükümlü kişi var mı? (Yes/No)", examples=["Yes", "No"])
    tenure: int = Field(description="Kaç aydır müşteri?", ge=0, le=120)
    PhoneService: str = Field(description="Telefon hizmeti var mı? (Yes/No)", examples=["Yes", "No"])
    MultipleLines: str = Field(
        description="Birden fazla hat var mı?",
        examples=["Yes", "No", "No phone service"]
    )
    InternetService: str = Field(
        description="İnternet hizmeti türü",
        examples=["DSL", "Fiber optic", "No"]
    )
    OnlineSecurity: str = Field(description="Online güvenlik var mı? (Yes/No/No internet service)")
    OnlineBackup: str = Field(description="Online yedekleme var mı? (Yes/No/No internet service)")
    DeviceProtection: str = Field(description="Cihaz koruma var mı? (Yes/No/No internet service)")
    TechSupport: str = Field(description="Teknik destek var mı? (Yes/No/No internet service)")
    StreamingTV: str = Field(description="TV yayını var mı? (Yes/No/No internet service)")
    StreamingMovies: str = Field(description="Film yayını var mı? (Yes/No/No internet service)")
    Contract: str = Field(
        description="Sözleşme tipi",
        examples=["Month-to-month", "One year", "Two year"]
    )
    PaperlessBilling: str = Field(description="Kağıtsız fatura? (Yes/No)")
    PaymentMethod: str = Field(
        description="Ödeme yöntemi",
        examples=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    )
    MonthlyCharges: float = Field(description="Aylık ücret ($)", ge=0)
    TotalCharges: float = Field(description="Toplam ücret ($)", ge=0)


class PredictionOutput(BaseModel):
    """Tahmin sonucu."""
    churn: int = Field(description="1 = Ayrılacak, 0 = Kalacak")
    probability: float = Field(description="Ayrılma olasılığı (0-1)")
    message: str = Field(description="Açıklama mesajı")
