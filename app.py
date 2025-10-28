"""
NexGen Logistics Intelligence System
Main Streamlit Application
"""
import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from src.preprocess import load_data, clean_dataframe, merge_datasets
from src.features import engineer_features
from src.modeling import train_delay_predictor
from src.recommend import recommend_interventions
from src.visualization import (
    plot_delay_distribution, 
    plot_cost_by_category,
    plot_carrier_performance,
    plot_feature_importance,
    plot_risk_gauge,
    plot_vehicle_availability
)

# Page Configuration
st.set_page_config(
    page_title="NexGen Logistics Recommender",
    
    layout="wide"
)

#  CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_prepare_data():
    """Load and prepare all datasets"""
    try:
        orders, delivery, routes, vehicles, warehouse, feedback, costs = load_data()
        
        # Merge Datasets
        main_df = merge_datasets(orders, delivery, routes, costs)
        
        # Engineer Features
        main_df = engineer_features(main_df)
        
        return main_df, vehicles, warehouse, feedback
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None, None

@st.cache_resource
def train_model(df):
    """Train the ML model"""
    return train_delay_predictor(df)

# Main App
st.markdown('<h1 class="main-header"> NexGen Logistics Intelligence System</h1>', unsafe_allow_html=True)
st.markdown("### AI-Powered Delivery Optimization & Intervention Recommender")

# Load Data
with st.spinner("Loading data..."):
    main_df, vehicles, warehouse, feedback = load_and_prepare_data()

if main_df is not None:
    # Train Model
    with st.spinner("Training predictive model..."):
        model, feature_cols, accuracy, roc_auc, importances = train_model(main_df)
    
    # Sidebar Filters
    st.sidebar.header(" Dashboard Controls")
    
    selected_segment = st.sidebar.multiselect(
        "Customer Segment",
        options=main_df['Customer_Segment'].unique(),
        default=main_df['Customer_Segment'].unique()
    )
    
    selected_priority = st.sidebar.multiselect(
        "Priority",
        options=main_df['Priority'].unique(),
        default=main_df['Priority'].unique()
    )
    
    selected_category = st.sidebar.multiselect(
        "Product Category",
        options=main_df['Product_Category'].unique(),
        default=main_df['Product_Category'].unique()
    )
    
    # Filter Data
    filtered_df = main_df[
        (main_df['Customer_Segment'].isin(selected_segment)) &
        (main_df['Priority'].isin(selected_priority)) &
        (main_df['Product_Category'].isin(selected_category))
    ]
    
    # Key Metrics
    st.header(" Performance Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", len(filtered_df))
    with col2:
        delayed = filtered_df['Is_Delayed'].sum()
        st.metric("Delayed Orders", delayed, f"{delayed/len(filtered_df)*100:.1f}%")
    with col3:
        avg_rating = filtered_df['Customer_Rating'].mean()
        st.metric("Avg Rating", f"{avg_rating:.2f}")
    with col4:
        st.metric("Model Accuracy", f"{accuracy*100:.1f}%")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([" Analytics", " Risk Predictor", " Recommendations", " Export"])
    
    with tab1:
        st.subheader("Delivery Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = plot_delay_distribution(filtered_df)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = plot_cost_by_category(filtered_df)
            st.plotly_chart(fig2, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig3 = plot_carrier_performance(filtered_df)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            fig4 = plot_feature_importance(importances)
            st.plotly_chart(fig4, use_container_width=True)
    
    with tab2:
        st.subheader(" Delivery Risk Prediction")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Select Order for Prediction")
            order_ids = filtered_df['Order_ID'].dropna().unique()
            selected_order = st.selectbox("Order ID", order_ids)
            
            if selected_order:
                order_data = filtered_df[filtered_df['Order_ID'] == selected_order].iloc[0]
                
                st.markdown("**Order Details:**")
                st.write(f" Product: {order_data['Product_Category']}")
                st.write(f" Segment: {order_data['Customer_Segment']}")
                st.write(f" Priority: {order_data['Priority']}")
                st.write(f" Route: {order_data['Origin']} → {order_data['Destination']}")
                st.write(f" Value: ₹{order_data['Order_Value_INR']:.2f}")
        
        with col2:
            if selected_order:
                # Predict Risk
                order_features = order_data[feature_cols].values.reshape(1, -1)
                risk_proba = model.predict_proba(order_features)[0, 1]
                
                st.markdown("#### Risk Assessment")
                
                fig_gauge = plot_risk_gauge(risk_proba)
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                # Recommendations
                st.markdown("####  Smart Recommendations")
                recommendations = recommend_interventions(order_data, risk_proba, vehicles, warehouse)
                for rec in recommendations:
                    st.markdown(f"- {rec}")
    
    with tab3:
        st.subheader(" Operational Insights & Recommendations")
        
        # High-risk orders
        high_risk_df = filtered_df[filtered_df['Is_Delayed'] == 1].copy()
        
        if len(high_risk_df) > 0:
            st.markdown("###  High-Risk Orders Requiring Attention")
            
            risk_features = high_risk_df[feature_cols].dropna()
            if len(risk_features) > 0:
                risk_scores = model.predict_proba(risk_features)[:, 1]
                high_risk_df.loc[risk_features.index, 'Risk_Score'] = risk_scores
                
                top_risk = high_risk_df.nlargest(10, 'Risk_Score')[
                    ['Order_ID', 'Customer_Segment', 'Product_Category', 'Origin', 
                     'Destination', 'Delay_Days', 'Risk_Score']
                ]
                
                st.dataframe(top_risk, use_container_width=True)
        
        # vehicle optimization
        st.markdown("###  Fleet Optimization Recommendations")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Most Efficient Vehicles (by CO2)**")
            top_vehicles = vehicles.nsmallest(5, 'CO2_Emissions_Kg_per_KM')[
                ['Vehicle_ID', 'Vehicle_Type', 'CO2_Emissions_Kg_per_KM', 'Fuel_Efficiency_KM_per_L']
            ]
            st.dataframe(top_vehicles, use_container_width=True)
        
        with col2:
            fig_vehicles = plot_vehicle_availability(vehicles)
            st.plotly_chart(fig_vehicles, use_container_width=True)
    
    with tab4:
        st.subheader(" Export Data & Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Download Filtered Data")
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                label=" Download CSV",
                data=csv_data,
                file_name="nexgen_logistics_data.csv",
                mime="text/csv"
            )
        
        with col2:
            st.markdown("#### Model Performance Report")
            report = f"""
# NexGen Logistics ML Model Report

## Model Performance
- Accuracy: {accuracy*100:.2f}%
- ROC-AUC Score: {roc_auc:.3f}

## Dataset Summary
- Total Orders: {len(main_df)}
- Delayed Orders: {main_df['Is_Delayed'].sum()}
- Average Delay: {main_df['Delay_Days'].mean():.2f} days

## Top Features
{importances.to_string()}
"""
            st.download_button(
                label=" Download Report",
                data=report,
                file_name="model_report.txt",
                mime="text/plain"
            )
        
        # Business Impact
        st.markdown("###  Estimated Business Impact")
        
        total_delayed = main_df['Is_Delayed'].sum()
        potential_savings = total_delayed * 500
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Delayed Orders", total_delayed)
        with col2:
            st.metric("Potential Savings", f"₹{potential_savings:,.0f}")
        with col3:
            improvement = (1 - main_df['Is_Delayed'].mean()) * 100
            st.metric("Target Improvement", f"{improvement:.1f}%")

else:
    st.error("Failed to load data. Please check your data files.")

# Footer
 