import pandas as pd
import numpy as np
import os

# --- Configuration based on the provided text ---
START_YEAR = 2024
END_YEAR = 2034

# Initial values for the year 2024 (annual averages)
INITIAL_VALUES = {
    'CO2_Mt': 42.0,
    'PM2.5_ug_m3': 104.7,
    'PM10_ug_m3': 261.8,
    'CO_ppb': 1200.0,
    'NO_ppb': 58.0
}

# Annual trends
ANNUAL_TRENDS = {
    'CO2_percent_change': 0.0075,
    'PM2.5_absolute_change': -1.2,
    'PM10_absolute_change': -2.1,
    'CO_percent_change': -0.005,
    'NO_percent_change': -0.008
}

# Seasonal baselines for PM2.5 and PM10 (monthly multipliers)
SEASONAL_BASELINES = {
    'PM2.5': {1: 142.4, 2: 142.4, 3: 81.2, 4: 81.2, 5: 81.2, 6: 64.8, 7: 64.8, 8: 64.8, 9: 64.8, 10: 144.3, 11: 144.3, 12: 142.4},
    'PM10': {1: 273.1, 2: 273.1, 3: 187.5, 4: 187.5, 5: 187.5, 6: 138.1, 7: 138.1, 8: 138.1, 9: 138.1, 10: 261.8, 11: 261.8, 12: 273.1}
}

# Specific seasonal trends (additive per year after 2024)
SEASONAL_ADJUSTMENTS = {
    'PM2.5': {'Post-monsoon': 0.8, 'Winter': -2.8},
    'PM10': {'Monsoon': -1.6, 'Post-monsoon': 1.0}
}

def generate_annual_projections(start_year, end_year):
    """Generates the annual average pollutant projections in memory."""
    years = list(range(start_year, end_year + 1))
    data = []
    current_values = INITIAL_VALUES.copy()
    
    for year in years:
        row = {'Year': year, **current_values}
        data.append(row)
        
        # Update values for the next year based on trends
        current_values['CO2_Mt'] *= (1 + ANNUAL_TRENDS['CO2_percent_change'])
        current_values['PM2.5_ug_m3'] += ANNUAL_TRENDS['PM2.5_absolute_change']
        current_values['PM10_ug_m3'] += ANNUAL_TRENDS['PM10_absolute_change']
        current_values['CO_ppb'] *= (1 + ANNUAL_TRENDS['CO_percent_change'])
        current_values['NO_ppb'] *= (1 + ANNUAL_TRENDS['NO_percent_change'])
        
    return pd.DataFrame(data).set_index('Year')

def generate_hourly_projections(annual_df):
    """Generates hour-by-hour data using annual, seasonal, and diurnal patterns."""
    start_year = annual_df.index.min()
    end_year = annual_df.index.max()
    
    # Create an hourly datetime index for the entire period
    dates = pd.date_range(start=f'{start_year}-01-01 00:00:00', end=f'{end_year}-12-31 23:00:00', freq='H')
    df = pd.DataFrame(index=dates)
    df.index.name = 'DateTime'
    
    # Map attributes from the index
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df['Hour'] = df.index.hour

    # --- Add Diurnal (Daily) Pattern ---
    # Create a simple sinusoidal pattern for the 24-hour cycle.
    # Peaks in the morning (traffic), dips midday (atmosphere mixing), rises in evening.
    hourly_multiplier = (1.2 + 0.3 * np.sin(2 * np.pi * (df['Hour'] - 8) / 24)) / 1.2
    
    # --- Map Month to Season ---
    def get_season(month):
        if month in [3, 4, 5]: return 'Summer'
        if month in [6, 7, 8, 9]: return 'Monsoon'
        if month in [10, 11]: return 'Post-monsoon'
        return 'Winter'
    df['Season'] = df['Month'].apply(get_season)

    # --- Generate Pollutant Data ---
    # Generic seasonal multipliers for pollutants without specific data
    generic_seasonal_multipliers = {'Winter': 1.3, 'Post-monsoon': 1.15, 'Summer': 0.9, 'Monsoon': 0.65}

    pollutants = {
        'CO2_Mt': 'generic', 'PM2.5_ug_m3': 'specific', 'PM10_ug_m3': 'specific',
        'CO_ppb': 'generic', 'NO_ppb': 'generic'
    }

    print("Generating hourly data for each pollutant...")
    for col_name, p_type in pollutants.items():
        # Get the interpolated annual average for each hour
        annual_avg = df['Year'].map(annual_df[col_name])
        
        # Apply seasonal multiplier
        if p_type == 'specific':
            pollutant_key = col_name.split('_')[0]
            base_annual_avg = np.mean(list(SEASONAL_BASELINES[pollutant_key].values()))
            scaling_factor = annual_avg / base_annual_avg
            seasonal_val = df['Month'].map(SEASONAL_BASELINES[pollutant_key]) * scaling_factor
            
            # Apply specific year-over-year seasonal adjustments
            years_passed = df['Year'] - start_year
            for season, adjustment in SEASONAL_ADJUSTMENTS.get(pollutant_key, {}).items():
                mask = (df['Season'] == season) & (years_passed > 0)
                seasonal_val.loc[mask] += adjustment * years_passed[mask]
        else:
            seasonal_multiplier = df['Season'].map(generic_seasonal_multipliers)
            seasonal_val = annual_avg * seasonal_multiplier

        # Apply the diurnal (hourly) pattern
        df[col_name] = seasonal_val * hourly_multiplier
    
    # --- Add Realistic Noise ---
    print("Adding random noise for realism...")
    for col in pollutants.keys():
        noise = np.random.normal(0, df[col].std() * 0.05, size=len(df))
        df[col] += noise
        df[col] = df[col].clip(0)

    return df.drop(columns=['Year', 'Month', 'Hour', 'Season'])

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Generate annual projections to guide the hourly model
    annual_projections = generate_annual_projections(START_YEAR, END_YEAR)
    
    # 2. Generate the detailed hourly projections
    hourly_projections = generate_hourly_projections(annual_projections)

    # 3. Define the output directory and create it if it doesn't exist
    output_dir = 'Data'
    os.makedirs(output_dir, exist_ok=True)

    # 4. Define the full file path for the hourly data
    output_file_path = os.path.join(output_dir, 'hourly_pollutant_projections_2024-2034.csv')

    # 5. Write the hourly dataframe to a CSV file
    print(f"\nWriting hourly data to '{output_file_path}'...")
    hourly_projections.to_csv(output_file_path, float_format='%.3f')

    print(f"✅ Successfully wrote hourly data for {len(hourly_projections)} records.")
    print("\nSample of the generated data:")
    print(hourly_projections.head())

