"""
Recommendation engine module
"""

def recommend_interventions(order_data, risk_score, vehicles, warehouse):
    """Generate intelligent recommendations based on risk"""
    recommendations = []
    
    if risk_score > 0.7:
        recommendations.append(" HIGH RISK: Immediate intervention required")
        recommendations.append(" Assign fastest available vehicle (Express delivery)")
        recommendations.append(" Route via nearest warehouse to reduce distance")
        recommendations.append(" Notify customer proactively about potential delays")
        recommendations.append(" Activate real-time tracking and monitoring")
        
    elif risk_score > 0.4:
        recommendations.append(" MODERATE RISK: Preventive action suggested")
        recommendations.append(" Consider alternate route with less traffic")
        recommendations.append(" Ensure vehicle capacity matches order requirements")
        recommendations.append(" Pre-check warehouse inventory availability")
        
    else:
        recommendations.append(" LOW RISK: Proceed with standard operations")
        recommendations.append(" Monitor for any weather or traffic updates")
    
    # Vehicle recommendations
    available_vehicles = vehicles[vehicles['Status'] == 'Available']
    if len(available_vehicles) > 0:
        best_vehicles = available_vehicles.nsmallest(3, 'CO2_Emissions_Kg_per_KM')
        vehicle_ids = ', '.join(best_vehicles['Vehicle_ID'].values)
        recommendations.append(f" Recommended Vehicles: {vehicle_ids}")
    
    # Warehouse recommendations
    if hasattr(order_data, 'Product_Category'):
        product_cat = order_data['Product_Category']
        warehouse_stock = warehouse[warehouse['Product_Category'] == product_cat]
        if len(warehouse_stock) > 0:
            best_warehouse = warehouse_stock.nsmallest(1, 'Storage_Cost_per_Unit')
            if len(best_warehouse) > 0:
                wh_location = best_warehouse.iloc[0]['Location']
                recommendations.append(f" Recommended Warehouse: {wh_location}")
    
    return recommendations

def get_alternate_routes(order_data, routes_df):
    """Suggest alternate routes"""
    # This is a simplified version - can be enhanced with actual routing logic
    origin = order_data.get('Origin', '')
    destination = order_data.get('Destination', '')
    
    similar_routes = routes_df[
        (routes_df['Route'].str.contains(origin, na=False)) |
        (routes_df['Route'].str.contains(destination, na=False))
    ]
    
    return similar_routes.nsmallest(3, 'Total_Cost') if len(similar_routes) > 0 else None
