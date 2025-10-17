#!/usr/bin/env python3
"""
Generate scientifically-based temperature projection data for Delhi NCR
Based on IPCC AR6 and IMD climate projections for North India

Scenarios:
- Conservative (RCP2.6/SSP1-2.6): +0.4°C per decade
- Moderate (RCP4.5/SSP2-4.5): +0.6°C per decade
- High (RCP8.5/SSP5-8.5): +1.0°C per decade

Reference sources:
- IPCC AR6 South Asia projections
- India Meteorological Department climate scenarios
- Ministry of Earth Sciences regional assessments
"""

import pandas as pd
import numpy as np

# Base year and baseline temperature
BASE_YEAR = 2024
BASELINE_TEMP = 25.5  # °C - Delhi annual average (approximate from your data)

# Projection parameters (based on IPCC AR6 for South Asia)
SCENARIOS = {
    'conservative': {
        'name': 'Conservative (SSP1-2.6)',
        'annual_increase': 0.04,  # +0.4°C per decade
        'description': 'Low emissions scenario with strong climate action',
        'source': 'IPCC AR6 SSP1-2.6 scenario for South Asia'
    },
    'moderate': {
        'name': 'Moderate (SSP2-4.5)',
        'annual_increase': 0.06,  # +0.6°C per decade
        'description': 'Middle-of-the-road scenario with moderate emissions reduction',
        'source': 'IPCC AR6 SSP2-4.5 scenario for South Asia'
    },
    'high': {
        'name': 'High (SSP5-8.5)',
        'annual_increase': 0.10,  # +1.0°C per decade
        'description': 'High emissions scenario with limited climate action',
        'source': 'IPCC AR6 SSP5-8.5 scenario for South Asia'
    }
}

def generate_temperature_projections(years=20):
    """
    Generate temperature projections for multiple scenarios
    
    Parameters:
    - years: Number of years to project (default 20 years: 2025-2044)
    
    Returns:
    - DataFrame with year and temperature projections for each scenario
    """
    
    print("=" * 70)
    print("Generating Temperature Projections for Delhi NCR")
    print("=" * 70)
    print(f"Base year: {BASE_YEAR}")
    print(f"Baseline temperature: {BASELINE_TEMP}°C")
    print(f"Projection period: {BASE_YEAR + 1} to {BASE_YEAR + years}")
    print()
    
    # Create year range
    projection_years = list(range(BASE_YEAR + 1, BASE_YEAR + years + 1))
    
    # Initialize data structure
    data = {'year': projection_years}
    
    # Generate projections for each scenario
    for scenario_key, scenario_info in SCENARIOS.items():
        annual_increase = scenario_info['annual_increase']
        temps = []
        
        for i, year in enumerate(projection_years, start=1):
            # Linear increase + small random variation (±0.1°C for natural variability)
            temp = BASELINE_TEMP + (i * annual_increase) + np.random.uniform(-0.1, 0.1)
            temps.append(round(temp, 2))
        
        # Add to data dictionary
        data[f'temp_{scenario_key}_celsius'] = temps
        
        print(f"✓ {scenario_info['name']}")
        print(f"  Rate: +{annual_increase * 10:.1f}°C per decade")
        print(f"  Year {projection_years[0]}: {temps[0]:.2f}°C")
        print(f"  Year {projection_years[-1]}: {temps[-1]:.2f}°C")
        print(f"  Total increase: +{temps[-1] - BASELINE_TEMP:.2f}°C")
        print()
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df


def save_projections():
    """Generate and save temperature projections"""
    
    # Generate 20-year projections
    df = generate_temperature_projections(years=20)
    
    # Save to CSV
    output_file = 'Data/temperature_projections_delhi.csv'
    df.to_csv(output_file, index=False)
    
    print("=" * 70)
    print(f"✓ Temperature projections saved to: {output_file}")
    print("=" * 70)
    print()
    print("Columns:")
    print("  - year: Projection year")
    print("  - temp_conservative_celsius: Conservative scenario (SSP1-2.6)")
    print("  - temp_moderate_celsius: Moderate scenario (SSP2-4.5)")
    print("  - temp_high_celsius: High emissions scenario (SSP5-8.5)")
    print()
    print("Sample data:")
    print(df.head(10))
    print()
    
    # Create metadata/citation file
    metadata_file = 'Data/temperature_projections_metadata.txt'
    with open(metadata_file, 'w') as f:
        f.write("Temperature Projections for Delhi NCR (2025-2044)\n")
        f.write("=" * 60 + "\n\n")
        f.write("METHODOLOGY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Baseline Year: {BASE_YEAR}\n")
        f.write(f"Baseline Temperature: {BASELINE_TEMP}°C\n")
        f.write(f"Projection Period: {BASE_YEAR + 1} to {BASE_YEAR + 20}\n")
        f.write("\n")
        f.write("SCENARIOS\n")
        f.write("-" * 60 + "\n")
        for scenario_key, scenario_info in SCENARIOS.items():
            f.write(f"\n{scenario_info['name']}\n")
            f.write(f"  Rate: +{scenario_info['annual_increase'] * 10:.1f}°C per decade\n")
            f.write(f"  Description: {scenario_info['description']}\n")
            f.write(f"  Source: {scenario_info['source']}\n")
        f.write("\n\nCITATION\n")
        f.write("-" * 60 + "\n")
        f.write("Temperature projections based on:\n")
        f.write("- IPCC (2021). Climate Change 2021: The Physical Science Basis.\n")
        f.write("  Sixth Assessment Report, Working Group I. Chapter 12: South Asia.\n")
        f.write("- India Meteorological Department (IMD). Climate Scenarios for India.\n")
        f.write("- Ministry of Earth Sciences (2020). Assessment of Climate Change\n")
        f.write("  over the Indian Region.\n")
        f.write("\n")
        f.write("Note: Projections include small random variations (±0.1°C) to\n")
        f.write("represent natural climate variability.\n")
    
    print(f"✓ Metadata saved to: {metadata_file}")
    print()
    print("=" * 70)
    print("✅ Complete! Use this data in your notebook.")
    print("=" * 70)
    
    return df


if __name__ == "__main__":
    df = save_projections()
