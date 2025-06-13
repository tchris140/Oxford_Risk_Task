import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def load_datasets():
    print("Loading datasets...")
    personality_df = pd.read_csv('csv_files/personality.csv')
    assets_df = pd.read_csv('csv_files/assets.csv')
    return personality_df, assets_df

def convert_to_gbp(assets_df):
    print("\nConverting asset values to GBP...")
    # Define exchange rates (as of March 2024)
    exchange_rates = {
        'USD': 0.79,  # 1 USD = 0.79 GBP
        'EUR': 0.85,  # 1 EUR = 0.85 GBP
        'JPY': 0.0052,  # 1 JPY = 0.0052 GBP
        'AUD': 0.52,  # 1 AUD = 0.52 GBP
        'GBP': 1.0    # 1 GBP = 1 GBP
    }
    
    # Create a new column for GBP values
    assets_df['asset_value_gbp'] = assets_df.apply(
        lambda row: row['asset_value'] * exchange_rates[row['asset_currency']], 
        axis=1
    )
    
    return assets_df

def check_missing_values(df, dataset_name):
    print(f"\n=== Missing Values in {dataset_name} ===")
    missing_values = df.isnull().sum()
    missing_percentage = (missing_values / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Values': missing_values,
        'Percentage': missing_percentage
    })
    missing_df = missing_df[missing_df['Missing Values'] > 0]
    
    if missing_df.empty:
        print("No missing values found!")
    else:
        print(missing_df)

def check_duplicates(df, dataset_name):
    print(f"\n=== Duplicate Rows in {dataset_name} ===")
    duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}")

def check_numeric_ranges(df, dataset_name):
    print(f"\n=== Numeric Value Ranges in {dataset_name} ===")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        print(f"\n{col}:")
        print(f"Min: {df[col].min():.2f}")
        print(f"Max: {df[col].max():.2f}")
        print(f"Mean: {df[col].mean():.2f}")
        print(f"Median: {df[col].median():.2f}")
        print(f"Standard Deviation: {df[col].std():.2f}")
        
        # Calculate outliers using IQR method
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        
        print(f"Number of outliers: {len(outliers)}")
        if len(outliers) > 0:
            print(f"Outlier values: {outliers.values}")

def check_categorical_values(df, dataset_name):
    print(f"\n=== Categorical Values in {dataset_name} ===")
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    for col in categorical_cols:
        print(f"\n{col}:")
        value_counts = df[col].value_counts()
        print("Value counts:")
        print(value_counts)
        print(f"Number of unique values: {df[col].nunique()}")

def plot_asset_distributions(assets_df):
    print("\nCreating data quality visualizations...")
    
    # Create visualizations directory if it doesn't exist
    viz_dir = 'visualizations'
    if not os.path.exists(viz_dir):
        os.makedirs(viz_dir)
    
    # Set style
    plt.style.use('ggplot')
    
    # 1. Asset Value Distribution (for outlier detection)
    plt.figure(figsize=(12, 6))
    sns.histplot(data=assets_df, x='asset_value_gbp', bins=30)
    plt.title('Distribution of Asset Values (GBP) - Data Quality Check')
    plt.xlabel('Asset Value (GBP)')
    plt.ylabel('Count')
    plt.savefig(os.path.join(viz_dir, 'asset_values_distribution.png'))
    plt.close()
    
    # 2. Asset Value by Currency (for currency balance check)
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=assets_df, x='asset_currency', y='asset_value_gbp')
    plt.title('Asset Values by Currency (GBP) - Data Quality Check')
    plt.xlabel('Currency')
    plt.ylabel('Asset Value (GBP)')
    plt.savefig(os.path.join(viz_dir, 'asset_values_by_currency.png'))
    plt.close()
    
    # 3. Asset Class Distribution (for class balance check)
    plt.figure(figsize=(10, 6))
    asset_counts = assets_df['asset_allocation'].value_counts()
    sns.barplot(x=asset_counts.index, y=asset_counts.values)
    plt.title('Distribution of Asset Classes - Data Quality Check')
    plt.xlabel('Asset Class')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'asset_class_distribution.png'))
    plt.close()

def analyze_currency_statistics(assets_df):
    print("\n=== Assets Data Currency Analysis (in GBP) ===")
    currency_stats = assets_df.groupby('asset_currency')['asset_value_gbp'].agg(['count', 'mean', 'std', 'min', 'max'])
    print("\nCurrency Statistics (in GBP):")
    print(currency_stats)

def analyze_asset_allocation(assets_df):
    print("\n=== Assets Data Allocation Analysis (in GBP) ===")
    allocation_stats = assets_df.groupby('asset_allocation')['asset_value_gbp'].agg(['count', 'mean', 'std', 'min', 'max'])
    print("\nAsset Allocation Statistics (in GBP):")
    print(allocation_stats)

def main():
    # Load datasets
    personality_df, assets_df = load_datasets()
    
    # Convert asset values to GBP
    assets_df = convert_to_gbp(assets_df)
    
    # Save GBP-converted data
    assets_df.to_csv('csv_files/assets_gbp.csv', index=False)
    print("\nSaved GBP-converted assets data to csv_files/assets_gbp.csv")
    
    # Analyze personality data
    print("\n=== Personality Data Analysis ===")
    check_missing_values(personality_df, "Personality Data")
    check_duplicates(personality_df, "Personality Data")
    check_numeric_ranges(personality_df, "Personality Data")
    
    # Analyze assets data
    print("\n=== Assets Data Analysis (in GBP) ===")
    check_missing_values(assets_df, "Assets Data")
    check_duplicates(assets_df, "Assets Data")
    check_numeric_ranges(assets_df, "Assets Data")
    check_categorical_values(assets_df, "Assets Data")
    
    # Analyze currency and allocation statistics
    analyze_currency_statistics(assets_df)
    analyze_asset_allocation(assets_df)
    
    # Create visualizations
    plot_asset_distributions(assets_df)

if __name__ == "__main__":
    main() 