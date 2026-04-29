import streamlit as st
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

st.set_page_config(page_title="Cell2Cell Churn Predictor", layout="wide", page_icon="📞")

# SIDEBAR: Project Background Placeholder
st.sidebar.header("📋 Project Background")
st.sidebar.markdown("""
### Context
*Goal: Identify high-value churn risks (Top 20% MRR).

Output: Real-time probability, Risk Status, and Retention Actions.*

### Model Logic
Ensemble: Soft-Voting (RF + XGBoost).

Strategy: Cost-Sensitive thresholds to minimize False Negatives.

Thresholds: 0.35 (VIP) | 0.50 (Standard).
""")

# MAIN PAGE

st.title("📞 Customer Churn Decision Intelligence")
st.markdown("Enter customer metrics below to generate a risk profile and recommended retention action.")

#  User Inputs organized in Columns
st.subheader("Customer Profile Features")

with st.form("churn_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### 💰 Financials")
        monthly_rev = st.number_input("Monthly Revenue ($)", min_value=-50.0,  value=50.0, help="Average monthly charges")
        recurring = st.number_input("Total Recurring Charge ($)", min_value=-20.0, max_value=500.0, value=40.0)
        overage = st.number_input("Overage Minutes", min_value=0.0, value=0.0)
        perc_rev = st.number_input("% Change in Revenue", value=0.0)
        
        st.markdown("##### 👥 Demographics")
        age = st.number_input("Age (HH1)", min_value=18.0, max_value=100.0, value=35.0)
        income = st.number_input("Income Group (0-9)", min_value=0, max_value=9, value=5)
        occupation = st.selectbox("Occupation", ["Professional", "Student", "Retired", "Other", "Clerical", "Self", "Crafts", "Homemaker"])

    with col2:
        st.markdown("##### 📶 Usage Patterns")
        monthly_mins = st.number_input("Monthly Minutes", min_value=0.0, value=400.0)
        perc_mins = st.number_input("% Change in Minutes", value=0.0)
        roaming = st.number_input("Roaming Calls", min_value=0.0, value=0.0)
        dropped = st.number_input("Dropped Calls", min_value=0.0, value=0.0)
        blocked = st.number_input("Blocked Calls", min_value=0.0, value=0.0)
        cust_care = st.number_input("Customer Care Calls", min_value=0.0, value=0.0)
        referrals = st.number_input("Referrals Made", min_value=0, value=0)

    with col3:
        st.markdown("##### 📱 Equipment & Credit")
        months_service = st.number_input("Months In Service", min_value=1, value=12)
        equip_days = st.number_input("Current Equipment Days", min_value=0.0, value=300.0)
        handset_price = st.selectbox("Handset Price", ["Unknown", "30", "40", "80", "100", "150", "200", "250", "300", "400", "500"])
        refurbished = st.selectbox("Handset Refurbished", ["No", "Yes"])
        web_capable = st.selectbox("Handset Web Capable", ["Yes", "No"])
        credit = st.selectbox("Credit Rating", ["1-Highest", "2-High", "3-Good", "4-Medium", "5-Low", "6-VeryLow", "7-Lowest"])

    submit_button = st.form_submit_button("Generate Risk Profile")

# 3. Prediction Execution
if submit_button:
    # Map inputs to CustomData
    data = CustomData(
        MonthlyRevenue=monthly_rev,
        TotalRecurringCharge=recurring,
        OverageMinutes=overage,
        PercChangeRevenues=perc_rev,
        MonthlyMinutes=monthly_mins,
        PercChangeMinutes=perc_mins,
        RoamingCalls=roaming,
        DroppedCalls=dropped,
        BlockedCalls=blocked,
        CustomerCareCalls=cust_care,
        MonthsInService=months_service,
        CurrentEquipmentDays=equip_days,
        HandsetPrice=handset_price,
        HandsetRefurbished=refurbished,
        HandsetWebCapable=web_capable,
        AgeHH1=age,
        CreditRating=credit,
        IncomeGroup=income,
        Occupation=occupation,
        ReferralsMadeBySubscriber=referrals
    )

    # Convert to DF
    features_df = data.get_data_as_data_frame()

    # Trigger Pipeline (pointing to saved_models!)
    predict_pipeline = PredictPipeline()
    prob, status, risk, action = predict_pipeline.predict(features_df)

    # 4. Results Dashboard
    st.markdown("---")
    st.header("🔍 Prediction Results")
    
    r_col1, r_col2, r_col3 = st.columns(3)
    
    with r_col1:
        st.metric("Churn Probability", f"{prob:.2%}")
    with r_col2:
        st.metric("Customer Segment", status)
    with r_col3:
        # Visual color mapping
        risk_colors = {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "blue", "LOW": "green"}
        st.markdown(f"**Risk Severity:** :{risk_colors.get(risk, 'grey')}[{risk}]")

    # Final "Action Card"
    if risk in ["CRITICAL", "HIGH"]:
        st.error(f"🚨 **RECOMMENDED ACTION:** {action}")
    elif risk == "MEDIUM":
        st.warning(f"⚠️ **RECOMMENDED ACTION:** {action}")
    else:
        st.success(f"✅ **RESULT:** {action}")