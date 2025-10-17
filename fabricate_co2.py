import pandas as pd
import numpy as np
import datetime

def generate_fabricated_co2_data():
    """
    Generates a CSV file with fabricated hourly CO2 data for Delhi,
    based on annual estimates and simulated realistic patterns.
    """
    print("Starting data generation...")

    # --- 1. Define Time Range ---
    # As specified by your AQI data.
    start_date = "2020-11-25 01:00:00"
    # FIX: Corrected the typo in the end_date string to a valid format.
    end_date = "2023-01-24 08:00:00"

    # Create a DataFrame with an hourly frequency
    hourly_index = pd.date_range(start=start_date, end=end_date, freq='H')
    df = pd.DataFrame(index=hourly_index)
    df.index.name = 'date'

    # --- 2. Annual CO2 Emission Estimates (in Megatonnes CO2e) ---
    # Based on the trend from your chart, extrapolated for missing years.
    annual_emissions_mt = {
        2020: 22.8, # Estimated based on trend
        2021: 23.8, # Estimated based on trend
        2022: 24.5, # Estimated based on trend
        2023: 25.2  # Estimated based on trend
    }

    # Convert Megatonnes per year to an average Tonnes per hour
    # 1 Mt = 1,000,000 tonnes. 1 year = 8766 hours (avg)
    avg_hourly_emissions_tonnes = {
        year: (mt * 1_000_000) / 8766
        for year, mt in annual_emissions_mt.items()
    }

    # --- 3. Simulate Realistic Patterns (Multiplicative Approach) ---
    # We will create multipliers to mimic real-world activity.

    total_hours = len(df)

    # REALISM UPGRADE: Seasonal Cycle (Higher in winter)
    # Using cosine so that the peak is in winter (start of the year).
    day_of_year = df.index.dayofyear
    seasonal_multiplier = 1 + 0.20 * np.cos(2 * np.pi * (day_of_year - 15) / 365.25) # Peak around Jan 15

    # REALISM UPGRADE: Weekly Cycle (Lower on weekends)
    # Directly reduce emissions on weekends instead of using a sine wave.
    dayofweek = df.index.dayofweek
    # Create a multiplier: 1.05 for weekdays, 0.90 for Sat, 0.80 for Sun
    weekly_multiplier = np.full(total_hours, 1.05)
    weekly_multiplier[dayofweek == 5] = 0.90 # Saturday
    weekly_multiplier[dayofweek == 6] = 0.80 # Sunday

    # REALISM UPGRADE: Daily Cycle (Morning and evening peaks)
    # Simulate a bimodal pattern for rush hours instead of a single peak.
    hour_of_day = df.index.hour
    morning_peak = np.exp(-((hour_of_day - 8)**2) / (2 * 3**2))  # Peak at 8 AM
    evening_peak = np.exp(-((hour_of_day - 18)**2) / (2 * 4**2)) # Peak at 6 PM
    # Combine and normalize to create a multiplier that raises/lowers the base
    daily_base = 0.7 # Night-time dip
    daily_range = 0.5 # Total range of fluctuation
    daily_multiplier = daily_base + daily_range * (morning_peak + evening_peak) / np.max(morning_peak + evening_peak)

    # --- 4. Combine Patterns to Fabricate Data ---
    print("Calculating hourly CO2 values...")

    # Get the base emission for each hour from the annual average
    base_co2 = df.index.year.map(avg_hourly_emissions_tonnes)

    # Add some random noise as a multiplier for more realism
    random_noise_multiplier = np.random.normal(1.0, 0.05, total_hours)

    # REALISM UPGRADE: Combine everything using multiplication for a more realistic interaction
    df['co2_tonnes'] = base_co2 * seasonal_multiplier * weekly_multiplier * daily_multiplier * random_noise_multiplier

    # Ensure no negative emissions, which are physically impossible
    df['co2_tonnes'] = df['co2_tonnes'].clip(lower=0)


    # --- 5. Save the Final Dataset ---
    # The placeholder columns and reordering steps have been removed as requested.

    # Save to CSV
    output_filename = 'Data/co2_hourly.csv'
    df.to_csv(output_filename)

    print("-" * 50)
    print(f"Successfully generated dataset!")
    print(f"File saved as: {output_filename}")
    print(f"Total hours generated: {total_hours}")
    print("\nSample of the generated data:")
    print(df.head())
    print("\nData summary:")
    print(df['co2_tonnes'].describe())
    print("-" * 50)


if __name__ == '__main__':
    generate_fabricated_co2_data()

