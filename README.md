# NexGen Logistics Intelligence System

**AI-Powered Delivery Optimization & Intervention Recommender**

A comprehensive logistics analytics platform that leverages machine learning to predict delivery delays, recommend operational interventions, and optimize fleet management for NexGen Logistics Pvt. Ltd.(sample case study)

---

## Problem Statement

NexGen Logistics, a mid-sized logistics company operating across India with international connections to Singapore, Dubai, Hong Kong, and Bangkok, faces critical operational challenges:

- **Delivery Performance Issues**: Inconsistent on-time delivery rates affecting customer satisfaction
- **Operational Inefficiencies**: Suboptimal route planning and vehicle allocation
- **Cost Pressures**: Rising operational costs without clear visibility into cost drivers
- **Limited Innovation**: Reactive rather than predictive operational approach
- **Sustainability Concerns**: Lack of data-driven insights for reducing carbon footprint

**Mission**: Transform NexGen from reactive to predictive operations using data analytics and AI-powered recommendations to achieve 15-20% cost reduction and significant improvement in customer satisfaction.

---

## Solution Overview

The **NexGen Logistics Intelligence System** is an interactive Streamlit-based dashboard that provides:

1. **Predictive Analytics**: ML-powered delay prediction with risk scoring
2. **Smart Recommendations**: Context-aware operational interventions for at-risk deliveries
3. **Performance Monitoring**: Real-time KPIs and carrier performance tracking
4. **Fleet Optimization**: Vehicle and route recommendations based on efficiency and sustainability
5. **Data Export**: Comprehensive reporting and data export capabilities

---

## Key Features

### Analytics Dashboard
- Delivery status distribution visualization (pie charts)
- Cost analysis by product category with gradient color coding
- Carrier performance benchmarking across 5 partners
- Feature importance analysis showing key delay prediction factors

### Risk Predictor
- Order-level delay risk scoring (0-100 scale)
- Interactive risk gauge with color-coded alerts (Green/Yellow/Red zones)
- Detailed order information display including route and value
- AI-powered intervention recommendations based on risk level

### Operational Recommendations
- High-risk order identification and prioritization (top 10 at-risk orders)
- Fleet efficiency recommendations ranked by CO2 emissions
- Vehicle availability tracking by location (Mumbai, Delhi, Bangalore, Chennai, Kolkata)
- Warehouse optimization suggestions based on storage costs

### Export & Reporting
- Filtered data download in CSV format
- Model performance reports with accuracy and ROC-AUC metrics
- Business impact calculations showing potential savings
- ROI projections based on delay reduction
## Usage Guide

### Dashboard Navigation

**Sidebar Controls:**
- Filter by Customer Segment (Enterprise, SMB, Individual)
- Filter by Priority (Express, Standard, Economy)
- Filter by Product Category (Electronics, Fashion, Healthcare, Food & Beverage, Industrial, Books, Home Goods)

**Tab 1 - Analytics:**
- View delivery status distribution across On-Time, Slightly-Delayed, and Severely-Delayed
- Analyze cost patterns by product category
- Compare carrier performance (GlobalTransit, QuickShip, SpeedyLogistics, ReliableExpress, EcoDeliver)
- Understand key delay prediction factors through feature importance

**Tab 2 - Risk Predictor:**
1. Select an Order ID from the dropdown menu
2. View order details including product, segment, priority, route, and value
3. See risk score on the gauge (0-40 Green: Low Risk, 40-70 Yellow: Moderate Risk, 70-100 Red: High Risk)
4. Read AI-generated recommendations tailored to the risk level

**Tab 3 - Recommendations:**
- Identify top 10 high-risk orders requiring immediate attention
- View most efficient vehicles ranked by CO2 emissions
- Check vehicle availability by location for optimal fleet allocation

**Tab 4 - Export:**
- Download filtered data as CSV for external analysis
- Generate model performance report with accuracy metrics
- View business impact metrics including potential savings

 

 

## Model Performance

### Algorithm Details
- **Model Type**: Random Forest Classifier
- **Configuration**: 100 estimators, max_depth=5
- **Training Method**: 80-20 train-test split with random_state=42

### Current Performance Metrics
- **Accuracy**: 53.3%
- **ROC-AUC Score**: 0.54
- **Training samples**: 150 orders with complete data
- **Test samples**: 30 orders

### Feature Importance
1. **Total_Cost** (35.3%) - Strongest predictor
2. **Distance_KM** (19.7%)
3. **Order_Value_INR** (18.1%)
4. **Promised_Delivery_Days** (16.9%)
5. **Traffic_Delay_Minutes** (9.9%)

### Model Limitations & Insights

**Current Challenges:**
- Small dataset (150 samples) limits model learning capacity
- Weak feature correlations with delay target variable
- Total Cost correlation: 0.272 (weak positive)
- Distance correlation: -0.023 (negligible)
- Traffic Delay correlation: 0.006 (negligible)

**Carrier Performance Analysis:**
- GlobalTransit: 63.6% delay rate (worst performer)
- ReliableExpress: 52.5% delay rate
- SpeedyLogistics: 51.2% delay rate
- EcoDeliver: 37.5% delay rate
- QuickShip: 25.8% delay rate (best performer)
## Business Impact

### Current State Analysis
- **Total Orders**: 200 in dataset
- **Delayed Orders**: 70 (35% delay rate)
- **Average Delay**: 1.08 days per delayed order
- **Cost Variability**: High across product categories
### Projected Improvements

**Operational Efficiency:**
- **15-20% cost reduction** through optimized routing and vehicle assignment
- **30% reduction in delays** via predictive interventions
- **Improved fleet utilization** reducing idle time by 25%
- **Fuel cost savings** through optimal route selection

**Customer Experience:**
- **Proactive communication** for at-risk orders
- **Improved satisfaction scores** through reliability
- **Reduced customer complaints** about delays
- **Enhanced brand reputation** through data-driven operations

### ROI Calculation

**Conservative Estimate:**
- Delayed orders in sample: 70
- Potential savings per delay avoided: Rs. 500
- Monthly sample projection: Rs. 35,000 savings
- Annual projection (scaled): Rs. 4,20,000+ savings

**Additional Benefits:**
- Reduced compensation/refund costs
- Lower customer churn rate
- Improved carrier negotiations through performance data
- Enhanced operational decision-making

---
