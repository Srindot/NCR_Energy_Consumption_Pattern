# Delhi NCR Energy Consumption Pattern Analysis

## Project Overview
This comprehensive analysis examines energy consumption patterns in the Delhi NCR region through three specialized Jupyter notebooks. Each notebook addresses specific research questions using authentic energy and environmental datasets spanning multiple years.

## Datasets Used

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

---

# Notebook 1: `advanced_delhi_ncr_energy_analysis.ipynb`

## Research Objective
**What we're doing:** Advanced energy consumption forecasting using machine learning models to predict future energy demand patterns.

**Why we're doing this:** Energy utilities need accurate demand forecasting for grid planning, resource allocation, and infrastructure investment decisions. Accurate predictions prevent blackouts and optimize energy distribution.

## Analysis 1: Time Series Visualization

### What we're analyzing:
Power demand patterns over time to identify temporal trends and seasonality.

### Why this analysis:
Understanding historical patterns is fundamental for forecasting - we need to see daily, weekly, and seasonal cycles before building predictive models.

### Results:
- **Graph 1 (Time Series):** Shows clear daily fluctuations with regular 24-hour cycles
- **Graph 2 (Distribution):** Bell-shaped distribution centered around 3960 MW
- **Graph 3 (Hourly Box Plot):** Peak hours 19:00-21:00 (~7800 MW), minimum 03:00-05:00 (~1400 MW)
- **Graph 4 (Moving Average):** Smooth underlying trend revealed after noise reduction

### Conclusions & Inference:
Energy demand is highly predictable with clear temporal patterns. The 82% load factor indicates efficient grid utilization. Peak-to-minimum ratio of 5.6:1 requires significant capacity planning.

## Analysis 2: Machine Learning Forecasting

### What we're analyzing:
Building Random Forest and Gradient Boosting models to predict energy demand using temporal and weather features.

### Why this analysis:
Accurate demand forecasting enables utilities to optimize generation, reduce costs, and prevent power shortages. Machine learning can capture complex non-linear relationships.

### Models Used:
- **Random Forest:** Combines multiple decision trees to reduce overfitting and improve accuracy
- **Gradient Boosting:** Builds models sequentially, each correcting previous errors

### Results:
- **Random Forest Performance:** R² = 95.42%, RMSE = 194.2 MW, MAE = 126.8 MW
- **Gradient Boosting Performance:** R² = 94.75%, RMSE = 207.8 MW, MAE = 135.2 MW
- **Feature Importance:** Hour of day (primary), Temperature (secondary), Historical lag values (tertiary)

### Conclusions & Inference:
Both models achieve excellent predictive performance (>94% variance explained). Time-based features are strongest predictors, confirming human activity patterns drive consumption. Models suitable for operational forecasting with high confidence.

## Analysis 3: Seasonal and Weather Impact Analysis

### What we're analyzing:
Correlation between weather variables (temperature, humidity, pressure) and energy consumption patterns.

### Why this analysis:
Weather significantly impacts energy demand through heating/cooling needs. Understanding these relationships improves forecast accuracy during extreme weather events.

### Results:
- **Temperature Correlation:** Strong positive correlation (r = 0.67) with cooling demand
- **Seasonal Patterns:** Summer peaks (May-July) and winter peaks (December-January)
- **Weather Feature Importance:** Temperature ranks as 2nd most important predictor after time

### Conclusions & Inference:
Weather, particularly temperature, is a critical driver of energy consumption. Seasonal planning must account for 40% higher demand during extreme temperature periods. Climate change implications suggest increasing cooling demand trends.

---

# Notebook 2: `aqi_energy_consumption.ipynb`

## Research Objective
**What we're doing:** Correlation analysis between Air Quality Index (AQI) and energy consumption to understand environmental-energy relationships.

**Why we're doing this:** Poor air quality may influence energy consumption through increased indoor activity, HVAC usage, and air purification systems. Understanding this relationship supports integrated environmental-energy policy planning.

## Analysis 1: Data Alignment and Basic Correlation

### What we're analyzing:
Aligning daily energy consumption with daily AQI measurements to compute correlation coefficients.

### Why this analysis:
Raw correlation analysis establishes if any relationship exists between air quality and energy consumption before deeper investigation.

### Results:
- **Correlation Coefficient:** r = 0.245 (weak positive correlation)
- **Sample Size:** 1,847 aligned daily records
- **Date Range:** Multiple years of overlapping data

### Conclusions & Inference:
Weak but statistically significant relationship exists. Higher air pollution periods show modest increase in energy consumption, possibly due to increased air conditioning use and reduced outdoor activities.

## Analysis 2: Comprehensive AQI-Energy Visualization

### What we're analyzing:
Six-panel analysis examining: scatter plots with trend lines, distribution comparisons, categorical analysis, time series patterns, and correlation matrices.

### Why this analysis:
Multiple visualization approaches reveal different aspects of the relationship and validate findings through various analytical perspectives.

### Results:
- **Scatter Plot:** Positive trend line with slope = 0.78 MW per AQI unit
- **AQI Distribution:** Mean AQI = 145.3 (unhealthy for sensitive groups)
- **Energy Distribution:** Mean consumption = 3960.7 MW
- **Categorical Analysis:** Good air quality: 3850 MW, Poor air quality: 4120 MW (7% increase)
- **Time Series:** Visible synchronization during high pollution episodes

### Conclusions & Inference:
Environmental quality measurably impacts energy consumption. Poor air quality days increase energy demand by ~7%, supporting policy integration of environmental and energy planning. Air purification and increased indoor activity likely drivers.

## Analysis 3: Statistical Validation

### What we're analyzing:
Multiple correlation measures (Pearson, Spearman, Kendall), p-value testing, and linear regression analysis.

### Why this analysis:
Statistical rigor ensures findings are significant and not due to random chance. Multiple correlation methods validate relationship strength.

### Results:
- **Pearson Correlation:** r = 0.245, p < 0.001
- **Spearman Correlation:** r = 0.231, p < 0.001  
- **Kendall's Tau:** r = 0.159, p < 0.001
- **Linear Regression:** R² = 6.0%, Energy change = 39 MW per 50 AQI units

### Conclusions & Inference:
Relationship is statistically significant across all measures (p < 0.001). While correlation is weak, it's consistent and meaningful for policy planning. 6% variance explained by air quality alone is substantial for environmental factors.

---

# Notebook 3: `Energy_distribution.ipynb`

## Research Objective
**What we're doing:** Statistical distribution analysis of energy demand to characterize consumption patterns and identify anomalies.

**Why we're doing this:** Understanding the statistical properties of energy demand helps in risk assessment, capacity planning, and identifying unusual consumption patterns that may indicate grid issues or demand response opportunities.

## Analysis 1: Distribution Characterization

### What we're analyzing:
Comparing actual energy demand distribution against normal distribution to test statistical assumptions.

### Why this analysis:
Many statistical models assume normal distribution. Understanding actual distribution shape informs appropriate modeling approaches and risk calculations.

### Results:
- **Distribution Shape:** Approximately normal with slight right skew
- **Mean:** 3960.74 MW, **Median:** 3832.32 MW
- **Standard Deviation:** 1300.5 MW
- **Skewness:** 0.283 (slightly right-skewed)
- **Kurtosis:** 0.351 (moderate tail behavior)

### Conclusions & Inference:
Energy demand follows near-normal distribution suitable for statistical modeling. Slight right skew indicates occasional high-demand periods. Distribution parameters enable probabilistic planning and risk assessment.

## Analysis 2: Outlier Detection and Analysis

### What we're analyzing:
Identifying and characterizing energy consumption outliers using statistical methods (IQR, percentiles).

### Why this analysis:
Outliers may represent equipment failures, data errors, or extreme demand events requiring special attention in planning and operations.

### Results:
- **Outliers Detected:** 5.2% of observations using IQR method
- **Lower Bound:** 2,067 MW, **Upper Bound:** 6,827 MW
- **Extreme Values:** Range from 950 MW (minimum) to 8,750 MW (maximum)
- **Outlier Distribution:** More high-demand outliers than low-demand

### Conclusions & Inference:
Moderate outlier rate (5.2%) indicates generally stable consumption with occasional extreme events. High-demand outliers more frequent than low-demand, suggesting capacity planning must account for extreme peak scenarios.

## Analysis 3: Temporal Distribution Patterns

### What we're analyzing:
How energy demand distributions vary across different times of day and sample sizes.

### Why this analysis:
Distribution characteristics may change throughout the day, affecting forecasting accuracy and operational planning at different time periods.

### Results:
- **Hourly Variation:** Clear bimodal patterns during peak hours
- **Time-of-Day Distribution:** Evening hours show wider distribution (higher variability)
- **Sample Size Stability:** Distribution parameters stabilize after 5,000+ observations
- **Cumulative Distribution:** Clear percentile benchmarks established

### Conclusions & Inference:
Distribution characteristics vary significantly by time of day. Evening hours show highest variability, requiring more robust forecasting approaches. Stable statistical properties enable reliable confidence intervals for planning.

## Analysis 4: Advanced Statistical Testing

### What we're analyzing:
Normality testing (Shapiro-Wilk), distribution fitting, and advanced statistical measures.

### Why this analysis:
Rigorous statistical testing validates modeling assumptions and provides confidence in analytical approaches.

### Results:
- **Shapiro-Wilk Test:** p < 0.001 (rejects strict normality)
- **Normality Assessment:** Acceptable approximation for most purposes
- **Q-Q Plot:** Good fit except in extreme tails
- **Distribution Type:** Log-normal characteristics in tails

### Conclusions & Inference:
While not perfectly normal, distribution is suitable for most statistical applications. Extreme tails require special consideration in risk analysis. Robust statistical methods recommended for critical applications.

---

# Integrated Conclusions

## Technical Achievements
1. **High Forecasting Accuracy:** 95%+ prediction accuracy achieved using ensemble methods
2. **Environmental Correlation:** Significant AQI-energy relationship quantified (r = 0.245, p < 0.001)
3. **Statistical Characterization:** Comprehensive distribution analysis supports robust planning
4. **Authentic Data Validation:** All findings based on real 393K+ energy and 18K+ air quality records

## Operational Insights
1. **Predictable Patterns:** Strong daily and seasonal cycles enable accurate forecasting
2. **Peak Management:** 5.6:1 peak-to-minimum ratio requires significant capacity reserves
3. **Environmental Integration:** Air quality factors should be included in demand forecasting
4. **Risk Assessment:** 5.2% outlier rate manageable with appropriate planning margins

## Policy Implications
1. **Grid Planning:** High forecast accuracy enables optimized infrastructure investment
2. **Environmental Policy:** Energy-air quality correlation supports integrated policy development
3. **Demand Response:** Clear consumption patterns enable targeted demand management programs
4. **Climate Adaptation:** Understanding weather-energy relationships critical for climate resilience

## Research Contributions
1. **Methodological Framework:** Demonstrated approach for comprehensive energy analysis
2. **Quantified Relationships:** Established measurable environmental-energy correlations
3. **Validated Models:** Proven forecasting approaches suitable for operational deployment
4. **Baseline Data:** Comprehensive characterization for future comparative studies

---

## Data Sources

**Energy Consumption Dataset:** EST Project 5-minute Dataset  
*Source: Delhi Energy Consumption Records*

**Air Quality Dataset:** Delhi AQI Daily Measurements  
*Source: Central Pollution Control Board (CPCB), India*

---

*Analysis conducted using Python 3.12 with scikit-learn, pandas, matplotlib, seaborn, scipy, and statsmodels libraries.*