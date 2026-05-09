# =========================
# CHARTS & VISUALIZATIONS
# =========================
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
from utils.recommendations import MealAnalysis


def create_macro_distribution_pie(meal: MealAnalysis) -> go.Figure:
    """Create pie chart for macronutrient distribution.
    
    Args:
        meal: Meal analysis
        
    Returns:
        Plotly figure
    """
    macros = meal.get_macro_ratios()
    
    labels = ['Protein', 'Fat', 'Carbs']
    values = [macros['protein'], macros['fat'], macros['carbs']]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#1a1a1a', width=2)),
        textposition='auto',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>',
    )])
    
    fig.update_layout(
        title='Macronutrient Distribution',
        font=dict(size=12, family="Arial, sans-serif", color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig


def create_nutrition_bars(meal: MealAnalysis) -> go.Figure:
    """Create bar chart for nutrition breakdown.
    
    Args:
        meal: Meal analysis
        
    Returns:
        Plotly figure
    """
    nutrients = ['Protein', 'Fat', 'Carbs', 'Sugar', 'Fiber', 'Sodium']
    values = [
        meal.total_protein,
        meal.total_fat,
        meal.total_carbs,
        meal.total_sugar,
        meal.total_fiber,
        meal.total_sodium / 10  # Scale down for visibility
    ]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#F7DC6F', '#BB8FCE', '#F8B88B']
    
    fig = go.Figure(data=[
        go.Bar(
            x=nutrients,
            y=values,
            marker=dict(color=colors, line=dict(color='white', width=1.5)),
            text=[f'{v:.1f}' for v in values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>%{y:.1f}g<extra></extra>',
        )
    ])
    
    fig.update_layout(
        title='Nutrition Breakdown by Nutrient',
        yaxis_title='Amount (g)',
        font=dict(size=11, family="Arial, sans-serif", color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        height=400,
        margin=dict(l=50, r=20, t=50, b=50),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.2)')
    )
    
    return fig


def create_calorie_gauge(current_calories: float, daily_goal: float) -> go.Figure:
    """Create gauge chart for calorie intake.
    
    Args:
        current_calories: Current meal calories
        daily_goal: Daily calorie goal
        
    Returns:
        Plotly figure
    """
    percentage = (current_calories / daily_goal) * 100
    
    # Determine color
    if percentage < 50:
        color = 'green'
    elif percentage < 100:
        color = 'orange'
    else:
        color = 'red'
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=percentage,
        title={'text': "Daily Calorie % of Goal"},
        delta={'reference': 100},
        gauge={
            'axis': {'range': [0, 150]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': 'rgba(144, 238, 144, 0.3)'},
                {'range': [50, 100], 'color': 'rgba(255, 165, 0, 0.3)'},
                {'range': [100, 150], 'color': 'rgba(255, 99, 71, 0.3)'}
            ],
            'threshold': {
                'line': {'color': 'white', 'width': 2},
                'thickness': 0.75,
                'value': 100
            }
        },
        number={'suffix': '%', 'font': {'size': 24}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        font=dict(size=12, family="Arial, sans-serif", color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig


def create_health_indicators(evaluation: Dict) -> go.Figure:
    """Create horizontal bar chart for health indicators.
    
    Args:
        evaluation: Health evaluation dictionary
        
    Returns:
        Plotly figure
    """
    indicators = [
        'Calories',
        'Fat',
        'Protein',
        'Sodium',
        'Sugar',
        'Fiber'
    ]
    
    status_map = {
        'Light meal': 2,
        'Moderate meal': 3,
        'Heavy meal': 4,
        'Very heavy meal': 5,
        'Low fat': 2,
        'Moderate fat': 3,
        'High fat': 4,
        'Very high fat ⚠️': 5,
        'Low protein': 2,
        'Moderate protein': 3,
        'High protein': 4,
        'Very high protein': 5,
        'Low sodium': 2,
        'Moderate sodium': 3,
        'High sodium': 4,
        'Very high sodium ⚠️': 5,
        'Low sugar': 2,
        'Moderate sugar': 3,
        'High sugar': 4,
        'Very high sugar ⚠️': 5,
        'Low fiber': 2,
        'Moderate fiber': 3,
        'Good fiber': 4,
    }
    
    values = [
        status_map.get(evaluation.get('calorie_status', 'Moderate'), 3),
        status_map.get(evaluation.get('fat_status', 'Moderate fat'), 3),
        status_map.get(evaluation.get('protein_status', 'Moderate protein'), 3),
        status_map.get(evaluation.get('sodium_status', 'Moderate sodium'), 3),
        status_map.get(evaluation.get('sugar_status', 'Moderate sugar'), 3),
        status_map.get(evaluation.get('fiber_status', 'Moderate fiber'), 3),
    ]
    
    colors = ['#FF6B6B' if v >= 4 else '#F7DC6F' if v == 3 else '#90EE90' for v in values]
    
    fig = go.Figure(data=[
        go.Bar(
            y=indicators,
            x=values,
            orientation='h',
            marker=dict(color=colors, line=dict(color='white', width=1.5)),
            text=['Best' if v == 2 else 'Good' if v == 3 else 'Caution' if v == 4 else 'Alert' for v in values],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Level: %{text}<extra></extra>',
        )
    ])
    
    fig.update_layout(
        title='Health Indicators Summary',
        xaxis_title='Health Level',
        font=dict(size=11, family="Arial, sans-serif", color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[0, 6], showgrid=False),
        yaxis=dict(showgrid=False),
        height=350,
        margin=dict(l=100, r=20, t=50, b=20),
        showlegend=False
    )
    
    return fig


def create_food_items_bar(food_items: List[Dict]) -> go.Figure:
    """Create bar chart showing detected food items and calories.
    
    Args:
        food_items: List of detected food items with calories
        
    Returns:
        Plotly figure
    """
    if not food_items:
        fig = go.Figure()
        fig.add_annotation(text="No food items detected")
        return fig
    
    foods = [item['food'].title() for item in food_items]
    calories = [item['calories'] for item in food_items]
    confidence = [item['confidence'] for item in food_items]
    
    fig = go.Figure(data=[
        go.Bar(
            x=foods,
            y=calories,
            marker=dict(
                color=calories,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='Calories', ticksuffix=' kcal'),
                line=dict(color='white', width=1.5)
            ),
            text=[f'{c} kcal' for c in calories],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Calories: %{y}<extra></extra>',
        )
    ])
    
    fig.update_layout(
        title='Detected Foods and Their Calories',
        yaxis_title='Calories (kcal)',
        font=dict(size=11, family="Arial, sans-serif", color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.2)'),
        height=400,
        margin=dict(l=60, r=20, t=50, b=60),
        hovermode='x',
        xaxis_tickangle=-45
    )
    
    return fig
