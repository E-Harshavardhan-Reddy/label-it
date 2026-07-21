"""
Professional data visualization components using Plotly
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

# Professional color palette
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#10B981',
    'warning': '#F59E0B',
    'error': '#EF4444',
    'info': '#3B82F6',
    'neutral': '#64748B'
}

def create_stats_chart(stats_data):
    """Create professional statistics overview chart"""
    if not stats_data:
        return None
    
    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Images Uploaded', 'Labels Added', 'Active Users', 'Languages Used'),
        specs=[[{"type": "indicator"}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}]]
    )
    
    # Add indicators
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=stats_data.get('total_images', 0),
        delta={'reference': stats_data.get('prev_images', 0)},
        title={"text": "Total Images"},
        number={'font': {'color': COLORS['primary'], 'size': 40}},
        domain={'row': 0, 'column': 0}
    ), row=1, col=1)
    
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=stats_data.get('total_labels', 0),
        delta={'reference': stats_data.get('prev_labels', 0)},
        title={"text": "Total Labels"},
        number={'font': {'color': COLORS['success'], 'size': 40}},
        domain={'row': 0, 'column': 1}
    ), row=1, col=2)
    
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=stats_data.get('total_users', 0),
        delta={'reference': stats_data.get('prev_users', 0)},
        title={"text": "Active Users"},
        number={'font': {'color': COLORS['info'], 'size': 40}},
        domain={'row': 1, 'column': 0}
    ), row=2, col=1)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=stats_data.get('languages_used', 0),
        title={"text": "Languages"},
        number={'font': {'color': COLORS['secondary'], 'size': 40}},
        domain={'row': 1, 'column': 1}
    ), row=2, col=2)
    
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter, sans-serif'},
        title={
            'text': '📊 Platform Statistics',
            'x': 0.5,
            'font': {'size': 24, 'color': COLORS['primary']}
        }
    )
    
    return fig

def create_category_distribution(category_data):
    """Create category distribution donut chart"""
    if not category_data:
        return None
    
    df = pd.DataFrame(list(category_data.items()), columns=['Category', 'Count'])
    
    fig = px.pie(
        df, 
        values='Count', 
        names='Category',
        title='📂 Images by Category',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter, sans-serif'},
        title={'font': {'size': 20, 'color': COLORS['primary']}}
    )
    
    return fig

def create_language_usage_chart(language_data):
    """Create language usage bar chart"""
    if not language_data:
        return None
    
    df = pd.DataFrame(list(language_data.items()), columns=['Language', 'Count'])
    df = df.sort_values('Count', ascending=True)
    
    fig = px.bar(
        df,
        x='Count',
        y='Language',
        orientation='h',
        title='🌐 Labels by Language',
        color='Count',
        color_continuous_scale=['#E2E8F0', COLORS['primary']],
        text='Count'
    )
    
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Labels: %{x}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter, sans-serif'},
        title={'font': {'size': 20, 'color': COLORS['primary']}},
        xaxis={'title': 'Number of Labels'},
        yaxis={'title': 'Language'},
        coloraxis_showscale=False
    )
    
    return fig

def create_activity_timeline(activity_data):
    """Create activity timeline chart"""
    if not activity_data:
        return None
    
    df = pd.DataFrame(activity_data)
    if df.empty:
        return None
    
    df['date'] = pd.to_datetime(df['date'])
    
    fig = px.line(
        df,
        x='date',
        y='uploads',
        title='📈 Upload Activity Timeline',
        markers=True,
        line_shape='spline',
        color_discrete_sequence=[COLORS['primary']]
    )
    
    fig.update_traces(
        hovertemplate='<b>Date:</b> %{x}<br><b>Uploads:</b> %{y}<extra></extra>',
        line={'width': 3}
    )
    
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter, sans-serif'},
        title={'font': {'size': 20, 'color': COLORS['primary']}},
        xaxis={'title': 'Date', 'gridcolor': '#E2E8F0'},
        yaxis={'title': 'Number of Uploads', 'gridcolor': '#E2E8F0'}
    )
    
    return fig

def create_user_contribution_chart(user_data):
    """Create user contribution chart"""
    if not user_data:
        return None
    
    df = pd.DataFrame(user_data)
    if df.empty:
        return None
    
    # Take top 10 contributors
    df = df.nlargest(10, 'contributions')
    
    fig = px.bar(
        df,
        x='username',
        y='contributions',
        title='👥 Top Contributors',
        color='contributions',
        color_continuous_scale=['#E2E8F0', COLORS['success']],
        text='contributions'
    )
    
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Contributions: %{y}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter, sans-serif'},
        title={'font': {'size': 20, 'color': COLORS['primary']}},
        xaxis={'title': 'User', 'tickangle': 45},
        yaxis={'title': 'Contributions'},
        coloraxis_showscale=False
    )
    
    return fig

def create_location_map(location_data):
    """Create location distribution map"""
    if not location_data:
        return None
    
    df = pd.DataFrame(location_data)
    if df.empty or 'latitude' not in df.columns or 'longitude' not in df.columns:
        return None
    
    fig = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        hover_name='title',
        hover_data=['category', 'uploaded_by'],
        color='category',
        size_max=15,
        zoom=2,
        height=400,
        title='🗺️ Image Locations'
    )
    
    fig.update_layout(
        mapbox_style='open-street-map',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter, sans-serif'},
        title={'font': {'size': 20, 'color': COLORS['primary']}}
    )
    
    return fig

def create_progress_chart(current, target, title):
    """Create progress indicator chart"""
    progress = min(current / target * 100, 100) if target > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current,
        delta={'reference': target},
        title={'text': title},
        gauge={
            'axis': {'range': [None, target]},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, target * 0.5], 'color': '#E2E8F0'},
                {'range': [target * 0.5, target * 0.8], 'color': '#CBD5E1'},
                {'range': [target * 0.8, target], 'color': '#94A3B8'}
            ],
            'threshold': {
                'line': {'color': COLORS['success'], 'width': 4},
                'thickness': 0.75,
                'value': target
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter, sans-serif', 'color': COLORS['primary']}
    )
    
    return fig
