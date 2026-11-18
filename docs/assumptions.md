
# Data Quality Observations and Assumptions

## 1. Electricity Dataset

- Contains 17,544 rows and 1,579 columns.
- Two building columns contain 100% missing values.
- Several other building columns contain high percentages of missing readings.
- Electricity data is initially stored in wide format.

## 2. Weather Dataset

- Contains 331,166 rows and 10 columns.
- precipDepth6HR has 94.52% missing values.
- cloudCoverage has 51.63% missing values.
- precipDepth1HR has 40.22% missing values.
- airTemperature has only 0.04% missing values.

## 3. Metadata Dataset

- Contains 1,636 rows and 32 columns.
- Several optional fields have substantial missingness.
- solar, leed_level, and date_opened have more than 98% missing values.

## 4. Initial Assumptions

- Completely empty electricity columns will be considered for removal.
- Columns with high missingness will be evaluated before removal.
- Missing weather values will not automatically be replaced with zero.
- Special values such as -1 in precipitation fields require investigation.
- Cleaning decisions will be documented before model training.


## Electricity Building Selection

After removing two completely empty columns, 1,576 building columns remained.

Missing-value analysis identified:

- 1,474 buildings with less than 20% missing readings.
- 40 buildings with 20–50% missing readings.
- 62 buildings with more than 50% missing readings.

### Selection Rule

For the initial modelling dataset, buildings with less than 20% missing readings will be retained.

Buildings with 20% or more missing readings will be excluded from the initial modelling dataset.

This threshold is an initial project assumption and may be reviewed during further analysis.

## Timestamp Validation

The selected electricity dataset contains 17,544 hourly records covering 2016–2017.

Timestamp validation identified:

- Invalid timestamps: 0
- Duplicate timestamps: 0
- Irregular hourly intervals: 0
- Missing hourly intervals: 0
- Expected interval: 1 hour

All timestamps are valid and consecutive.

## Missing-Data Gap Analysis

The 20 buildings with the highest missing percentages were investigated.

The analysis identified different missing-data patterns:

- Some buildings contain a small number of long continuous gaps.
- Some buildings contain many separate missing periods.
- The longest observed missing period was 3,351 consecutive hours.

### Initial Missing-Data Treatment Assumptions

- Short gaps of 1–3 hours may be considered for interpolation.
- Gaps of 4–24 hours require further investigation.
- Gaps longer than 24 hours will not automatically be imputed.
- Missing readings will not automatically be replaced with zero.
- All missing-data treatment decisions will be evaluated before model training.
