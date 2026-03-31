/*
====================================================================================================
PROJECT     : Telecom Customer Churn Prediction (Cingular Wireless / Cell2Cell)
AUTHOR      : Abdelrahman
DATE        : 2026-03-30
DESCRIPTION : 
    This script performs a comprehensive Exploratory Data Analysis (EDA) and 
    Feature Selection process. 
    
    Key Actions:
    1.  Data Quality Audit: Scanned 58 features for Nulls, Zeros, and "Hidden" Unknowns.
    2.  Business Logic Validation: Investigated revenue-to-recurring charge gaps 
        and usage patterns.
    3.  Feature Selection: Reduced dimensionality from 58 to 21 "Champion" features 
        based on statistical significance and domain relevance (Telecom).
    4.  Target Audit: Verified 'Yes/No' churn distribution and checked for 
        Data Leakage across key categories.
    5.  Production View: Created 'train_data_final' as the primary source for 
        the Python Machine Learning pipeline.

DATABASE    : cell2cell
SOURCE TABLE: train_data
OUTPUT VIEW : train_data_final
====================================================================================================
*/
select * from train_data;

-- let's identify the Customer Churn percentage.
SELECT 
    churn,
    COUNT(*) AS customer_count,
    ROUND((COUNT(*) * 100.0 / (SELECT 
                    COUNT(*)
                FROM
                    train_data)),
            2) AS percentage
FROM
    train_data
GROUP BY churn;

-- churn rate is 28.82%


SELECT COUNT(*) 
FROM information_schema.columns 
WHERE table_schema = 'cell2cell' 
  AND table_name = 'train_data';

-- we have 58 columns in the dataset
-- let's check the columns further
SELECT column_name#, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'train_data';

-- this is to generate the code needed to calculate then nulls for all columns
SET PERSIST group_concat_max_len = 1000000;
select @@global.group_concat_max_len;
SELECT 
    GROUP_CONCAT(
        CONCAT(
            'SUM(', COLUMN_NAME, ' IS NULL) AS ', COLUMN_NAME, '_nulls, ',
            'ROUND(SUM(', COLUMN_NAME, ' IS NULL) / COUNT(*) * 100, 2) AS ', COLUMN_NAME, '_pct'
        ) 
        SEPARATOR ',\n'
    ) AS generated_sql
FROM information_schema.columns 
WHERE table_schema = 'cell2cell' 
  AND table_name = 'train_data';
  
  select SUM(ActiveSubs IS NULL) AS ActiveSubs_nulls, ROUND(SUM(ActiveSubs IS NULL) / COUNT(*) * 100, 2) AS ActiveSubs_pct,
SUM(AdjustmentsToCreditRating IS NULL) AS AdjustmentsToCreditRating_nulls, ROUND(SUM(AdjustmentsToCreditRating IS NULL) / COUNT(*) * 100, 2) AS AdjustmentsToCreditRating_pct,
SUM(AgeHH1 IS NULL) AS AgeHH1_nulls, ROUND(SUM(AgeHH1 IS NULL) / COUNT(*) * 100, 2) AS AgeHH1_pct,
SUM(AgeHH2 IS NULL) AS AgeHH2_nulls, ROUND(SUM(AgeHH2 IS NULL) / COUNT(*) * 100, 2) AS AgeHH2_pct,
SUM(BlockedCalls IS NULL) AS BlockedCalls_nulls, ROUND(SUM(BlockedCalls IS NULL) / COUNT(*) * 100, 2) AS BlockedCalls_pct,
SUM(BuysViaMailOrder IS NULL) AS BuysViaMailOrder_nulls, ROUND(SUM(BuysViaMailOrder IS NULL) / COUNT(*) * 100, 2) AS BuysViaMailOrder_pct,
SUM(CallForwardingCalls IS NULL) AS CallForwardingCalls_nulls, ROUND(SUM(CallForwardingCalls IS NULL) / COUNT(*) * 100, 2) AS CallForwardingCalls_pct,
SUM(CallWaitingCalls IS NULL) AS CallWaitingCalls_nulls, ROUND(SUM(CallWaitingCalls IS NULL) / COUNT(*) * 100, 2) AS CallWaitingCalls_pct,
SUM(ChildrenInHH IS NULL) AS ChildrenInHH_nulls, ROUND(SUM(ChildrenInHH IS NULL) / COUNT(*) * 100, 2) AS ChildrenInHH_pct,
SUM(Churn IS NULL) AS Churn_nulls, ROUND(SUM(Churn IS NULL) / COUNT(*) * 100, 2) AS Churn_pct,
SUM(CreditRating IS NULL) AS CreditRating_nulls, ROUND(SUM(CreditRating IS NULL) / COUNT(*) * 100, 2) AS CreditRating_pct,
SUM(CurrentEquipmentDays IS NULL) AS CurrentEquipmentDays_nulls, ROUND(SUM(CurrentEquipmentDays IS NULL) / COUNT(*) * 100, 2) AS CurrentEquipmentDays_pct,
SUM(CustomerCareCalls IS NULL) AS CustomerCareCalls_nulls, ROUND(SUM(CustomerCareCalls IS NULL) / COUNT(*) * 100, 2) AS CustomerCareCalls_pct,
SUM(CustomerID IS NULL) AS CustomerID_nulls, ROUND(SUM(CustomerID IS NULL) / COUNT(*) * 100, 2) AS CustomerID_pct,
SUM(DirectorAssistedCalls IS NULL) AS DirectorAssistedCalls_nulls, ROUND(SUM(DirectorAssistedCalls IS NULL) / COUNT(*) * 100, 2) AS DirectorAssistedCalls_pct,
SUM(DroppedBlockedCalls IS NULL) AS DroppedBlockedCalls_nulls, ROUND(SUM(DroppedBlockedCalls IS NULL) / COUNT(*) * 100, 2) AS DroppedBlockedCalls_pct,
SUM(DroppedCalls IS NULL) AS DroppedCalls_nulls, ROUND(SUM(DroppedCalls IS NULL) / COUNT(*) * 100, 2) AS DroppedCalls_pct,
SUM(HandsetModels IS NULL) AS HandsetModels_nulls, ROUND(SUM(HandsetModels IS NULL) / COUNT(*) * 100, 2) AS HandsetModels_pct,
SUM(HandsetPrice IS NULL) AS HandsetPrice_nulls, ROUND(SUM(HandsetPrice IS NULL) / COUNT(*) * 100, 2) AS HandsetPrice_pct,
SUM(HandsetRefurbished IS NULL) AS HandsetRefurbished_nulls, ROUND(SUM(HandsetRefurbished IS NULL) / COUNT(*) * 100, 2) AS HandsetRefurbished_pct,
SUM(Handsets IS NULL) AS Handsets_nulls, ROUND(SUM(Handsets IS NULL) / COUNT(*) * 100, 2) AS Handsets_pct,
SUM(HandsetWebCapable IS NULL) AS HandsetWebCapable_nulls, ROUND(SUM(HandsetWebCapable IS NULL) / COUNT(*) * 100, 2) AS HandsetWebCapable_pct,
SUM(HasCreditCard IS NULL) AS HasCreditCard_nulls, ROUND(SUM(HasCreditCard IS NULL) / COUNT(*) * 100, 2) AS HasCreditCard_pct,
SUM(Homeownership IS NULL) AS Homeownership_nulls, ROUND(SUM(Homeownership IS NULL) / COUNT(*) * 100, 2) AS Homeownership_pct,
SUM(InboundCalls IS NULL) AS InboundCalls_nulls, ROUND(SUM(InboundCalls IS NULL) / COUNT(*) * 100, 2) AS InboundCalls_pct,
SUM(IncomeGroup IS NULL) AS IncomeGroup_nulls, ROUND(SUM(IncomeGroup IS NULL) / COUNT(*) * 100, 2) AS IncomeGroup_pct,
SUM(MadeCallToRetentionTeam IS NULL) AS MadeCallToRetentionTeam_nulls, ROUND(SUM(MadeCallToRetentionTeam IS NULL) / COUNT(*) * 100, 2) AS MadeCallToRetentionTeam_pct,
SUM(MaritalStatus IS NULL) AS MaritalStatus_nulls, ROUND(SUM(MaritalStatus IS NULL) / COUNT(*) * 100, 2) AS MaritalStatus_pct,
SUM(MonthlyMinutes IS NULL) AS MonthlyMinutes_nulls, ROUND(SUM(MonthlyMinutes IS NULL) / COUNT(*) * 100, 2) AS MonthlyMinutes_pct,
SUM(MonthlyRevenue IS NULL) AS MonthlyRevenue_nulls, ROUND(SUM(MonthlyRevenue IS NULL) / COUNT(*) * 100, 2) AS MonthlyRevenue_pct,
SUM(MonthsInService IS NULL) AS MonthsInService_nulls, ROUND(SUM(MonthsInService IS NULL) / COUNT(*) * 100, 2) AS MonthsInService_pct,
SUM(NewCellphoneUser IS NULL) AS NewCellphoneUser_nulls, ROUND(SUM(NewCellphoneUser IS NULL) / COUNT(*) * 100, 2) AS NewCellphoneUser_pct,
SUM(NonUSTravel IS NULL) AS NonUSTravel_nulls, ROUND(SUM(NonUSTravel IS NULL) / COUNT(*) * 100, 2) AS NonUSTravel_pct,
SUM(NotNewCellphoneUser IS NULL) AS NotNewCellphoneUser_nulls, ROUND(SUM(NotNewCellphoneUser IS NULL) / COUNT(*) * 100, 2) AS NotNewCellphoneUser_pct,
SUM(Occupation IS NULL) AS Occupation_nulls, ROUND(SUM(Occupation IS NULL) / COUNT(*) * 100, 2) AS Occupation_pct,
SUM(OffPeakCallsInOut IS NULL) AS OffPeakCallsInOut_nulls, ROUND(SUM(OffPeakCallsInOut IS NULL) / COUNT(*) * 100, 2) AS OffPeakCallsInOut_pct,
SUM(OptOutMailings IS NULL) AS OptOutMailings_nulls, ROUND(SUM(OptOutMailings IS NULL) / COUNT(*) * 100, 2) AS OptOutMailings_pct,
SUM(OutboundCalls IS NULL) AS OutboundCalls_nulls, ROUND(SUM(OutboundCalls IS NULL) / COUNT(*) * 100, 2) AS OutboundCalls_pct,
SUM(OverageMinutes IS NULL) AS OverageMinutes_nulls, ROUND(SUM(OverageMinutes IS NULL) / COUNT(*) * 100, 2) AS OverageMinutes_pct,
SUM(OwnsComputer IS NULL) AS OwnsComputer_nulls, ROUND(SUM(OwnsComputer IS NULL) / COUNT(*) * 100, 2) AS OwnsComputer_pct,
SUM(OwnsMotorcycle IS NULL) AS OwnsMotorcycle_nulls, ROUND(SUM(OwnsMotorcycle IS NULL) / COUNT(*) * 100, 2) AS OwnsMotorcycle_pct,
SUM(PeakCallsInOut IS NULL) AS PeakCallsInOut_nulls, ROUND(SUM(PeakCallsInOut IS NULL) / COUNT(*) * 100, 2) AS PeakCallsInOut_pct,
SUM(PercChangeMinutes IS NULL) AS PercChangeMinutes_nulls, ROUND(SUM(PercChangeMinutes IS NULL) / COUNT(*) * 100, 2) AS PercChangeMinutes_pct,
SUM(PercChangeRevenues IS NULL) AS PercChangeRevenues_nulls, ROUND(SUM(PercChangeRevenues IS NULL) / COUNT(*) * 100, 2) AS PercChangeRevenues_pct,
SUM(PrizmCode IS NULL) AS PrizmCode_nulls, ROUND(SUM(PrizmCode IS NULL) / COUNT(*) * 100, 2) AS PrizmCode_pct,
SUM(ReceivedCalls IS NULL) AS ReceivedCalls_nulls, ROUND(SUM(ReceivedCalls IS NULL) / COUNT(*) * 100, 2) AS ReceivedCalls_pct,
SUM(ReferralsMadeBySubscriber IS NULL) AS ReferralsMadeBySubscriber_nulls, ROUND(SUM(ReferralsMadeBySubscriber IS NULL) / COUNT(*) * 100, 2) AS ReferralsMadeBySubscriber_pct,
SUM(RespondsToMailOffers IS NULL) AS RespondsToMailOffers_nulls, ROUND(SUM(RespondsToMailOffers IS NULL) / COUNT(*) * 100, 2) AS RespondsToMailOffers_pct,
SUM(RetentionCalls IS NULL) AS RetentionCalls_nulls, ROUND(SUM(RetentionCalls IS NULL) / COUNT(*) * 100, 2) AS RetentionCalls_pct,
SUM(RetentionOffersAccepted IS NULL) AS RetentionOffersAccepted_nulls, ROUND(SUM(RetentionOffersAccepted IS NULL) / COUNT(*) * 100, 2) AS RetentionOffersAccepted_pct,
SUM(RoamingCalls IS NULL) AS RoamingCalls_nulls, ROUND(SUM(RoamingCalls IS NULL) / COUNT(*) * 100, 2) AS RoamingCalls_pct,
SUM(RVOwner IS NULL) AS RVOwner_nulls, ROUND(SUM(RVOwner IS NULL) / COUNT(*) * 100, 2) AS RVOwner_pct,
SUM(ServiceArea IS NULL) AS ServiceArea_nulls, ROUND(SUM(ServiceArea IS NULL) / COUNT(*) * 100, 2) AS ServiceArea_pct,
SUM(ThreewayCalls IS NULL) AS ThreewayCalls_nulls, ROUND(SUM(ThreewayCalls IS NULL) / COUNT(*) * 100, 2) AS ThreewayCalls_pct,
SUM(TotalRecurringCharge IS NULL) AS TotalRecurringCharge_nulls, ROUND(SUM(TotalRecurringCharge IS NULL) / COUNT(*) * 100, 2) AS TotalRecurringCharge_pct,
SUM(TruckOwner IS NULL) AS TruckOwner_nulls, ROUND(SUM(TruckOwner IS NULL) / COUNT(*) * 100, 2) AS TruckOwner_pct,
SUM(UnansweredCalls IS NULL) AS UnansweredCalls_nulls, ROUND(SUM(UnansweredCalls IS NULL) / COUNT(*) * 100, 2) AS UnansweredCalls_pct,
SUM(UniqueSubs IS NULL) AS UniqueSubs_nulls, ROUND(SUM(UniqueSubs IS NULL) / COUNT(*) * 100, 2) AS UniqueSubs_pct
  from train_data;
  -- most of the columns have zero nulls, the rest has less than 2% but we will investigate the hidden nulls
  
  -- let's find columns that has high zero percentage and unkonwn values 
  -- finding zeros
 SELECT 
    GROUP_CONCAT(
        CONCAT(
            'SELECT "', COLUMN_NAME, '" AS col_name, ',
            'ROUND(SUM(', COLUMN_NAME, ' = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data'
        ) 
        SEPARATOR '\n UNION ALL \n'
    ) AS final_query
FROM information_schema.columns 
WHERE table_schema = 'cell2cell' 
  AND table_name = 'train_data'
  AND DATA_TYPE IN ('int', 'decimal', 'float', 'bigint', 'tinyint', 'double');
  
  
SELECT "ActiveSubs" AS col_name, ROUND(SUM(ActiveSubs = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "AdjustmentsToCreditRating" AS col_name, ROUND(SUM(AdjustmentsToCreditRating = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "AgeHH1" AS col_name, ROUND(SUM(AgeHH1 = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "AgeHH2" AS col_name, ROUND(SUM(AgeHH2 = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "BlockedCalls" AS col_name, ROUND(SUM(BlockedCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "CallForwardingCalls" AS col_name, ROUND(SUM(CallForwardingCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "CallWaitingCalls" AS col_name, ROUND(SUM(CallWaitingCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "CurrentEquipmentDays" AS col_name, ROUND(SUM(CurrentEquipmentDays = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "CustomerCareCalls" AS col_name, ROUND(SUM(CustomerCareCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "CustomerID" AS col_name, ROUND(SUM(CustomerID = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "DirectorAssistedCalls" AS col_name, ROUND(SUM(DirectorAssistedCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "DroppedBlockedCalls" AS col_name, ROUND(SUM(DroppedBlockedCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "DroppedCalls" AS col_name, ROUND(SUM(DroppedCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "HandsetModels" AS col_name, ROUND(SUM(HandsetModels = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "Handsets" AS col_name, ROUND(SUM(Handsets = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "InboundCalls" AS col_name, ROUND(SUM(InboundCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "IncomeGroup" AS col_name, ROUND(SUM(IncomeGroup = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "MonthlyMinutes" AS col_name, ROUND(SUM(MonthlyMinutes = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "MonthlyRevenue" AS col_name, ROUND(SUM(MonthlyRevenue = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "MonthsInService" AS col_name, ROUND(SUM(MonthsInService = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "OffPeakCallsInOut" AS col_name, ROUND(SUM(OffPeakCallsInOut = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "OutboundCalls" AS col_name, ROUND(SUM(OutboundCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "OverageMinutes" AS col_name, ROUND(SUM(OverageMinutes = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "PeakCallsInOut" AS col_name, ROUND(SUM(PeakCallsInOut = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "PercChangeMinutes" AS col_name, ROUND(SUM(PercChangeMinutes = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "PercChangeRevenues" AS col_name, ROUND(SUM(PercChangeRevenues = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "ReceivedCalls" AS col_name, ROUND(SUM(ReceivedCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "ReferralsMadeBySubscriber" AS col_name, ROUND(SUM(ReferralsMadeBySubscriber = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "RetentionCalls" AS col_name, ROUND(SUM(RetentionCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "RetentionOffersAccepted" AS col_name, ROUND(SUM(RetentionOffersAccepted = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "RoamingCalls" AS col_name, ROUND(SUM(RoamingCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "ThreewayCalls" AS col_name, ROUND(SUM(ThreewayCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "TotalRecurringCharge" AS col_name, ROUND(SUM(TotalRecurringCharge = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "UnansweredCalls" AS col_name, ROUND(SUM(UnansweredCalls = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
 UNION ALL 
SELECT "UniqueSubs" AS col_name, ROUND(SUM(UniqueSubs = 0) / COUNT(*) * 100, 2) AS zero_pct FROM train_data
order by zero_pct desc;
  
  -- finding "Unknown" or "Wrong" Values 
  
SELECT 
    GROUP_CONCAT(
        CONCAT(
            'SELECT "', COLUMN_NAME, '" AS col_name, ',
            'ROUND(SUM(UPPER(TRIM(', COLUMN_NAME, ')) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data'
        ) 
        SEPARATOR '\n UNION ALL \n'
    ) AS final_query
FROM information_schema.columns 
WHERE table_schema = 'cell2cell' 
  AND table_name = 'train_data'
  AND DATA_TYPE IN ('varchar', 'char', 'text');
  
 SELECT "BuysViaMailOrder" AS col_name, ROUND(SUM(UPPER(TRIM(BuysViaMailOrder)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "ChildrenInHH" AS col_name, ROUND(SUM(UPPER(TRIM(ChildrenInHH)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "Churn" AS col_name, ROUND(SUM(UPPER(TRIM(Churn)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "CreditRating" AS col_name, ROUND(SUM(UPPER(TRIM(CreditRating)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "HandsetPrice" AS col_name, ROUND(SUM(UPPER(TRIM(HandsetPrice)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "HandsetRefurbished" AS col_name, ROUND(SUM(UPPER(TRIM(HandsetRefurbished)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "HandsetWebCapable" AS col_name, ROUND(SUM(UPPER(TRIM(HandsetWebCapable)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "HasCreditCard" AS col_name, ROUND(SUM(UPPER(TRIM(HasCreditCard)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "Homeownership" AS col_name, ROUND(SUM(UPPER(TRIM(Homeownership)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "MadeCallToRetentionTeam" AS col_name, ROUND(SUM(UPPER(TRIM(MadeCallToRetentionTeam)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "MaritalStatus" AS col_name, ROUND(SUM(UPPER(TRIM(MaritalStatus)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "NewCellphoneUser" AS col_name, ROUND(SUM(UPPER(TRIM(NewCellphoneUser)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "NonUSTravel" AS col_name, ROUND(SUM(UPPER(TRIM(NonUSTravel)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "NotNewCellphoneUser" AS col_name, ROUND(SUM(UPPER(TRIM(NotNewCellphoneUser)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "Occupation" AS col_name, ROUND(SUM(UPPER(TRIM(Occupation)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "OptOutMailings" AS col_name, ROUND(SUM(UPPER(TRIM(OptOutMailings)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "OwnsComputer" AS col_name, ROUND(SUM(UPPER(TRIM(OwnsComputer)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "OwnsMotorcycle" AS col_name, ROUND(SUM(UPPER(TRIM(OwnsMotorcycle)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "PrizmCode" AS col_name, ROUND(SUM(UPPER(TRIM(PrizmCode)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "RespondsToMailOffers" AS col_name, ROUND(SUM(UPPER(TRIM(RespondsToMailOffers)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "RVOwner" AS col_name, ROUND(SUM(UPPER(TRIM(RVOwner)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "ServiceArea" AS col_name, ROUND(SUM(UPPER(TRIM(ServiceArea)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
 UNION ALL 
SELECT "TruckOwner" AS col_name, ROUND(SUM(UPPER(TRIM(TruckOwner)) IN ("UNKNOWN", "U", "?", "NONE", "")) / COUNT(*) * 100, 2) AS unknown_pct FROM train_data
order by unknown_pct desc;

select churn, MonthlyRevenue, TotalRecurringCharge, PercChangeRevenues
  
from train_data	
where MonthlyRevenue <= 0;

-- I created a View to identify the status of customer's plan 

create view PlanStatus as 
select churn, (case when MonthlyRevenue - TotalRecurringCharge between -0.50 and 0.50 then "On Plan"
when MonthlyRevenue > TotalRecurringCharge + 0.50 then "Over-Payer"
else "Discounted"
end) as Status
from train_data;

select * from PlanStatus;
select count(*) as count, Status, churn
from planstatus 
group by 2, 3
order by 2;


select distinct occupation 
from train_data;
-- I checked the Cardinality of the Occupation feature to make sure how many values we have, we have 8 

-- here's the final training data after feature selection from 58 to 21 features 
create view train_data_final as 
select churn, MonthlyRevenue, TotalRecurringCharge, OverageMinutes, PercChangeRevenues,
MonthlyMinutes, PercChangeMinutes, RoamingCalls, DroppedCalls, BlockedCalls, CustomerCareCalls,
MonthsInService, CurrentEquipmentDays, HandsetPrice, HandsetRefurbished, HandsetWebCapable,
AgeHH1, CreditRating, IncomeGroup, Occupation, ReferralsMadeBySubscriber
from train_data;

select * from train_data_final;

-- some Sanity checks 
select churn from train_data
where churn != "Yes" and "No";

select MonthlyMinutes, MonthlyRevenue 
from train_data_final
where MonthlyMinutes = 0;

select max(MonthlyRevenue)
from train_data_final 
where MonthlyMinutes = 0;

select max(OverageMinutes), avg(OverageMinutes)
from train_data_final;
-- max overage mins is 4321 and the average is 40



-- Final Target Audit for Churn Leakage/Bias
SELECT 'CreditRating' AS feature, CreditRating AS value, COUNT(*) AS total, 
ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct 
FROM train_data_final GROUP BY 1, 2
UNION ALL
SELECT 'Occupation', Occupation, COUNT(*), 
ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
FROM train_data_final GROUP BY 1, 2
UNION ALL
SELECT 'HandsetWebCapable', HandsetWebCapable, COUNT(*), 
ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
FROM train_data_final GROUP BY 1, 2
UNION ALL
SELECT 'HandsetRefurbished', HandsetRefurbished, COUNT(*), 
ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
FROM train_data_final GROUP BY 1, 2
UNION ALL
SELECT 'IncomeGroup', IncomeGroup, COUNT(*), 
ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
FROM train_data_final GROUP BY 1, 2
ORDER BY feature, churn_rate_pct DESC;

-- we found out that there is no value has a churn more than 37.35%

select * from train_data_final;