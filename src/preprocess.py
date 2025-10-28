"""
Data loading and preprocessing module
"""
import pandas as pd

def load_data(data_dir='data/'):
    """Load all CSV datasets"""
    try:
        orders = pd.read_csv(f'{data_dir}orders.csv')
        delivery = pd.read_csv(f'{data_dir}delivery_performance.csv')
        routes = pd.read_csv(f'{data_dir}routes_distance.csv')
        vehicles = pd.read_csv(f'{data_dir}vehicle_fleet.csv')
        warehouse = pd.read_csv(f'{data_dir}warehouse_inventory.csv')
        feedback = pd.read_csv(f'{data_dir}customer_feedback.csv')
        costs = pd.read_csv(f'{data_dir}cost_breakdown.csv')
        
        return orders, delivery, routes, vehicles, warehouse, feedback, costs
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

def clean_dataframe(df):
    """Clean and standardize dataframe"""
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Handle missing values - you can customize per dataset
    return df

def merge_datasets(orders, delivery, routes, costs):
    """Merge all order-related datasets"""
    main_df = orders.merge(delivery, on='Order_ID', how='left')
    main_df = main_df.merge(routes, on='Order_ID', how='left')
    main_df = main_df.merge(costs, on='Order_ID', how='left')
    
    return main_df
