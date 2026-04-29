import pandas as pd


def load_data(filepath='data/health_data.csv'):
    """
    Load health data from CSV, clean missing values, and standardize column names.
    """
    df = pd.read_csv(filepath)

    # Remove spaces from column names
    df.columns = df.columns.str.strip()

    # Ensure all columns are correct
    print("Initial dataframe columns:", df.columns)

    # Rename columns to ensure consistent naming
    df.rename(columns={
        'Sleep_Hours': 'Sleep_hours',
        'Heart_Rate_Bpm': 'heart_rate_bpm',
        'Calories_Burned': 'calories_burned',
        'Active_Minutes': 'active_minutes'
    }, inplace=True)

    print("Renamed dataframe columns:", df.columns)  # Debug purpose

    # Change case to prevent case-sensitive errors
    df.columns = df.columns.str.lower()

    # Update column names list again
    column_names = df.columns

    if 'heart_rate_bpm' not in column_names:
        # Assume another form due to changed filenames
        df.rename(columns={'Heart_Rate_bpm': 'heart_rate_bpm'}, inplace=True)

    # Fill missing values
    df['steps'] = df['steps'].fillna(df['steps'].median())
    # Fill missing Sleep_hours with 7.0
    df['sleep_hours'] = df['sleep_hours'].fillna(7.0)

    # Fill missing heart_rate_bpm with 68
    df['heart_rate_bpm'] = df['heart_rate_bpm'].fillna(68)

    for column in df.columns:
        if df[column].isnull().any() and column not in ['date', 'steps', 'sleep_hours', 'heart_rate_bpm']:
            df[column] = df[column].fillna(df[column].median())

    # Convert 'Date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    return df


def calculate_recovery_score(df):
    """
    Calculate Recovery Score
    """

    df['recovery_score'] = 50  # Ensure the column name is lowercase
    if 'sleep_hours' in df.columns:
        df.loc[df['sleep_hours'] >= 7, 'recovery_score'] += 20
        df.loc[df['sleep_hours'] < 6, 'recovery_score'] -= 15





    if 'heart_rate_bpm' in df.columns:


        df.loc[df['heart_rate_bpm'] <= 70, 'recovery_score'] += 10
        df.loc[df['heart_rate_bpm'] > 85, 'recovery_score'] -= 10





    if 'steps' in df.columns:
        df.loc[df['steps'] >= 8000, 'recovery_score'] += 5
        df.loc[df['steps'] < 4000, 'recovery_score'] -= 5
        df.loc[df['steps'] > 14000, 'recovery_score'] -= 5


    df['recovery_score'] = df['recovery_score'].clip(0, 100)

    return df


def process_data():
    df = load_data()
    df = calculate_recovery_score(df)
    return df