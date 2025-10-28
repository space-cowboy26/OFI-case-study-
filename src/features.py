"""
Feature engineering module
"""
import pandas as pd

def engineer_features(main_df):
    """Create derived features for modeling"""
    
    # Calculate delay
    main_df['Delay_Days'] = main_df['Actual_Delivery_Days'] - main_df['Promised_Delivery_Days']
    main_df['Is_Delayed'] = (main_df['Delay_Days'] > 0).astype(int)
    
    # Calculate total cost
    main_df['Total_Cost'] = (
        main_df['Fuel_Cost'] + main_df['Labor_Cost'] + 
        main_df['Vehicle_Maintenance'] + main_df['Insurance'] + 
        main_df['Packaging_Cost'] + main_df['Technology_Platform_Fee'] + 
        main_df['Other_Overhead']
    )
    
    # Handle missing values
    main_df['Traffic_Delay_Minutes'] = main_df['Traffic_Delay_Minutes'].fillna(0)
    main_df['Weather_Impact'] = main_df['Weather_Impact'].fillna('None')
    main_df['Special_Handling'] = main_df['Special_Handling'].fillna('None')
    main_df['Customer_Rating'] = main_df['Customer_Rating'].fillna(3)
    
    # Cost per KM
    main_df['Cost_Per_KM'] = main_df['Total_Cost'] / (main_df['Distance_KM'] + 1)
    
    # Risk score based on multiple factors
    main_df['Route_Risk_Score'] = (
        (main_df['Distance_KM'] / main_df['Distance_KM'].max()) * 0.3 +
        (main_df['Traffic_Delay_Minutes'] / (main_df['Traffic_Delay_Minutes'].max() + 1)) * 0.4 +
        (main_df['Weather_Impact'] != 'None').astype(int) * 0.3
    )
    
    return main_df
