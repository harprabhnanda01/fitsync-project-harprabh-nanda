import streamlit as st
from modules.theme import toggle_dark_mode, get_theme_css

# Set page configurations
st.set_page_config(layout="wide", page_title="FitSync - Home")

dark_mode = toggle_dark_mode()
st.markdown(get_theme_css(dark_mode), unsafe_allow_html=True)

# Main title
st.title("FitSync - Personal Health Analytics 🎉")

# Welcome message
st.markdown("""
Welcome to **FitSync**, your personal health analytics dashboard!

## 📊 Features

Navigate using the sidebar to explore:

- **Dashboard** - View your key performance metrics and interactive visualizations
- **Trends & Insights** - Analyze monthly trends and metric distributions

## 🎯 What You'll See

Track your health metrics including:
- 📍 Daily Steps
- 😴 Sleep Hours
- ❤️ Heart Rate
- 🔥 Calories Burned
- 💪 Recovery Score

Start exploring by selecting a page from the sidebar!
""")

# Add some styling
st.markdown("---")
st.markdown("*Empower your health journey with data-driven insights.*")