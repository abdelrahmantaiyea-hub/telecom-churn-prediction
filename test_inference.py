from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# 1. Create 'Fake' User Data (Matching your 20 features)
# Use a high MonthlyRevenue to test the VIP logic ($100 > $78.92)
data = CustomData(
    MonthlyRevenue=120.50, 
    TotalRecurringCharge=40.0,
    OverageMinutes=15.0,
    PercChangeRevenues=0.05,
    MonthlyMinutes=450.0,
    PercChangeMinutes=0.1,
    RoamingCalls=2.0,
    DroppedCalls=1.0,
    BlockedCalls=0.0,
    CustomerCareCalls=5.0,
    MonthsInService=24,
    CurrentEquipmentDays=300.0,
    HandsetPrice='200',
    HandsetRefurbished='No',
    HandsetWebCapable='Yes',
    AgeHH1=35.0,
    CreditRating='1-Highest',
    IncomeGroup=6,
    Occupation='Professional',
    ReferralsMadeBySubscriber=2
)

# 2. Get the DataFrame
features_df = data.get_data_as_data_frame()

# 3. Run the Pipeline
pipeline = PredictPipeline()
prob, status, risk, action = pipeline.predict(features_df)

# 4. Print results to verify
print("--- Prediction Results ---")
print(f"Probability: {prob:.2%}")
print(f"Status:      {status}")
print(f"Risk Level:  {risk}")
print(f"Action:      {action}")