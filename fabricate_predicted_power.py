import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# --- Configuration ---
START_YEAR = 2025
END_YEAR = 2035
BASELINE_ANNUAL_DEMAND_MW = 4500  # Starting average demand in MW for the start year
MEAN_ANNUAL_GROWTH_RATE = 0.025 # The average annual increase in demand
GROWTH_RATE_VOLATILITY = 0.01 # How much the growth rate can vary each year

# Base monthly seasonal multipliers. These will be varied slightly each year.
SEASONAL_MULTIPLIERS = {
    1: 1.15, 2: 1.05, 3: 1.0, 4: 1.1, 5: 1.25, 6: 1.30,
    7: 1.1, 8: 1.0, 9: 0.95, 10: 1.05, 11: 1.1, 12: 1.20
}

OUTPUT_DIR = 'Data'
PLOT_DIR = 'Plots'
OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, 'fabricated_monthly_power_demand.csv')
OUTPUT_PLOT_PATH = os.path.join(PLOT_DIR, 'fabricated_monthly_power_demand_plot.png')

def generate_fabricated_monthly_power_demand():
    """
    Generates a more realistic, month-wise power demand forecast by incorporating
    variable growth, seasonality, economic cycles, and random shocks.
    """
    print("1. Generating monthly fabricated power demand data from 2025 to 2035...")
    
    dates = pd.date_range(start=f'{START_YEAR}-01-01', end=f'{END_YEAR}-12-31', freq='MS')
    df = pd.DataFrame(index=dates)
    df.index.name = 'Date'
    
    # --- Simulate Variable Annual Growth ---
    annual_demand = {}
    current_demand = BASELINE_ANNUAL_DEMAND_MW
    for year in range(START_YEAR, END_YEAR + 1):
        annual_demand[year] = current_demand
        # The growth rate for the next year is randomized around the mean
        growth_rate = np.random.normal(MEAN_ANNUAL_GROWTH_RATE, GROWTH_RATE_VOLATILITY)
        current_demand *= (1 + growth_rate)

    df['annual_avg'] = df.index.year.map(annual_demand)
    
    # --- Simulate Variable Seasonality and Economic Cycle ---
    num_months = len(df)
    # A slow sine wave to simulate a multi-year economic cycle
    economic_cycle = 1 + 0.04 * np.sin(2 * np.pi * np.arange(num_months) / (12 * 5)) # 5-year cycle
    
    # Apply seasonal multipliers with some randomness each month
    seasonal_effects = [m * np.random.normal(1, 0.03) for m in df.index.month.map(SEASONAL_MULTIPLIERS)]
    
    df['Fabricated_Power_Demand_MW'] = df['annual_avg'] * seasonal_effects * economic_cycle
    
    # --- Add Random Shocks ---
    # Simulate a few unpredictable major events (e.g., extreme heatwave, economic event)
    num_shocks = 3
    shock_indices = np.random.choice(df.index, num_shocks, replace=False)
    for shock_date in shock_indices:
        shock_magnitude = np.random.uniform(0.10, 0.20) # 10-20% shock
        shock_direction = np.random.choice([-1, 1])
        df.loc[shock_date, 'Fabricated_Power_Demand_MW'] *= (1 + shock_magnitude * shock_direction)

    # --- Add Final Layer of Noise ---
    noise = np.random.normal(0, df['Fabricated_Power_Demand_MW'].std() * 0.02, size=len(df))
    df['Fabricated_Power_Demand_MW'] += noise

    print("   - Data generation complete.")
    
    return df[['Fabricated_Power_Demand_MW']]

def plot_fabricated_data(df):
    """
    Generates and saves a plot of the fabricated power demand data.
    """
    print("\n3. Generating and saving plot...")
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(15, 8))

    df['12-Month_Rolling_Average'] = df['Fabricated_Power_Demand_MW'].rolling(window=12, center=True).mean()

    ax.plot(df.index, df['Fabricated_Power_Demand_MW'], label='Monthly Fabricated Demand', color='skyblue', alpha=0.8)
    ax.plot(df.index, df['12-Month_Rolling_Average'], label='12-Month Rolling Average', color='navy', linestyle='--')

    ax.set_title('Fabricated Monthly Power Demand (2025-2035)', fontsize=16)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Fabricated Power Demand (MW)', fontsize=12)
    ax.legend()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    plt.tight_layout()

    os.makedirs(PLOT_DIR, exist_ok=True)
    fig.savefig(OUTPUT_PLOT_PATH)
    print(f"   - Plot saved to '{OUTPUT_PLOT_PATH}'")
    
    plt.show()

# --- Main execution block ---
if __name__ == "__main__":
    # 1. Generate the data
    fabricated_data = generate_fabricated_monthly_power_demand()
    
    # 2. Save the data to a CSV file
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fabricated_data.to_csv(OUTPUT_FILE_PATH, float_format='%.2f')
    
    print(f"\n✅ Successfully saved fabricated monthly power demand to '{OUTPUT_FILE_PATH}'")
    print("\nSample of the generated data:")
    print(fabricated_data.head())
    
    # 3. Plot the generated data
    plot_fabricated_data(fabricated_data)

