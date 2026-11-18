
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

## 8. Selected Electricity Dataset Analysis

- Removed two completely empty building columns.
- Selected 1,474 buildings with less than 20% missing readings.
- The prepared dataset contains 17,544 rows and 1,475 columns, including the timestamp.
- Missing-value analysis identified 1,101 building columns with missing readings.
- 374 building columns contain no missing readings.
- The highest missing percentage among selected buildings is approximately 19.10%.

## 9. Missing-Value Visualization

- Generated a chart showing the top 20 buildings with the highest missing-value percentages.
- The visualization helps identify buildings that require further investigation.
- Missing readings have not yet been imputed.
- Continuous missing-data gaps were investigated before selecting a cleaning strategy.

## 10. Missing-Data Gap Visualization

- Visualized missing-data patterns for the five buildings with the longest continuous missing periods.
- Eagle_office_Amie has the longest missing period of 3,351 consecutive hours.
- Bear_education_Merrill has a longest gap of 2,991 hours.
- Rat_public_Johnna has a longest gap of 2,343 hours.
- Bear_assembly_Angel has a longest gap of 2,297 hours.
- Bear_assembly_Diana has a longest gap of 2,149 hours.
- These long gaps should not be automatically filled through interpolation.
- Further missing-value treatment decisions are required before model training.

## 11. Timestamp Validation

- Validated all 17,544 timestamps.
- No invalid timestamps were identified.
- No duplicate timestamps were identified.
- No irregular hourly intervals were identified.
- No missing hourly intervals were identified.
- The dataset covers January 1, 2016, to December 31, 2017.
- The observed frequency is exactly one hour.

### Important Limitation

The electricity trend chart represents the average across available building readings at each timestamp. It does not represent the total electricity consumption of all buildings.

## Output Files

### Figures

- outputs/figures/electricity_over_time.png
- outputs/figures/weather_missing_values.png
- outputs/figures/building_usage_distribution.png
- outputs/figures/top_20_missing_buildings.png
- outputs/figures/missing_gaps_top_5_buildings.png

### Reports

- outputs/reports/building_missing_report.csv
- outputs/reports/selected_missing_report.csv
- outputs/reports/missing_gap_analysis.csv
- outputs/reports/timestamp_validation_report.csv

## 12. Selected Building Electricity Analysis

Selected building: Robin_office_Wai

- Building usage: Office
- Site: Robin
- Building area: 16,221 sqm
- Observation period: January 1, 2016, to December 31, 2017.
- Total hourly electricity readings: 17,544.
- Missing electricity readings: 0.
- Average electricity reading: 166.28.
- Minimum electricity reading: 0.
- Maximum electricity reading: 497.70.
- Standard deviation: 103.84.
- Negative readings: 0.

### Zero Reading Analysis

- Identified 44 zero electricity readings.
- These represent approximately 0.25% of all observations.
- The readings occurred in two consecutive periods:
  - April 16, 2017, 02:00–23:00: 22 hours.
  - April 17, 2017, 02:00–23:00: 22 hours.
- The cause of these zero readings has not been confirmed.
- Zero readings will be retained until further investigation.

### Time-Series Visualization Findings

- Electricity readings show repeated hourly fluctuations.
- Higher peaks are visible during parts of 2016.
- An unusual lower-consumption period is visible between April and August 2017.
- A noticeable change in the consumption pattern appears around September 2017.
- These changes require further investigation before being classified as errors or outliers.

### Output Figures

- outputs/figures/robin_office_electricity_timeseries.png
- outputs/figures/robin_office_zero_readings.png

## 13. Weather Alignment for Selected Building

- Selected building: Robin_office_Wai
- Site ID: Robin
- Electricity timestamps: 17,544.
- Weather timestamps: 17,516.
- Matching timestamps: 17,516.
- Electricity-only timestamps: 28.
- Weather-only timestamps: 0.
- Approximately 99.84% of electricity timestamps have matching weather records.

### Weather Feature Quality

- airTemperature has 1 missing value.
- dewTemperature has 1 missing value.
- cloudCoverage has 14,149 missing values.
- precipDepth1HR has 17,516 missing values.
- precipDepth6HR has 16,097 missing values.
- seaLvlPressure has 61 missing values.
- windDirection has 6 missing values.
- windSpeed has no missing values.

Highly incomplete weather features will be reviewed before feature selection.

### Output Report

- outputs/reports/candidate_alignment_report.csv

## 14. Robin Site-Wide Building Comparison

To investigate the unusual electricity consumption drop in
Robin_office_Wai, 51 buildings belonging to the Robin site
were compared.

The comparison uses May, June, and July from 2016 and 2017.

### Results

- Total buildings compared: 51
- Buildings with decreased average readings: 29
- Buildings with increased average readings: 22
- Median percentage change across buildings: -3.93%
- Robin_office_Wai percentage change: -89.87%

### Selected Building Comparisons

| Building | Percentage Change |
|---|---:|
| Robin_office_Wai | -89.87% |
| Robin_lodging_Phillip | -84.92% |
| Robin_education_Lashandra | -69.04% |
| Robin_education_Derick | -37.66% |
| Robin_office_Saul | -36.13% |
| Robin_office_Donald | +100.20% |

### Findings

- Electricity consumption did not decrease uniformly across
  all buildings at the Robin site.
- Some buildings experienced substantial decreases.
- Other buildings experienced increases.
- Robin_office_Wai had a substantially larger decrease than
  the median building-level change.
- The unusual consumption drop may be building-specific or
  affect a subset of buildings.

### Limitations

Percentage changes can become very large when the 2016
baseline consumption is close to zero.

These comparisons do not establish whether the changes
were caused by operational activity, equipment changes,
meter problems, or data collection issues.

### Output Report

- outputs/reports/robin_site_building_comparison.csv
