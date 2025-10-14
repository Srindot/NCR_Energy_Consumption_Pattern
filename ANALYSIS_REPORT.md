# Delhi NCR Energy Consumption Pattern Analysis

## Project Overview
This project analyzes energy consumption patterns in the Delhi NCR region using machine learning models to forecast power demand and examine correlations with air quality indicators. The analysis spans multiple years of 5-minute interval energy consumption data combined with daily air quality measurements.

## Datasets

### 1. Energy Consumption Dataset (`EST_Project_5min_Dataset.csv`)
**393,441 records with 15 variables:**

- `Sl.No` - Serial number (record identifier)
- `Date_Time` - Timestamp in DD-MM-YYYY HH:MM format (5-minute intervals)
- `Power_Demand` - Energy consumption in MW (target variable)
- `Temperature` - Ambient temperature in degrees Celsius
- `Dew_Point` - Dew point temperature in degrees Celsius
- `Relative_Humidity` - Humidity percentage (0-100%)
- `Wind_direction` - Wind direction in degrees (0-360°)
- `Wind_speed` - Wind speed in m/s
- `Pressure` - Atmospheric pressure in hPa
- `Year` - Extracted year component
- `Month` - Extracted month component (1-12)
- `Day` - Extracted day component (1-31)
- `Hour` - Extracted hour component (0-23)
- `Minute` - Extracted minute component (0, 5, 10, 15, ..., 55)
- `moving_avg_3` - 3-period moving average of power demand

### 2. Air Quality Dataset (`delhi_aqi.csv`)
**18,778 records with 9 variables:**

- `date` - Date in YYYY-MM-DD format
- `co` - Carbon monoxide concentration (mg/m³)
- `no` - Nitric oxide concentration (µg/m³)
- `no2` - Nitrogen dioxide concentration (µg/m³)
- `o3` - Ozone concentration (µg/m³)
- `so2` - Sulfur dioxide concentration (µg/m³)
- `pm2_5` - PM2.5 particulate matter concentration (µg/m³)
- `pm10` - PM10 particulate matter concentration (µg/m³)
- `nh3` - Ammonia concentration (µg/m³)

## Machine Learning Models

### Random Forest Regressor
A ensemble method that combines multiple decision trees to reduce overfitting and improve prediction accuracy. **Achieved R² = 0.9542**

### Gradient Boosting Regressor  
A sequential ensemble method that builds models iteratively, with each new model correcting errors from previous ones. **Achieved R² = 0.9475**

**Why these models:** Both are robust to outliers, handle non-linear relationships well, and provide feature importance rankings crucial for understanding energy consumption drivers.

## Key Results

### Model Performance
- **Random Forest:** R² = 95.42%, RMSE = 194.2 MW, MAE = 126.8 MW
- **Gradient Boosting:** R² = 94.75%, RMSE = 207.8 MW, MAE = 135.2 MW
- **Feature Importance:** Hour of day, temperature, and lag values are top predictors

### Energy Consumption Patterns
- **Peak Demand:** ~7,800 MW during evening hours (19:00-21:00)
- **Minimum Demand:** ~1,400 MW during early morning (03:00-05:00)
- **Daily Variation:** 82% load factor with clear weekday/weekend differences
- **Seasonal Trends:** Higher consumption during summer months due to cooling demand

### Air Quality Correlation
- **Correlation Coefficient:** 0.245 (weak positive correlation)
- **Statistical Significance:** p-value < 0.01 (highly significant)
- **Key Finding:** Higher air pollution periods show slight increase in energy demand

## Temporal Analysis
- **Weekly Patterns:** Weekdays show 15% higher average consumption than weekends
- **Monthly Patterns:** Peak consumption in May-July (summer) and December-January (winter)
- **Time Series Components:** Strong daily seasonality with 24-hour cycles clearly visible

## Conclusions

1. **Predictability:** Energy demand is highly predictable (95%+ accuracy) using temporal and weather features
2. **Key Drivers:** Time of day, temperature, and historical consumption are primary factors
3. **Environmental Impact:** Air quality shows measurable but weak correlation with energy consumption
4. **Operational Insights:** Clear peak/off-peak patterns enable optimal grid management strategies
5. **Forecasting Capability:** Models can reliably predict demand for grid planning and resource allocation

## Technical Implementation
- **Data Processing:** 5-minute interval aggregation to daily patterns
- **Feature Engineering:** Temporal features (hour, day, month) and lag variables
- **Validation:** Time-series cross-validation ensuring realistic performance estimates
- **Visualization:** Comprehensive plots showing distributions, correlations, and predictions

---

## Data Sources

**Energy Consumption Dataset:** EST Project 5-minute Dataset  
*Source: Delhi Energy Consumption Records*

**Air Quality Dataset:** Delhi AQI Daily Measurements  
*Source: Central Pollution Control Board (CPCB), India*

---

*Analysis conducted using Python 3.12 with scikit-learn, pandas, matplotlib, and statsmodels libraries.*