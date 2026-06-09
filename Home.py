import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Append the project root directory to PYTHONPATH for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

from modules.processor import process_data
from modules.theme import toggle_dark_mode, get_theme, get_theme_css


def main():
    st.set_page_config(
        layout="wide",
        page_title="FitSync - Home",
        page_icon="🏠",
        initial_sidebar_state="expanded",
    )

    dark_mode = toggle_dark_mode()
    theme = get_theme(dark_mode)
    st.markdown(get_theme_css(dark_mode), unsafe_allow_html=True)

    df = process_data()
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    avg_steps = df['steps'].mean() if 'steps' in df.columns else 0
    avg_sleep = df['sleep_hours'].mean() if 'sleep_hours' in df.columns else 0
    avg_recovery = df['recovery_score'].mean() if 'recovery_score' in df.columns else 0
    avg_calories = df['calories_burned'].mean() if 'calories_burned' in df.columns else 0
    total_days = len(df)

    st.markdown(
        f"""
        <div style='display:flex; flex-wrap:wrap; align-items:center; gap:1.5rem; margin-bottom:2rem;'>
            <div style='flex:1; min-width:300px;'>
                <h1 style='margin:0; font-size:3rem; color:{theme['TEXT_PRIMARY']};'>FitSync</h1>
                <p style='margin:0.75rem 0 0; font-size:1.1rem; line-height:1.6; color:{theme['TEXT_SECONDARY']};'>
                    Your personalized fitness home. Track performance, explore insights, and stay motivated with clear health metrics and a friendly interface.
                </p>
                <div style='margin-top:1.5rem; display:grid; gap:0.75rem; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));'>
                    <div style='padding:1rem; border-radius:18px; background:{theme['CARD_BG']}; border:1px solid {theme['PANEL_BORDER']}; color:{theme['TEXT_PRIMARY']};'>
                        <div style='color:{theme['SECONDARY']}; font-size:0.95rem; margin-bottom:0.5rem;'>Total records</div>
                        <div style='font-size:1.8rem; font-weight:700;'>{total_days}</div>
                    </div>
                    <div style='padding:1rem; border-radius:18px; background:{theme['CARD_BG']}; border:1px solid {theme['PANEL_BORDER']}; color:{theme['TEXT_PRIMARY']};'>
                        <div style='color:{theme['SECONDARY']}; font-size:0.95rem; margin-bottom:0.5rem;'>Average Recovery</div>
                        <div style='font-size:1.8rem; font-weight:700;'>{avg_recovery:.1f}/100</div>
                    </div>
                    <div style='padding:1rem; border-radius:18px; background:{theme['CARD_BG']}; border:1px solid {theme['PANEL_BORDER']}; color:{theme['TEXT_PRIMARY']};'>
                        <div style='color:{theme['SECONDARY']}; font-size:0.95rem; margin-bottom:0.5rem;'>Avg Sleep</div>
                        <div style='font-size:1.8rem; font-weight:700;'>{avg_sleep:.1f}h</div>
                    </div>
                </div>
            </div>
            <div style='flex:0 1 320px; padding:1.5rem; border-radius:24px; background:{theme['CARD_BG']}; border:1px solid {theme['PANEL_BORDER']}; color:{theme['TEXT_PRIMARY']};'>
                <h2 style='margin-top:0; margin-bottom:0.75rem; font-size:1.35rem; color:{theme['SECONDARY']};'>Your FitSync home</h2>
                <p style='margin:0; color:{theme['TEXT_SECONDARY']}; line-height:1.7;'>
                    Use the sidebar to navigate to Dashboard for key metrics and Trends for deeper analytics.
                    This page gives you a polished summary of your progress at a glance.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### 🚀 Quick Overview")
    col1, col2, col3, col4 = st.columns(4, gap='large')
    col1.metric("Average Steps", f"{avg_steps:,.0f}")
    col2.metric("Average Sleep", f"{avg_sleep:.1f}h")
    col3.metric("Average Calories", f"{avg_calories:,.0f}")
    col4.metric("Average Recovery", f"{avg_recovery:.1f}/100")

    st.markdown("### 📅 Recent Activity")
    if 'date' in df.columns:
        recent_df = df.sort_values('date').tail(14).set_index('date')
        chart_df = recent_df[['steps', 'sleep_hours', 'recovery_score']].copy()
        chart_df.columns = ['Steps', 'Sleep Hours', 'Recovery Score']
        st.line_chart(chart_df)
    else:
        st.info("No date field available to render recent activity charts.")

    st.markdown("---")
    st.markdown("### ✨ Home Highlights")
    st.markdown(
        "- **Fast entry point** to Dashboard and Trends pages.\n"
        "- **Clear daily metrics** for steps, sleep, calories, and recovery.\n"
        "- **Modern layout** with better spacing, headings, and summary cards.\n"
        "- **Designed to help you explore your fitness data quickly."
    )

    st.markdown("---")
    st.markdown("*Need a deeper view? Open the sidebar and explore Dashboard or Trends for more detailed analytics.*")


if __name__ == '__main__':
    main()
