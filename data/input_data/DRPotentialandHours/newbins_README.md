# New Demand Response Binning Data and Hours
## Data Provided by Tina Jayaweera, Northwest Power and Conservation Council
## Documentation by Lily Hahn

For background on why new bins for DR products were developed, see newbinsrationale.pdf. The Northwest Power and Conservation Council found that with their original DR product projections for potential and hours of use, DR products were never being called online by the Regional Portfolio Model. As a result, they developed these new bins and hours of use as a sensitivity test. 

# About the DR Products
Bin 1 includes Demand Voltage Reduction (DVR) and Residential Time-of-Use (ResTOU). We can limit our analysis of the new bins to these products, which are acquired by the Regional Portfolio Model. This model has suggested that as a result of acquiring these products, greenhouse gas emissions are reduced by a cumulative 1.4 MMT. However, this model uses a simplistic calculation of greenhouse gas emissions reductions using time-averaged emissions factors. Our goal will be to use hourly emissions rates to determine the emissions impact of these products and compare with the model's estimate. 

# Navigating the spreadsheet for DR potential: 'DR RPM Inputs_021621_newaMWbins.xlsx'
In the "Reporter Outputs" sheet, see "Summer Potential" and "Winter Potential" sections with DR potential for each product in MW for years 2022-2041. We only need DVR and ResTOU.

# Hours of DR implementation
For each hour of the year, a 1 is listed for hours of DR implementation, or a 0 if DR is not implemented at that time.

# Shift versus shed
DVR is a shed product, so the load is reduced during hours of implementation. ResTOU is a shift product, so the load is reduced during hours of implementation but must be shifted to other hours of the day. However, TOU pilots suggest that this product often looks more like a shed product, with customers reducing their energy usage rather than shifting it. 

For the ResTOU product, we might want to try several shift assumptions such as:
1) treat this as a shed product, do not shift load
2) shift load to 10 pm-2 am (e.g. running the dishwasher and laundry at night)
3) shift load to 2 pm-6 pm
4) shift load to period producing maximum or minimum emissions reduction to get at bounds for this