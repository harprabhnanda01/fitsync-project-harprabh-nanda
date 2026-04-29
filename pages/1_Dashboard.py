import streamlit as st
import plotly.express as px
import sys
import os
from datetime import datetime
import pandas as pd  # Ensure pandas is imported

# Append the project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.processor import process_data

# Set page configurations
st.set_page_config(layout="wide", page_title="FitSync - Dashboard")

# Main title and logo (if applicable)
# st.image("path/to/logo.png", width=200)  # Include this if you have a logo
st.title("FitSync - Personal Health Analytics 🎉")

# Sidebar filters and styling
st.sidebar.header("Filters ⚙️")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 days", "Last 30 days", "All time"],
    index=2
)

# Add a date range filter
date_range = st.sidebar.date_input("Select Date Range", [datetime.now()])

# Load and process the data
df = process_data()
# Filter the DataFrame based on time range
if time_range == "Last 7 days":
    filtered_df = df.tail(7)
elif time_range == "Last 30 days":
    filtered_df = df.tail(30)
else:
    filtered_df = df  # "All time" uses the full DataFrame

# Ensure date_range covers start and end dates correctly
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['date'] >= pd.to_datetime(date_range[0])) &
        (filtered_df['date'] <= pd.to_datetime(date_range[1]))
    ]
else:
    st.warning("Please select both start and end dates for filtering.")

# Metrics
st.subheader("Key Performance Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    avg_steps = filtered_df['steps'].mean()
    st.metric(label="Average Steps 📊", value=f"{avg_steps:.0f}")

with col2:
    avg_sleep_hours = filtered_df['sleep_hours'].mean()
    st.metric(label="Average Sleep Hours 🌙", value=f"{avg_sleep_hours:.1f}")

with col3:
    avg_recovery_score = filtered_df['recovery_score'].mean()
    st.metric(label="Average Recovery Score 💪", value=f"{avg_recovery_score:.1f}")

# Enhanced Interactive Graphs
st.markdown("### Visual Insights")
col1, col2 = st.columns(2)

with col1:
    dual_chart = px.line(
    filtered_df,
    x='date',
        y=['recovery_score', 'sleep_hours'],
        labels={'value': 'Scores', 'variable': 'Metrics'},
        title="Recovery Score & Sleep Trend"
)
    st.plotly_chart(dual_chart, use_container_width=True)

with col2:
    scatter_plot = px.scatter(
        filtered_df,
        x='steps',
        y='recovery_score',
        color='sleep_hours',
        labels={'color': 'Sleep Hours'},
        title="Recovery Score vs Daily Steps"
    )
    st.plotly_chart(scatter_plot, use_container_width=True)

# Option to download filtered data
csv = filtered_df.to_csv(index=False)
st.sidebar.markdown("### Download Data")
st.sidebar.download_button(label="📥 Download Filtered Data CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')
st.markdown("---")
st.markdown("*Empower your health journey with data-driven insights.*")

