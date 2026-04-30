import streamlit as st
import plotly.express as px
import pandas as pd
from modules.processor import process_data
from datetime import datetime, timedelta
import os
import sys

# Configuration constants
PRIMARY_COLOR = "#1E3A8A"
SECONDARY_COLOR = "#0EA5E9"
ACCENT_COLOR = "#F59E0B"
SUCCESS_COLOR = "#10B981"
DANGER_COLOR = "#EF4444"
BACKGROUND_COLOR = "#0F172A"
CARD_BG = "#1E293B"
TEXT_PRIMARY = "#F1F5F9"
TEXT_SECONDARY = "#CBD5E1"

# Append project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set page configurations
st.set_page_config(
    page_title="FitSync - Trends & Insights",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📈"
)

# Inject custom CSS
st.markdown(f"""
    <style>
        body {{
            font-family: 'Sans-serif';
            background-color: {BACKGROUND_COLOR};
        }}
        .stButton>button {{
            background-color: {PRIMARY_COLOR};
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 0.6rem;
        }}
        .stButton>button:hover {{
            background-color: {SECONDARY_COLOR};
            transition: background-color 0.3s;
        }}
        .stMetric {{
            border: 1px solid {SECONDARY_COLOR};
            padding: 1rem;
            border-radius: 10px;
        }}
    </style>
    """, unsafe_allow_html=True)

# Main title
st.title("Trends & Insights 📈")
st.markdown("*Analyzing your fitness journey*", unsafe_allow_html=True)
st.divider()

# Sidebar filters
with st.sidebar:
    st.markdown("### ⚙️ Filters")
    st.divider()
    time_range = st.selectbox(
        "Select Time Range",
        options=["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
        index=1
    )

# Load and process data
df = process_data()

# Apply time range filter
if time_range == "Last 7 days":
    filtered_df = df.tail(7)
elif time_range == "Last 30 days":
    filtered_df = df.tail(30)
elif time_range == "Last 90 days":
    filtered_df = df.tail(90)
else:
    filtered_df = df

# Ensure we have data
if len(filtered_df) == 0:
    st.warning("⚠️ No data available for the selected time range.")
    filtered_df = df

# Summary Statistics
st.markdown("### 📊 Summary Statistics")
st.dataframe(filtered_df[['recovery_score', 'sleep_hours', 'steps', 'calories_burned']].describe(), height=200)
st.divider()

# Enhanced Interactive Graphs
st.markdown("### 📈 Data Visualizations")

# Create a 2x2 grid for better layout
chart_row1_col1, chart_row1_col2 = st.columns(2)
chart_row2_col1, chart_row2_col2 = st.columns(2)

with chart_row1_col1:
    # Average Recovery Score Month-wise
    filtered_df['date'] = pd.to_datetime(filtered_df['date'])
    filtered_df['month'] = filtered_df['date'].dt.to_period('M')
    monthly_avg_recovery = filtered_df.groupby('month')['recovery_score'].mean().reset_index()
    monthly_avg_recovery['month'] = monthly_avg_recovery['month'].astype(str)
    fig1 = px.line(monthly_avg_recovery, x='month', y='recovery_score', title="Average Recovery Score Month-wise")
    fig1.update_traces(line_color=SECONDARY_COLOR, marker_size=8)
    fig1.update_layout(template='plotly_dark', plot_bgcolor='rgba(30, 41, 59, 0.5)', paper_bgcolor='rgba(15, 23, 42, 0.3)', hovermode='x unified', title_font_size=18, font=dict(family='Segoe UI', color=TEXT_PRIMARY))
    st.plotly_chart(fig1, use_container_width=True)

with chart_row1_col2:
    # Distribution of Metrics
    fig2 = px.histogram(filtered_df.melt(value_vars=['steps', 'calories_burned', 'recovery_score', 'sleep_hours']), x='value', color='variable', facet_col='variable', title="Metric Distributions", facet_col_wrap=2)
    fig2.update_layout(template='plotly_dark', plot_bgcolor='rgba(30, 41, 59, 0.5)', paper_bgcolor='rgba(15, 23, 42, 0.3)', title_font_size=18, font=dict(family='Segoe UI', color=TEXT_PRIMARY), showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# Downloadable CSV
data_csv = filtered_df.to_csv(index=False)
st.sidebar.download_button("Download CSV", data_csv, "trends_data.csv", "text/csv")

# Footer
st.divider()
st.markdown("Empower your health journey with insights | FitSync © 2025", unsafe_allow_html=True)
