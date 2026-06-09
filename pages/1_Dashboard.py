import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd  # Ensure pandas is imported
from datetime import datetime, timedelta
import os
import sys

# Append the project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.processor import process_data
from modules.theme import toggle_dark_mode, get_theme_css

# Configuration constants from config.py
PRIMARY_COLOR = "#1E3A8A"
SECONDARY_COLOR = "#0EA5E9"
ACCENT_COLOR = "#F59E0B"
SUCCESS_COLOR = "#10B981"
DANGER_COLOR = "#EF4444"

# Set page configurations
st.set_page_config(
    page_title="FitSync - Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏋️‍♂️"
)

dark_mode = toggle_dark_mode()
st.markdown(get_theme_css(dark_mode), unsafe_allow_html=True)

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

