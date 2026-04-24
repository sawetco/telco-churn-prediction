# API'ye gelen ve giden verilerin şeklini tanımlıyoruz.
from pydantic import BaseModel, Field

class CustomerInput(BaseModel):
    gender: int
    SeniorCitizen: int
    Partner: int
    Dependents: int
    tenure: int
    PhoneService: int
    OnlineSecurity: int
    OnlineBackup: int
    DeviceProtection: int
    TechSupport: int
    StreamingTV: int
    StreamingMovies: int
    PaperlessBilling: int
    MonthlyCharges: float
    TotalCharges: float
    MultipleLines_No_phone_service: int = Field(alias='MultipleLines_No phone service')
    MultipleLines_Yes: int = Field(alias='MultipleLines_Yes')
    InternetService_Fiber_optic: int = Field(alias='InternetService_Fiber optic')
    InternetService_No: int = Field(alias='InternetService_No')
    Contract_One_year: int = Field(alias='Contract_One year')
    Contract_Two_year: int = Field(alias='Contract_Two year')
    PaymentMethod_Credit_card_automatic: int = Field(alias='PaymentMethod_Credit card (automatic)')
    PaymentMethod_Electronic_check: int = Field(alias='PaymentMethod_Electronic check')
    PaymentMethod_Mailed_check: int = Field(alias='PaymentMethod_Mailed check')

    model_config = {"populate_by_name": True}

class PredictionOutput(BaseModel):
    churn: int
    probability: float
    message: str