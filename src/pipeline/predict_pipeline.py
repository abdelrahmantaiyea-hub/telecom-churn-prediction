import os
import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    
    VIP_REVENUE_THRESHOLD = 78.92
    
    def __init__(self):
        pass

    def predict(self, features):
        
        
        try:

            model_path = os.path.join("saved_models", "model_trainer.pkl")
            preprocessor_path = os.path.join("saved_models", "preprocessor.pkl")

            logging_info = "Loading model and preprocessor for prediction..."

            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            data_scaled = preprocessor.transform(features)
            
            probability = model.predict_proba(data_scaled)[0][1]

            monthly_revenue = features['MonthlyRevenue'].iloc[0]

            status, risk, action = self.get_business_insights(probability, monthly_revenue)

            return probability, status, risk, action 
        
        except Exception as e:
            raise CustomException(sys, e)   

    def get_business_insights(self, probability, monthly_revenue):
    
    # 1. Identify Status
        is_vip = True if monthly_revenue >= self.VIP_REVENUE_THRESHOLD else False
        status = "VIP" if is_vip else "Standard"

        # 2. Apply the Logic Matrix
        if is_vip:
            if probability >= 0.60:
                risk_level = "CRITICAL"
                action = "Immediate Call from Relationship Manager"
            elif probability >= 0.35:
                risk_level = "HIGH"
                action = "Personalized Special Offer / Strategic Call"
            else:
                risk_level = "LOW"
                action = "Regular Monitoring"
        else:
            # Standard Customer Logic
            if probability >= 0.70:
                risk_level = "HIGH"
                action = " A Call from the Retention Team"
            elif probability >= 0.40:
                risk_level = "MEDIUM"
                action = "Send a Discount or Voucher via Email/SMS"
            else:
                risk_level = "LOW"
                action = "No Action Required"

        return status, risk_level, action     
        


class CustomData:
    def __init__(self, MonthlyRevenue: float,
                 TotalRecurringCharge: float,
                 OverageMinutes: float,
                 PercChangeRevenues: float,
                 MonthlyMinutes: float,
                 PercChangeMinutes: float,
                 RoamingCalls: float,
                 DroppedCalls: float,
                 BlockedCalls: float,
                 CustomerCareCalls: float,
                 MonthsInService: int,
                 CurrentEquipmentDays: float,
                 HandsetPrice: str,
                 HandsetRefurbished: str,
                 HandsetWebCapable: str,
                 AgeHH1: float,
                 CreditRating: str,
                 IncomeGroup: int,
                 Occupation: str,
                 ReferralsMadeBySubscriber: int):
        
        self.MonthlyRevenue = MonthlyRevenue
        self.TotalRecurringCharge = TotalRecurringCharge
        self.OverageMinutes = OverageMinutes
        self.PercChangeRevenues = PercChangeRevenues
        self.MonthlyMinutes = MonthlyMinutes
        self.PercChangeMinutes = PercChangeMinutes
        self.RoamingCalls = RoamingCalls
        self.DroppedCalls = DroppedCalls
        self.BlockedCalls = BlockedCalls
        self.CustomerCareCalls = CustomerCareCalls
        self.MonthsInService = MonthsInService
        self.CurrentEquipmentDays = CurrentEquipmentDays
        self.HandsetPrice = HandsetPrice
        self.HandsetRefurbished = HandsetRefurbished
        self.HandsetWebCapable = HandsetWebCapable
        self.AgeHH1 = AgeHH1
        self.CreditRating = CreditRating
        self.IncomeGroup = IncomeGroup
        self.Occupation = Occupation
        self.ReferralsMadeBySubscriber = ReferralsMadeBySubscriber

    def get_data_as_data_frame(self):

        try:

            # Mapping these into a Dictionary for Pandas
            custom_data_input_dict = {
                "MonthlyRevenue": [self.MonthlyRevenue],
                "TotalRecurringCharge": [self.TotalRecurringCharge],
                "OverageMinutes": [self.OverageMinutes],
                "PercChangeRevenues": [self.PercChangeRevenues],
                "MonthlyMinutes": [self.MonthlyMinutes],
                "PercChangeMinutes": [self.PercChangeMinutes],
                "RoamingCalls": [self.RoamingCalls],
                "DroppedCalls": [self.DroppedCalls],
                "BlockedCalls": [self.BlockedCalls],
                "CustomerCareCalls": [self.CustomerCareCalls],
                "MonthsInService": [self.MonthsInService],
                "CurrentEquipmentDays": [self.CurrentEquipmentDays],
                "HandsetPrice": [self.HandsetPrice],
                "HandsetRefurbished": [self.HandsetRefurbished],
                "HandsetWebCapable": [self.HandsetWebCapable],
                "AgeHH1": [self.AgeHH1],
                "CreditRating": [self.CreditRating],
                "IncomeGroup": [self.IncomeGroup],
                "Occupation": [self.Occupation],
                "ReferralsMadeBySubscriber": [self.ReferralsMadeBySubscriber],
            }

            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(sys, e)        
    

