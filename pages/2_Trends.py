import streamlit as st
import plotly.express as px
import pandas as pd
from modules.processor import process_data

# Set page configurations
st.set_page_config(layout="wide", page_title="FitSync - Trends & Insights")

# Main title of the page
st.title("Trends and Insights")

# Sidebar filters (same as the Dashboard page)
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 days", "Last 30 days", "All time"],
    index=2
)

# Load and process the data
df = process_data()

# Filter the DataFrame based on time range
if time_range == "Last 7 days":
    filtered_df = df.tail(7)
elif time_range == "Last 30 days":
    filtered_df = df.tail(30)
else:
    filtered_df = df  # "All time" uses the full DataFrame

# Show summary statistics
st.subheader("Summary Statistics")
st.write(filtered_df[['recovery_score', 'sleep_hours', 'steps', 'calories_burned']].describe())

# Line chart: Average Recovery Score month-wise
st.subheader("Average Recovery Score Month-wise")
# Ensure the date is in datetime format and add a `month` column for grouping
filtered_df['date'] = pd.to_datetime(filtered_df['date'])
filtered_df['month'] = filtered_df['date'].dt.to_period('M')

monthly_avg_recovery = filtered_df.groupby('month')['recovery_score'].mean().reset_index()
monthly_avg_recovery['month'] = monthly_avg_recovery['month'].astype(str)  # Convert months back to string for plotting

recovery_month_chart = px.line(
    monthly_avg_recovery,
    x='month',
    y='recovery_score',
    title="Average Recovery Score Month-wise"
)
st.plotly_chart(recovery_month_chart, use_container_width=True)

# Histogram: Distribution of Steps, Calories Burned, Recovery Score, Sleep Hours
st.subheader("Distribution of Steps, Calories Burned, Recovery Score, and Sleep Hours")

fig = px.histogram(
    filtered_df.melt(value_vars=['steps', 'calories_burned', 'recovery_score', 'sleep_hours']),
    x='value',
    color='variable',
    facet_col='variable',
    title="Distribution of Metrics",
    facet_col_wrap=2
)
st.plotly_chart(fig, use_container_width=True)