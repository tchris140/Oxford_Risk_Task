import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple
import os

# Constants
PERSONALITY_DATA_URL = "https://raw.githubusercontent.com/karwester/behavioural-finance-task/refs/heads/main/personality.csv"
SUPABASE_URL = "https://pvgaaikztozwlfhyrqlo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2Z2FhaWt6dG96d2xmaHlycWxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4NDE2MjUsImV4cCI6MjA2MzQxNzYyNX0.iAqMXnJ_sJuBMtA6FPNCRcYnKw95YkJvY3OhCIZ77vI"

def get_viz_dir():
    viz_dir = 'visualizations'
    if not os.path.exists(viz_dir):
        os.makedirs(viz_dir)
    return viz_dir

def load_personality_data() -> pd.DataFrame:
    """
    Load personality data from CSV file.
    Returns a pandas DataFrame containing the personality data.
    """
    df = pd.read_csv('csv_files/personality.csv')
    return df

def load_assets_data() -> pd.DataFrame:
    """
    Load assets data from CSV file.
    Returns a pandas DataFrame containing the assets data.
    """
    df = pd.read_csv('csv_files/assets.csv')
    return df

def find_highest_gbp_assets(personality_df: pd.DataFrame, assets_df: pd.DataFrame) -> Tuple[float, float]:
    """
    Find the person with the highest total assets in GBP and their risk tolerance.
    Returns a tuple of (highest_gbp_assets, risk_tolerance).
    """
    # Filter for GBP assets only
    gbp_assets = assets_df[assets_df['asset_currency'] == 'GBP']
    
    # Group by _id and sum asset_value
    total_gbp_assets = gbp_assets.groupby('_id')['asset_value'].sum()
    
    # Find person with highest GBP assets
    highest_gbp_person_id = total_gbp_assets.idxmax()
    highest_gbp_amount = total_gbp_assets.max()
    
    # Get their risk tolerance
    risk_tolerance = personality_df[personality_df['_id'] == highest_gbp_person_id]['risk_tolerance'].iloc[0]
    
    return highest_gbp_amount, risk_tolerance

def analyze_assets_distribution(assets_df: pd.DataFrame) -> None:
    """
    Create visualizations for assets distribution analysis.
    """
    viz_dir = get_viz_dir()
    
    # Convert to GBP
    exchange_rates = {
        'GBP': 1.0,
        'USD': 0.79,
        'EUR': 0.86,
        'JPY': 0.0053,
        'AUD': 0.52
    }
    assets_df_gbp = assets_df.copy()
    assets_df_gbp['asset_value_gbp'] = assets_df_gbp.apply(
        lambda row: row['asset_value'] * exchange_rates[row['asset_currency']], 
        axis=1
    )
    
    # Create combined visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Total value by currency
    currency_totals = assets_df_gbp.groupby('asset_currency')['asset_value_gbp'].sum().reset_index()
    currency_totals = currency_totals.sort_values('asset_value_gbp', ascending=False)
    sns.barplot(x='asset_currency', y='asset_value_gbp', data=currency_totals, ax=ax1)
    ax1.set_title('Total Asset Value by Currency (GBP)')
    ax1.set_xlabel('Currency')
    ax1.set_ylabel('Total Value (GBP)')
    
    # Value distribution by currency
    sns.boxplot(x='asset_currency', y='asset_value_gbp', data=assets_df_gbp, ax=ax2)
    ax2.set_title('Asset Value Distribution by Currency (GBP)')
    ax2.set_xlabel('Currency')
    ax2.set_ylabel('Asset Value (GBP)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'assets_distribution.png'))
    plt.close()

def analyze_asset_classes(assets_df: pd.DataFrame) -> None:
    """
    Create visualizations for asset class analysis.
    """
    viz_dir = get_viz_dir()
    
    # Convert to GBP
    exchange_rates = {
        'GBP': 1.0,
        'USD': 0.79,
        'EUR': 0.86,
        'JPY': 0.0053,
        'AUD': 0.52
    }
    assets_df_gbp = assets_df.copy()
    assets_df_gbp['asset_value_gbp'] = assets_df_gbp.apply(
        lambda row: row['asset_value'] * exchange_rates[row['asset_currency']],
        axis=1
    )
    
    # Create combined visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Total value by asset class
    asset_class_totals = assets_df_gbp.groupby('asset_allocation')['asset_value_gbp'].sum().reset_index()
    asset_class_totals = asset_class_totals.sort_values('asset_value_gbp', ascending=False)
    sns.barplot(x='asset_allocation', y='asset_value_gbp', data=asset_class_totals, ax=ax1)
    ax1.set_title('Total Asset Value by Asset Class (GBP)')
    ax1.set_xlabel('Asset Class')
    ax1.set_ylabel('Total Value (GBP)')
    ax1.tick_params(axis='x', labelrotation=45)
    
    # Value distribution by asset class
    sns.boxplot(x='asset_allocation', y='asset_value_gbp', data=assets_df_gbp, ax=ax2)
    ax2.set_title('Asset Value Distribution by Asset Class (GBP)')
    ax2.set_xlabel('Asset Class')
    ax2.set_ylabel('Asset Value (GBP)')
    ax2.tick_params(axis='x', labelrotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'asset_classes_distribution.png'))
    plt.close()

def analyze_personality_traits(personality_df: pd.DataFrame, assets_df: pd.DataFrame) -> None:
    """
    Create visualizations for personality trait analysis.
    """
    viz_dir = get_viz_dir()
    
    # Convert assets to GBP
    exchange_rates = {
        'GBP': 1.0,
        'USD': 0.79,
        'EUR': 0.86,
        'JPY': 0.0053,
        'AUD': 0.52
    }
    assets_df_gbp = assets_df.copy()
    assets_df_gbp['asset_value_gbp'] = assets_df_gbp.apply(
        lambda row: row['asset_value'] * exchange_rates[row['asset_currency']],
        axis=1
    )
    total_assets_by_id = assets_df_gbp.groupby('_id')['asset_value_gbp'].sum().reset_index()
    
    # Create combined visualization for all personality traits
    traits = ['risk_tolerance', 'confidence', 'composure', 'impulsivity', 'impact_desire']
    fig, axes = plt.subplots(len(traits), 2, figsize=(14, 20))
    
    for idx, trait in enumerate(traits):
        combined_data = pd.merge(
            total_assets_by_id,
            personality_df[['_id', trait]],
            on='_id',
            how='inner'
        )
        # Distribution of trait
        sns.histplot(data=personality_df, x=trait, bins=30, ax=axes[idx, 0])
        axes[idx, 0].set_title(f'Distribution of {trait.replace("_", " ").title()}')
        axes[idx, 0].set_xlabel(trait.replace("_", " ").title())
        axes[idx, 0].set_ylabel('Count')
        # Scatter plot vs total assets
        sns.scatterplot(data=combined_data, x=trait, y='asset_value_gbp', ax=axes[idx, 1])
        axes[idx, 1].set_title(f'{trait.replace("_", " ").title()} vs Total Assets')
        axes[idx, 1].set_xlabel(trait.replace("_", " ").title())
        axes[idx, 1].set_ylabel('Total Assets (GBP)')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'personality_traits_analysis.png'))
    plt.close()

def analyze_personality_vs_num_investments(personality_df: pd.DataFrame, assets_df: pd.DataFrame) -> None:
    """
    Create visualizations comparing personality traits to the number of investments per individual.
    """
    viz_dir = get_viz_dir()
    # Count number of investments per individual
    num_investments = assets_df.groupby('_id').size().reset_index(name='num_investments')
    # Merge with personality data
    merged = pd.merge(personality_df, num_investments, on='_id', how='inner')
    traits = ['risk_tolerance', 'confidence', 'composure', 'impulsivity', 'impact_desire']
    
    # Create a 2x3 grid layout (5 traits + 1 empty space)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()  # Flatten the 2D array of axes for easier indexing
    
    for idx, trait in enumerate(traits):
        # Scatter plot: trait vs num_investments
        sns.scatterplot(data=merged, x=trait, y='num_investments', ax=axes[idx])
        axes[idx].set_title(f'{trait.replace("_", " ").title()} vs Number of Investments')
        axes[idx].set_xlabel(trait.replace("_", " ").title())
        axes[idx].set_ylabel('Number of Investments')
    
    # Remove the last unused subplot
    fig.delaxes(axes[-1])
    
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'personality_vs_num_investments.png'))
    plt.close()

def main():
    # Load data
    print("Loading personality data...")
    personality_df = load_personality_data()
    
    print("Loading assets data...")
    assets_df = load_assets_data()
    
    # Find highest GBP assets and risk tolerance
    highest_gbp_amount, risk_tolerance = find_highest_gbp_assets(personality_df, assets_df)
    print(f"\nHighest GBP assets: £{highest_gbp_amount:,.2f}")
    print(f"Risk tolerance of person with highest GBP assets: {risk_tolerance:.2f}")
    
    # Perform analysis
    print("\nAnalyzing assets distribution...")
    analyze_assets_distribution(assets_df)
    
    print("Analyzing asset classes...")
    analyze_asset_classes(assets_df)
    
    print("Analyzing personality traits...")
    analyze_personality_traits(personality_df, assets_df)
    
    print("Analyzing personality traits vs number of investments...")
    analyze_personality_vs_num_investments(personality_df, assets_df)

if __name__ == "__main__":
    main() 