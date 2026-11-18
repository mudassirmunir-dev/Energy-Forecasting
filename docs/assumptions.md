
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
