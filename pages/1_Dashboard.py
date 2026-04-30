import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd  # Ensure pandas is imported
from modules.processor import process_data
from datetime import datetime, timedelta
import os
import sys

# Configuration constants from config.py
PRIMARY_COLOR = "#1E3A8A"
SECONDARY_COLOR = "#0EA5E9"
ACCENT_COLOR = "#F59E0B"
SUCCESS_COLOR = "#10B981"
DANGER_COLOR = "#EF4444"
BACKGROUND_COLOR = "#0F172A"
CARD_BG = "#1E293B"
TEXT_PRIMARY = "#F1F5F9"
TEXT_SECONDARY = "#CBD5E1"

# Append the project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set page configurations
st.set_page_config(
    page_title="FitSync - Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏋️‍♂️"
)

# Inject professional custom CSS
st.markdown(f"""
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        html, body, [data-testid="stAppViewContainer"] {{
            background: linear-gradient(135deg, {BACKGROUND_COLOR} 0%, #1a2a4a 100%);
            color: {TEXT_PRIMARY};
            font-family: 'Segoe UI', 'Roboto', sans-serif;
        }}
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PRIMARY_COLOR} 0%, #0d1f3c 100%);
            border-right: 1px solid {SECONDARY_COLOR};
        }}
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            color: {TEXT_PRIMARY};
        }}
        .stButton>button {{
            background: linear-gradient(90deg, {SECONDARY_COLOR} 0%, {ACCENT_COLOR} 100%);
            color: white;
            font-size: 14px;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            border: none;
            box-shadow: 0 4px 15px rgba(15, 149, 224, 0.3);
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            box-shadow: 0 6px 20px rgba(15, 149, 224, 0.5);
            transform: translateY(-2px);
        }}
        .stButton>button:active {{
            transform: translateY(0);
        }}
        [data-testid="stMetric"] {{
            background: linear-gradient(135deg, {CARD_BG} 0%, rgba(30, 41, 59, 0.8) 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(14, 165, 233, 0.2);
            box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1);
            transition: all 0.3s ease;
        }}
        [data-testid="stMetric"]:hover {{
            border-color: rgba(14, 165, 233, 0.5);
            box-shadow: 0 12px 40px rgba(14, 165, 233, 0.2);
            transform: translateY(-4px);
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 14px;
            color: {TEXT_SECONDARY};
            font-weight: 500;
            margin-bottom: 0.5rem;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 32px;
            color: {SECONDARY_COLOR};
            font-weight: 700;
        }}
        h1, h2, h3 {{
            color: {TEXT_PRIMARY};
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(90deg, {SECONDARY_COLOR}, {ACCENT_COLOR});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        h2 {{
            font-size: 1.8rem;
            margin-bottom: 1.2rem;
            margin-top: 2rem;
            border-bottom: 2px solid {SECONDARY_COLOR};
            padding-bottom: 0.8rem;
        }}
        h3 {{
            font-size: 1.3rem;
            margin-bottom: 1rem;
            color: {ACCENT_COLOR};
        }}
        .stSelectbox, .stDateInput, .stRadio {{
            color: {TEXT_PRIMARY};
        }}
        [data-testid="stSelectbox"] > div > div {{
            background-color: {CARD_BG};
            border: 1px solid rgba(14, 165, 233, 0.3);
            border-radius: 8px;
        }}
        [data-testid="stDateInput"] > div > div {{
            background-color: {CARD_BG};
            border: 1px solid rgba(14, 165, 233, 0.3);
            border-radius: 8px;
        }}
        [data-testid="stRadio"] > div {{
            background-color: transparent;
        }}
        .stPlotlyChart {{
            background: {CARD_BG};
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid rgba(14, 165, 233, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }}
        [data-testid="stMarkdown"] {{
            color: {TEXT_SECONDARY};
        }}
        hr {{
            border-color: rgba(14, 165, 233, 0.2);
            margin: 2rem 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, {CARD_BG} 0%, rgba(30, 41, 59, 0.8) 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(16, 185, 129, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }}
        .info-box {{
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%);
            border-left: 4px solid {SECONDARY_COLOR};
            padding: 1.2rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
    </style>
    """, unsafe_allow_html=True)

# Load and process the data
df = process_data()

# Navigation section
with st.sidebar:
    st.markdown("### 🏋️ Navigation")
    st.divider()
    section = st.radio("Go to", options=["Dashboard", "Profile", "Settings"], index=0, label_visibility="collapsed")

# Main title
st.title("FitSync - Personal Health Analytics 🎉")
st.markdown("*Real-time insights into your health and fitness journey*")
st.divider()

# Sidebar filters
with st.sidebar:
    st.markdown("### ⚙️ Filters & Settings")
    st.divider()
    
    time_range = st.selectbox(
        "Select Time Range",
        options=["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
        index=1
    )
    
    # Apply time range filter
    if time_range == "Last 7 days":
        filtered_df = df.tail(7).copy()
    elif time_range == "Last 30 days":
        filtered_df = df.tail(30).copy()
    elif time_range == "Last 90 days":
        filtered_df = df.tail(90).copy()
    else:
        filtered_df = df.copy()  # "All time" uses the full DataFrame
    
    # Ensure we have data
    if len(filtered_df) == 0:
        st.warning("⚠️ No data available for the selected time range.")
        filtered_df = df.copy()

# Metrics
st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_steps = filtered_df['steps'].mean()
    st.metric(
        label="Average Steps 👟",
        value=f"{avg_steps:,.0f}",
        delta=f"{(avg_steps - filtered_df['steps'].iloc[0] if len(filtered_df) > 0 else 0):,.0f}" if len(filtered_df) > 1 else None
    )

with col2:
    avg_sleep_hours = filtered_df['sleep_hours'].mean()
    st.metric(
        label="Average Sleep 😴",
        value=f"{avg_sleep_hours:.1f}h",
        delta=f"{(avg_sleep_hours - 7.0):+.1f}h vs target" if avg_sleep_hours != 0 else None
    )

with col3:
    avg_heart_rate = filtered_df['heart_rate_bpm'].mean()
    st.metric(
        label="Average Heart Rate ❤️",
        value=f"{avg_heart_rate:.0f} BPM",
        delta="Normal Range" if 60 <= avg_heart_rate <= 100 else "Check Up"
    )

with col4:
    avg_recovery_score = filtered_df['recovery_score'].mean()
    st.metric(
        label="Recovery Score 💪",
        value=f"{avg_recovery_score:.0f}/100",
        delta=f"{'Excellent' if avg_recovery_score > 80 else 'Good' if avg_recovery_score > 60 else 'Needs Work'}"
    )

st.divider()

# Enhanced Interactive Graphs
st.markdown("### 📈 Data Visualizations")

# Create a 2x2 grid for better layout
chart_row1_col1, chart_row1_col2 = st.columns(2)
chart_row2_col1, chart_row2_col2 = st.columns(2)

# Prepare colors for charts
colors_dict = {
    'recovery_score': '#0EA5E9',
    'steps': '#10B981',
    'sleep_hours': '#F59E0B',
    'heart_rate_bpm': '#EF4444'
}

with chart_row1_col1:
    # Recovery Score Trend
    fig1 = px.line(
        filtered_df,
        x='date',
        y='recovery_score',
        title="Recovery Score Trend",
        markers=True,
        line_shape='spline'
    )
    fig1.update_traces(line_color='#0EA5E9', marker_size=8)
    fig1.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(30, 41, 59, 0.5)',
        paper_bgcolor='rgba(15, 23, 42, 0.3)',
        hovermode='x unified',
        title_font_size=18,
        font=dict(family='Segoe UI', color='#E2E8F0'),
    )
    st.plotly_chart(fig1, use_container_width=True)

with chart_row1_col2:
    # Steps Over Time
    fig2 = px.bar(
        filtered_df,
        x='date',
        y='steps',
        title="Daily Steps",
        color='steps',
        color_continuous_scale='Viridis'
    )
    fig2.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(30, 41, 59, 0.5)',
        paper_bgcolor='rgba(15, 23, 42, 0.3)',
        hovermode='x unified',
        title_font_size=18,
        font=dict(family='Segoe UI', color='#E2E8F0'),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

with chart_row2_col1:
    # Sleep Hours vs Recovery Score
    fig3 = px.scatter(
        filtered_df,
        x='sleep_hours',
        y='recovery_score',
        title="Sleep Duration vs Recovery Score",
        color='recovery_score',
        color_continuous_scale='RdYlGn',
        size='steps',
        hover_data=['date']
    )
    fig3.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(30, 41, 59, 0.5)',
        paper_bgcolor='rgba(15, 23, 42, 0.3)',
        hovermode='closest',
        title_font_size=18,
        font=dict(family='Segoe UI', color='#E2E8F0'),
    )
    st.plotly_chart(fig3, use_container_width=True)

with chart_row2_col2:
    # Heart Rate Distribution
    if 'heart_rate_bpm' in filtered_df.columns:
        fig4 = px.histogram(
            filtered_df,
            x='heart_rate_bpm',
            nbins=20,
            title="Heart Rate Distribution",
            color_discrete_sequence=['#EF4444']
        )
        fig4.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(30, 41, 59, 0.5)',
            paper_bgcolor='rgba(15, 23, 42, 0.3)',
            title_font_size=18,
            font=dict(family='Segoe UI', color='#E2E8F0'),
            showlegend=False
        )
        st.plotly_chart(fig4, use_container_width=True)

st.divider()
# Download section
with st.sidebar:
    st.divider()
    st.markdown("### 💾 Export Data")
    
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"fitsync_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    st.divider()
    st.markdown("### ℹ️ Info")
    st.info(f"📅 Records: {len(filtered_df)}\n\n⏱️ Period: {time_range}")

# Footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.markdown("🔗 **Quick Links**\n- Dashboard\n- Trends\n- Profile")
with footer_col2:
    st.markdown("📊 **Data Summary**\n- Total Days Tracked\n- Avg Steps: 8,500+\n- Avg Sleep: 7 hours")
with footer_col3:
    st.markdown("💡 **Tips**\n- Keep steps above 8,000/day\n- Sleep 7-9 hours nightly\n- Monitor heart rate trends")

st.markdown("""
---
<div style='text-align: center; color: #94A3B8;'>
    <p><i>Empower your health journey with data-driven insights | FitSync © 2025</i></p>
</div>
""", unsafe_allow_html=True)

