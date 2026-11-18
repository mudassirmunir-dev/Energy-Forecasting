
# Exploratory Data Analysis (EDA)

## 1. Electricity Consumption Over Time

- Visualized average electricity readings across all building columns.
- Used hourly timestamps to observe changes over time.
- The chart provides an overall trend rather than individual building consumption.

## 2. Weather Missing Values

- Visualized missing-value percentages for weather features.
- precipDepth6HR has the highest missing percentage (94.52%).
- cloudCoverage has 51.63% missing values.
- airTemperature has only 0.04% missing values.

## 3. Building Distribution by Primary Usage

- Visualized the number of buildings in each primary usage category.
- Used metadata column primaryspaceusage.
- This helps identify the dominant building categories.

## 4. Electricity Trend Analysis

- Average electricity readings fluctuate throughout the observation period.
- Most readings appear approximately between 110 and 180.
- Higher average readings are visible during parts of June–September 2016.
- Several unusually high peaks appear in October 2016, January 2017, September 2017, and November 2017.
- These peaks may represent genuine demand spikes or unusual observations.
- Further investigation is required before treating them as outliers.

## 5. Building Distribution Analysis

- Education is the most common building category.
- Office is the second most common category.
- Entertainment/public assembly, lodging/residential, and public services are also represented.
- Healthcare and warehouse/storage have relatively few buildings.
- Building usage categories are imbalanced.

## 6. Weather Missing-Value Analysis

- precipDepth6HR has 94.52% missing values.
- cloudCoverage has 51.63% missing values.
- precipDepth1HR has 40.22% missing values.
- airTemperature has only 0.04% missing values.
- windSpeed has only 0.17% missing values.
- Timestamp and site_id contain no missing values.

## 7. EDA Conclusions

- Electricity readings fluctuate over the observation period.
- Several unusually high electricity peaks require further investigation.
- Education buildings dominate the building distribution.
- Weather features have different levels of missingness.
- Temperature and wind speed are relatively complete features.
- Further preprocessing is required before machine learning.

### Important Limitation

The chart represents the average across available building readings at each timestamp. It does not represent the total electricity consumption of all buildings.

## Output Files

- outputs/figures/electricity_over_time.png
- outputs/figures/weather_missing_values.png
- outputs/figures/building_usage_distribution.png
