#!/usr/bin/env python3
"""
Download NASA POWER Global Horizontal Irradiance (GHI) data for Delhi NCR
Coordinates: 28.7°N, 77.1°E
Date range: 2021-01-01 to 2024-12-31
"""

import requests
import pandas as pd
import os

# Configuration
LATITUDE = 28.7
LONGITUDE = 77.1
START_DATE = "20210101"
END_DATE = "20241231"
OUTPUT_FILE = "Data/ghi_nasa_power.csv"

# NASA POWER API endpoint
API_URL = (
    f"https://power.larc.nasa.gov/api/temporal/daily/point?"
    f"parameters=ALLSKY_SFC_SW_DWN&"
    f"community=RE&"
    f"longitude={LONGITUDE}&"
    f"latitude={LATITUDE}&"
    f"start={START_DATE}&"
    f"end={END_DATE}&"
    f"format=JSON"
)

print("=" * 60)
print("NASA POWER GHI Data Download for Delhi NCR")
print("=" * 60)
print(f"Location: {LATITUDE}°N, {LONGITUDE}°E")
print(f"Date Range: 2021-01-01 to 2024-12-31")
print(f"Parameter: ALLSKY_SFC_SW_DWN (GHI in kWh/m²/day)")
print("=" * 60)

# Create Data directory if it doesn't exist
os.makedirs("Data", exist_ok=True)

# Download data
print("\nDownloading data from NASA POWER API...")
print(f"URL: {API_URL[:80]}...")

try:
    response = requests.get(API_URL, timeout=60)
    response.raise_for_status()
    print("✓ Download successful!")
    
    # Parse JSON response
    data = response.json()
    
    # Extract the parameter data
    ghi_data = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
    
    # Convert to pandas DataFrame
    dates = []
    ghi_values = []
    
    for date_str, ghi_value in ghi_data.items():
        # date_str is in format YYYYMMDD
        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]
        date = f"{year}-{month}-{day}"
        dates.append(date)
        ghi_values.append(ghi_value)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        'ghi_kwh_m2': ghi_values
    })
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n✓ Data saved to: {OUTPUT_FILE}")
    print(f"\nData Summary:")
    print(f"  Total records: {len(df)}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  GHI statistics (kWh/m²/day):")
    print(f"    Mean:   {df['ghi_kwh_m2'].mean():.2f}")
    print(f"    Median: {df['ghi_kwh_m2'].median():.2f}")
    print(f"    Min:    {df['ghi_kwh_m2'].min():.2f}")
    print(f"    Max:    {df['ghi_kwh_m2'].max():.2f}")
    
    print("\n✓ First 5 rows:")
    print(df.head())
    
    print("\n✓ Last 5 rows:")
    print(df.tail())
    
    print("\n" + "=" * 60)
    print("SUCCESS! GHI data is ready for analysis.")
    print("=" * 60)
    
except requests.exceptions.RequestException as e:
    print(f"\n✗ Error downloading data: {e}")
    print("\nTroubleshooting:")
    print("1. Check your internet connection")
    print("2. The NASA POWER server might be temporarily down")
    print("3. Try the manual download link:")
    print(f"   https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude={LONGITUDE}&latitude={LATITUDE}&start={START_DATE}&end={END_DATE}&format=CSV")
    
except Exception as e:
    print(f"\n✗ Error processing data: {e}")
    print("Please check the API response format or contact NASA POWER support.")
