# Financial Personality and Assets Analysis

This project analyzes the relationship between financial personality traits and asset holdings using two datasets:
1. Financial Personality data (CSV)
2. Financial Assets data (Supabase API)

## Project Structure

```
Oxford_Risk_Task/
├── csv_files/              # Directory containing all CSV data files
│   ├── personality.csv     # Personality trait data
│   ├── assets.csv         # Raw assets data
│   ├── assets_gbp.csv     # Assets data converted to GBP
│   └── combined_analysis.csv  # Merged dataset for analysis
├── visualizations/         # Directory containing all generated visualizations
├── download_datasets.py    # Script to download and prepare datasets
├── data_quality_check.py   # Script for data quality analysis
├── financial_analysis.py   # Script for financial analysis
├── correlation_analysis.py # Script for correlation analysis
└── requirements.txt        # Python package dependencies
```

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Download the datasets:
```bash
python download_datasets.py
```

## Analysis Scripts

### 1. Data Quality Check (`data_quality_check.py`)
- Converts all asset values to GBP
- Performs data quality checks:
  - Missing values analysis
  - Duplicate detection
  - Numeric range analysis
  - Categorical value analysis
- Generates visualizations:
  - Asset value distribution
  - Asset values by currency
  - Asset class distribution

### 2. Financial Analysis (`financial_analysis.py`)
- Analyzes asset distributions and personality traits
- Generates visualizations:
  - Asset distribution by currency
  - Asset class analysis
  - Personality traits vs total assets
  - Personality traits vs number of investments

### 3. Correlation Analysis (`correlation_analysis.py`)
- Analyzes correlations between personality traits and financial metrics
- Generates visualizations:
  - Correlation heatmap
  - Personality traits pairplot
  - Risk tolerance correlations

## Key Features

1. **Currency Standardization**
   - All asset values are converted to GBP for consistent analysis
   - Exchange rates are maintained for USD, EUR, JPY, and AUD

2. **Personality Traits Analysis**
   - Risk tolerance
   - Confidence
   - Composure
   - Impulsivity
   - Impact desire

3. **Asset Analysis**
   - Asset class distribution
   - Currency distribution
   - Value distribution
   - Investment count per individual

4. **Correlation Analysis**
   - Personality traits vs total assets
   - Personality traits vs number of investments
   - Inter-trait correlations

## Output Files

### CSV Files
- `assets_gbp.csv`: Assets data with values converted to GBP
- `combined_analysis.csv`: Merged dataset for comprehensive analysis

### Visualizations
All visualizations are saved in the `visualizations/` directory:
- Data quality visualizations
- Financial analysis plots
- Correlation analysis plots
- Personality trait distributions
- Asset allocation patterns

## Usage

1. First, download the datasets:
```bash
python download_datasets.py
```

2. Run the data quality check:
```bash
python data_quality_check.py
```

3. Perform financial analysis:
```bash
python financial_analysis.py
```

4. Run correlation analysis:
```bash
python correlation_analysis.py
```

## Dependencies

- pandas >= 1.3.0
- numpy >= 1.20.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0
- requests >= 2.26.0
- scipy >= 1.7.0

## Notes

- All monetary values are standardized to GBP
- Visualizations are automatically saved in the `visualizations/` directory
- Data files are stored in the `csv_files/` directory
- The analysis includes both individual trait analysis and correlation studies 