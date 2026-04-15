first I imported the data to do some EDA and preprocess the data so we can prepare for the tranforamtion file

I checked the data types of the columns to see which is dummies and which numrical 

Step 1: Handling Nulls and Lying Zeros

then I checked if cols had any nulls 

I found that 
MonthlyRevenue               120
TotalRecurringCharge         120
OverageMinutes               120
RoamingCalls                 120
MonthlyMinutes               120

so I thought that they are inactive customer so they probably churned

but I did some calculations and it turned out these null values does represent churners they're just random


MonthlyRevenue	TotalRecurringCharge	OverageMinutes	PercChangeRevenues	RoamingCalls	MonthlyMinutes
churn						
No	65	65	65	125	65	65
Yes	55	55	55	165	55	55


also for the 
PercChangeRevenues           290
PercChangeMinutes            290
I thought maybe those are the inactive one or probably new customers 
as change get calculated on month over month 
and if this is the customer's first month then it would give us null

and I checked that also and it turned out they are not new customers


cause I checked the MonthsInService for these nulls and found many customers had been with the company for 12, 18, or 24+ months.

so I checked their monthly minutes for this exact month and I found they did have minutes

so my hypothesis there are customer who were not active and then came back and reactivated their service
it might be   data logging error also

Now I imputed the data 
I checked the distrubition of all columns that has nulls 
and I found that all of them were Skewed data 

So I imputed with the Median 


Also I decided to add a Missing Indcator columns for all variables that have 
more than 0.1% nulls 
to make the model able to catch the signals of the nulls so we don't miss anything 

but right before that I handled the lying zero in columns like 
HandsetPrice, AgeHH1, IncomeGroup cause they cannot have zeros so I replaced them with nulls


Step 2: Handling Outliers 
First I calculated the difference between the max value and the 99% percentile

and I had huge outliers 

and I decided to Cap the outliers to 99% percentile
before the scaling cause I didn't want the scaling to affected with those huge outliers

Step: 3 Mapping the Dummies

I mapped the dummies using the ordinalencoder from the sklearn
instead of doing it manually 


Step 4: Scalling the data 

I scaled the the Extremem features that has huge variance and outliers
with Robust scaler 
I didn't use the log scaler cause some variables had negtives 

and the stable ones I used standerscaler 