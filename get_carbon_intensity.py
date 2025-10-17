#!/usr/bin/env python3
"""
Fetch India Grid Carbon Intensity from Climatiq API
Based on CEA (Central Electricity Authority) CO2 Baseline Database 2024
"""

import requests
import json

# Instructions:
# 1. Go to https://www.climatiq.io and create a free account
# 2. Go to Dashboard → API Keys and copy your key
# 3. Replace YOUR_API_KEY_HERE below with your actual key

CLIMATIQ_API_KEY = "YOUR_API_KEY_HERE"  # Replace this with your actual API key

API_URL = "https://api.climatiq.io/data/v1/estimate"

def get_india_carbon_intensity():
    """
    Fetch India's grid carbon intensity from Climatiq API
    Source: CEA (Central Electricity Authority) Official Data
    """
    
    print("=" * 70)
    print("Fetching India Grid Carbon Intensity from Climatiq API")
    print("Source: CEA (Central Electricity Authority) CO2 Baseline Database")
    print("=" * 70)
    
    # Check if API key is set
    if CLIMATIQ_API_KEY == "YOUR_API_KEY_HERE":
        print("\n❌ ERROR: Please set your Climatiq API key!")
        print("\nSteps:")
        print("1. Go to: https://www.climatiq.io")
        print("2. Create free account")
        print("3. Go to Dashboard → API Keys")
        print("4. Copy your key")
        print("5. Edit this script and replace YOUR_API_KEY_HERE with your key")
        return None
    
    headers = {
        "Authorization": f"Bearer {CLIMATIQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "emission_factor": {
            "activity_id": "electricity-supply_grid-source_supplier_mix",
            "source": "Government of India - Central Electricity Authority",
            "region": "IN",
            "year": 2024,
            "source_lca_activity": "electricity_generation"
        },
        "parameters": {
            "energy": 1000,
            "energy_unit": "kWh"
        }
    }
    
    print("\n📡 Requesting data from Climatiq API...")
    
    try:
        response = requests.post(API_URL, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        print("✅ Data retrieved successfully!\n")
        print("=" * 70)
        print("INDIA GRID CARBON INTENSITY (2024)")
        print("=" * 70)
        
        # Extract key values
        co2e = result.get('co2e', 0)  # kg CO2 equivalent per 1000 kWh
        co2 = result.get('co2', 0)    # kg CO2 per 1000 kWh
        
        # Convert to gCO2/kWh (standard unit)
        co2e_g_per_kwh = co2e  # Already in kg per 1000 kWh = g per kWh
        co2_g_per_kwh = co2
        
        print(f"\n📊 Carbon Intensity Values:")
        print(f"   CO₂e (CO2 equivalent): {co2e_g_per_kwh:.1f} gCO₂e/kWh")
        print(f"   CO₂ (Carbon dioxide):  {co2_g_per_kwh:.1f} gCO₂/kWh")
        
        print(f"\n📋 Official Source:")
        print(f"   Authority: Central Electricity Authority (CEA), India")
        print(f"   Database: CO₂ Baseline Database Version 20.0 (2024)")
        print(f"   Region: India (National Grid)")
        print(f"   Year: 2024")
        
        print(f"\n📝 Citation:")
        print(f'   "Grid emission factor for India: {co2e_g_per_kwh:.0f} gCO₂e/kWh"')
        print(f'   Source: Central Electricity Authority (CEA), CO₂ Baseline Database')
        print(f'   v20.0, 2024, via Climatiq API (https://www.climatiq.io)')
        
        print("\n" + "=" * 70)
        print("✅ RESULT: Use {:.0f} gCO₂/kWh in your notebook".format(co2e_g_per_kwh))
        print("=" * 70)
        
        # Save to file for reference
        output_file = "Data/carbon_intensity_india.txt"
        with open(output_file, 'w') as f:
            f.write("India Grid Carbon Intensity\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Value: {co2e_g_per_kwh:.1f} gCO₂e/kWh\n")
            f.write(f"Source: Central Electricity Authority (CEA)\n")
            f.write(f"Database: CO₂ Baseline Database Version 20.0\n")
            f.write(f"Year: 2024\n")
            f.write(f"Retrieved: {result.get('audit_trail', 'N/A')}\n\n")
            f.write("Full API Response:\n")
            f.write(json.dumps(result, indent=2))
        
        print(f"\n💾 Details saved to: {output_file}")
        
        return co2e_g_per_kwh
        
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ HTTP Error: {e}")
        print(f"Response: {response.text}")
        if response.status_code == 401:
            print("\n⚠️  Authentication failed. Please check your API key.")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request Error: {e}")
        return None
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


if __name__ == "__main__":
    intensity = get_india_carbon_intensity()
    
    if intensity:
        print("\n✨ Success! You can now use this value in your notebook.")
        print(f"   Update the carbon_intensity_g_per_kwh variable to: {intensity:.0f}")
    else:
        print("\n⚠️  Could not retrieve data. Please check the errors above.")
