"""
Visualization functions module
"""
import plotly.express as px
import plotly.graph_objects as go

def plot_delay_distribution(df):
    """Plot delivery status distribution"""
    delay_counts = df['Delivery_Status'].value_counts()
    fig = px.pie(
        values=delay_counts.values, 
        names=delay_counts.index,
        title="Delivery Status Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig

def plot_cost_by_category(df):
    """Plot average cost by product category"""
    cost_by_category = df.groupby('Product_Category')['Total_Cost'].mean().sort_values()
    fig = px.bar(
        x=cost_by_category.values,
        y=cost_by_category.index,
        orientation='h',
        title="Average Cost by Product Category",
        labels={
            'x': 'Average Cost (INR)', 
            'y': 'Product Category',
            'color': 'Cost (INR)'  
        },
        color=cost_by_category.values,
        color_continuous_scale='Blues'
    )
    return fig


def plot_carrier_performance(df):
    """Plot carrier delay rate"""
    carrier_perf = df.groupby('Carrier').agg({
        'Is_Delayed': 'mean',
        'Customer_Rating': 'mean'
    }).round(2)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=carrier_perf.index,
        y=carrier_perf['Is_Delayed'],
        name='Delay Rate',
        marker_color='indianred'
    ))
    fig.update_layout(
        title="Carrier Delay Rate",
        xaxis_title="Carrier",
        yaxis_title="Delay Rate"
    )
    return fig

def plot_feature_importance(importances):
    """Plot feature importance"""
    fig = px.bar(
        importances,
        x='Importance',
        y='Feature',
        orientation='h',
        title="Feature Importance for Delay Prediction",
        color='Importance',
        color_continuous_scale='Viridis'
    )
    return fig

def plot_risk_gauge(risk_proba):
    """Create risk gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_proba * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Delay Risk Score"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgreen"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    return fig

def plot_vehicle_availability(vehicles):
    """Plot available vehicles by location"""
    available = vehicles[vehicles['Status'] == 'Available'].groupby('Current_Location').size()
    fig = px.bar(
        x=available.index,
        y=available.values,
        labels={'x': 'Location', 'y': 'Available Vehicles'},
        title="Available Vehicles by Location",
        color=available.values,
        color_continuous_scale='Greens'
    )
    return fig
