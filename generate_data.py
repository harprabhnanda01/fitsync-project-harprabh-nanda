import numpy as np
import pandas as pd
from datetime import timedelta, datetime

# Settings for the data generation
start_date = datetime(2025, 1, 1)
days = 365
missing_percentage = 0.05

# Generate dates
dates = [start_date + timedelta(days=i) for i in range(days)]

# Generate data with realistic distributions
steps = np.random.normal(loc=8500, scale=2000, size=days).clip(3000, 18000)
sleep_hours = np.random.normal(loc=7.2, scale=1.0, size=days).clip(4.5, 9.5)
heart_rate_bpm = np.random.normal(loc=68, scale=10, size=days).clip(48, 110)
calories_burned = np.random.uniform(1800, 2400, size=days)
active_minutes = np.random.uniform(20, 180, size=days)

# Introducing missing values
for data in [steps, sleep_hours, heart_rate_bpm, calories_burned, active_minutes]:
    nan_indices = np.random.choice(days, int(missing_percentage * days), replace=False)
    data[nan_indices] = np.nan

# Create DataFrame
fitness_data = pd.DataFrame({
    'date': dates,
    'steps': steps,
    'sleep_hours': sleep_hours,
    'heart_rate_bpm': heart_rate_bpm,
    'calories_burned': calories_burned,
    'active_minutes': active_minutes
})

# Save to CSV
fitness_data.to_csv('data/health_data.csv', index=False)
