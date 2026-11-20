# Building Energy Consumption Forecasting

**PSEB AI Engineering Course — Data Engineering & Machine Learning Project**

**Author:** Mudassir Munir  
**Course ID:** PSEB-2026-010784

---

## 1. Project Overview

This project develops a reproducible data pipeline and machine learning workflow for analyzing and forecasting building electricity consumption.

It uses the Building Data Genome Project 2 (BDG2), a real-world dataset containing electricity meter readings, building metadata, and weather observations.

The project covers:

- Raw data inspection and quality assessment.
- Data cleaning and validation.
- Exploratory data analysis and visualization.
- Building metadata and weather analysis.
- SQLite database creation and SQL analysis.
- Feature engineering.
- Machine learning model comparison.
- Model evaluation and error analysis.
- Saving and reloading a trained model for predictions.

## 2. Dataset

**Dataset:** Building Data Genome Project 2 (BDG2)

**Official source:**  
https://github.com/buds-lab/building-data-genome-project-2

**Dataset license:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

The dataset contains building electricity consumption readings, weather information, and building metadata.

### Dataset files

| File | Description |
|---|---|
| electricity.csv | Hourly electricity meter readings |
| weather.csv | Weather observations |
| metadata.csv | Building information and characteristics |

### Original dataset statistics

| Dataset | Rows | Columns |
|---|---:|---:|
| Electricity | 17,544 | 1,579 |
| Weather | 331,166 | 10 |
| Metadata | 1,636 | 32 |

The original electricity dataset contains 1,578 building columns and one timestamp column.

**Dataset access date:** [Enter the actual date you accessed/downloaded the dataset.]

## 3. Project Structure

```text
Energy-Forecasting/
│
├── data/
│   ├── raw/
│   │   └── bdg2/
│   │       ├── electricity.csv
│   │       ├── weather.csv
│   │       └── metadata/
│   │           └── metadata.csv
│   │
│   └── cleaned/
│       ├── electricity.csv
│       ├── electricity_selected.csv
│       ├── final_forecasting_dataset.csv
│       └── energy_analysis.db
│
├── src/
│   ├── inspect_data.py
│   ├── dataset_statistics.py
│   ├── data_quality.py
│   ├── clean_data.py
│   ├── analyze_buildings.py
│   ├── prepare_electricity.py
│   ├── analyze_selected_data.py
│   ├── validate_timestamps.py
│   ├── inspect_building_metadata.py
│   ├── select_candidate_buildings.py
│   ├── inspect_candidate_building.py
│   ├── analyze_zero_readings.py
│   ├── analyze_temporal_patterns.py
│   ├── investigate_consumption_drop.py
│   ├── compare_robin_buildings.py
│   ├── screen_final_building.py
│   ├── inspect_final_candidate.py
│   ├── build_final_dataset.py
│   ├── validate_final_dataset.py
│   ├── train_models.py
│   ├── analyze_model_errors.py
│   ├── investigate_largest_error.py
│   ├── check_dst_anomaly.py
│   ├── test_saved_model.py
│   ├── build_sqlite_database.py
│   └── run_sql_analysis.py
│
├── notebooks/
├── tests/
│
├── outputs/
│   ├── figures/
│   └── reports/
│       └── sql_building_usage_analysis.csv
│
├── models/
│
├── sql/
│   └── building_usage_analysis.sql
│
├── docs/
│   ├── schema.md
│   ├── assumptions.md
│   └── exploration.md
│
├── requirements.txt
├── .gitignore
├── LICENSE
├── DATA_LICENSE
└── README.md
```

Raw data and generated model files may be excluded from Git because of their large size. The raw dataset must be downloaded separately.

## 4. Environment Setup

### Requirements

- Python 3.10 or later
- pip
- Git
- Visual Studio Code (recommended)

### Clone the repository

```bash
git clone https://github.com/mudassirmunir-dev/Energy-Forecasting.git
cd Energy-Forecasting
```

### Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Dataset setup

Download BDG2 from its official repository:

https://github.com/buds-lab/building-data-genome-project-2

Place the required files in the following locations:

```text
data/raw/bdg2/electricity.csv
data/raw/bdg2/weather.csv
data/raw/bdg2/metadata/metadata.csv
```

Raw data files must remain unchanged.

## 5. Data Processing Workflow

### Step 1: Inspect raw data

```powershell
python src/inspect_data.py
python src/dataset_statistics.py
```

These scripts inspect dataset structure, dimensions, and data types.

### Step 2: Analyze data quality

```powershell
python src/data_quality.py
```

This step examines missing values and data quality issues.

### Step 3: Clean electricity data

```powershell
python src/clean_data.py
```

The cleaning process removes completely empty building columns while preserving the original raw data.

### Step 4: Select buildings

```powershell
python src/analyze_buildings.py
python src/prepare_electricity.py
python src/analyze_selected_data.py
```

Buildings are screened according to missing-value percentages.

### Step 5: Validate timestamps and inspect metadata

```powershell
python src/validate_timestamps.py
python src/inspect_building_metadata.py
```

### Step 6: Explore consumption patterns

Run the relevant analysis scripts to examine:

- Building usage categories.
- Missing and zero readings.
- Electricity consumption over time.
- Hourly, daily, and monthly consumption patterns.
- Unusual consumption changes.

### Step 7: Prepare the forecasting dataset

```powershell
python src/screen_final_building.py
python src/inspect_final_candidate.py
python src/build_final_dataset.py
python src/validate_final_dataset.py
```

The initial forecasting candidate is **Hog_lodging_Shonda**, located at site Hog.

## 6. SQLite Database and SQL Analysis

SQLite was used to perform relational analysis between building electricity summaries and building metadata.

### Database

Database file:

```text
data/cleaned/energy_analysis.db
```

The database contains two tables:

| Table | Description | Records |
|---|---|---:|
| building_energy_summary | Total consumption, average consumption, and reading count for each building | 1,474 |
| building_metadata | Building identifiers, site information, primary space usage, and floor area | 1,636 |

All 1,474 energy summary records successfully matched building metadata records through `building_id`.

### SQL query

The SQL analysis joins both tables using `building_id` and groups buildings by their primary space usage category.

The query calculates:

- Number of buildings in each category.
- Average electricity consumption per building.
- Total electricity consumption per category.

The results are sorted by average consumption in descending order.

The SQL query is stored in:

```text
sql/building_usage_analysis.sql
```

### SQL query

```sql
SELECT
    m.primaryspaceusage AS building_usage,
    COUNT(*) AS building_count,
    ROUND(AVG(e.average_consumption), 2) AS average_consumption,
    ROUND(SUM(e.total_consumption), 2) AS total_consumption
FROM building_energy_summary AS e
INNER JOIN building_metadata AS m
    ON e.building_id = m.building_id
WHERE m.primaryspaceusage IS NOT NULL
GROUP BY m.primaryspaceusage
ORDER BY average_consumption DESC;
```

### Results and findings

The query successfully returned 16 building usage categories.

Top five categories by average electricity consumption:

| Building usage | Buildings | Average consumption |
|---|---:|---:|
| Healthcare | 26 | 292.98 |
| Education | 561 | 187.36 |
| Utility | 4 | 163.79 |
| Office | 282 | 137.20 |
| Technology/science | 6 | 121.86 |

Key findings:

- Healthcare had the highest average building consumption at 292.98 across 26 buildings.
- Education had an average building consumption of 187.36 across 561 buildings.
- Education recorded the largest total consumption, approximately 1.822 billion in the dataset's recorded units.
- Office buildings had an average consumption of 137.20 across 282 buildings.
- Lodging/residential buildings had an average consumption of 85.32 across 147 buildings.

These findings show differences in electricity consumption across building usage categories. The highest average does not necessarily mean the highest total consumption because categories contain different numbers of buildings.

**Interpretation note:** Average consumption represents the mean of the per-building average readings over the available period. It is not normalized by building floor area.

### Reproducing the SQLite analysis

Build the database:

```powershell
python src/build_sqlite_database.py
```

Execute the SQL analysis:

```powershell
python src/run_sql_analysis.py
```

The query results are saved to:

```text
outputs/reports/sql_building_usage_analysis.csv
```

## 7. Forecasting Problem

### Objective

Predict the next hour's electricity consumption using historical consumption, calendar information, and available weather observations.

**Problem type:** Supervised machine learning — Regression.

**Target:** `target`

**Selected building:** `Hog_lodging_Shonda`

**Target timestamp:** One hour after the input timestamp.

### Feature engineering

The forecasting dataset includes:

- Previous electricity consumption.
- Historical consumption lags.
- Rolling consumption averages.
- Hour, weekday, month, and weekend indicators.
- Weather measurements.
- Weather availability indicator.

The final forecasting dataset contains:

| Property | Value |
|---|---:|
| Rows | 17,376 |
| Columns | 19 |
| Input features | 16 |
| Target | 1 |

## 8. Model Training

The dataset is divided chronologically:

| Dataset | Rows | Percentage |
|---|---:|---:|
| Training | 13,900 | 80% |
| Testing | 3,476 | 20% |

A chronological split is used because the task involves time-series forecasting. The preprocessing pipeline is fitted using training data only.

### Models compared

1. Persistence baseline.
2. Random Forest Regressor.
3. HistGradientBoosting Regressor.

The preprocessing and model are combined using scikit-learn `Pipeline` and `ColumnTransformer`.

### Run training

```powershell
python src/train_models.py
```

## 9. Model Evaluation

The models are evaluated using:

- **MAE:** Mean Absolute Error.
- **RMSE:** Root Mean Squared Error.
- **R²:** Coefficient of Determination.

### Model comparison

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Persistence Baseline | 6.8035 | 9.5302 | 0.8365 |
| Random Forest | 5.1297 | 7.2785 | 0.9046 |
| HistGradientBoosting | **5.0928** | **7.2435** | **0.9055** |

HistGradientBoosting achieved the best results among the evaluated models.

It reduced MAE by approximately 25.1% compared with the persistence baseline.

## 10. Error Analysis

The model's prediction errors were examined using:

- Monthly error analysis.
- Hourly error analysis.
- Actual versus predicted plots.
- Prediction error distribution.
- Investigation of the largest prediction errors.

The largest observed error occurred around November 5, 2017, at 02:00, when actual consumption was 212 and predicted consumption was approximately 102.46.

The reason for this isolated spike remains unconfirmed.

## 11. Saved Model and Inference

The trained models are saved using Joblib.

```text
models/
├── random_forest.joblib
└── hist_gradient_boosting.joblib
```

To test the saved model:

```powershell
python src/test_saved_model.py
```

The script reloads the saved pipeline, recreates the chronological test split, generates predictions, and calculates evaluation metrics.

Predictions are saved to:

```text
outputs/reports/saved_model_predictions.csv
```

The saved model reproduced the original evaluation metrics:

- MAE: 5.0928
- RMSE: 7.2435
- R²: 0.9055

## 12. Visualizations

The project generates visualizations for electricity consumption, missing values, building usage, and forecasting performance.

Some important figures include:

- Electricity consumption over time.
- Weather missing-value distribution.
- Building usage distribution.
- Hourly, daily, and monthly consumption patterns.
- Actual versus predicted consumption.
- Prediction error distribution.
- Monthly prediction error.

Figures are stored in:

```text
outputs/figures/
```

## 13. Limitations and Assumptions

- The initial forecasting experiment focuses on one selected building.
- Some weather observations contain missing values.
- Missing weather features are handled by the fitted preprocessing pipeline.
- The cause of unusual consumption readings has not been conclusively established.
- The evaluation is one-step-ahead forecasting using actual recent consumption readings as historical inputs.
- This is not a recursive multi-hour forecasting experiment.
- Model performance on other buildings and sites has not yet been established.
- SQL category averages are not normalized by floor area.

Additional assumptions and risks are documented in `docs/assumptions.md`.

## 14. Reproducibility

The project stores code, cleaned outputs, figures, reports, SQL queries, and trained models separately.

Raw dataset files should remain unchanged.

To reproduce the workflow:

1. Set up the Python environment.
2. Download and place the required raw dataset files.
3. Execute the data processing scripts in the documented order.
4. Build the SQLite database and run the SQL analysis.
5. Prepare the forecasting dataset.
6. Train and evaluate the machine learning models.
7. Reload the saved model and verify its predictions.

Follow the commands in this README. The project does not currently provide a single command that runs every processing stage.

## 15. Acknowledgements

This project uses the Building Data Genome Project 2 dataset.

Dataset repository:

https://github.com/buds-lab/building-data-genome-project-2

The dataset is attributed to its original contributors and is used under the repository's CC BY-SA 4.0 license.

## 16. Licensing and Dataset Attribution

### Project Code

The original code in this repository is licensed under the MIT License.

### Dataset

This project uses the Building Data Genome Project 2 (BDG2).

Original dataset:

https://github.com/buds-lab/building-data-genome-project-2

Dataset license:

Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

The original dataset license is included in `DATA_LICENSE`.

The dataset remains subject to its original license.
