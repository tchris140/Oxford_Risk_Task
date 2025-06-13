import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

def load_and_prepare_data():
    """Load and prepare data for correlation analysis"""
    print("Loading datasets...")
    personality_df = pd.read_csv('csv_files/personality.csv')
    assets_df = pd.read_csv('csv_files/assets_gbp.csv')
    
    # Calculate total assets per person
    total_assets = assets_df.groupby('_id')['asset_value_gbp'].sum().reset_index()
    total_assets.columns = ['_id', 'total_assets_gbp']
    
    # Merge with personality data
    combined_df = pd.merge(personality_df, total_assets, on='_id', how='inner')
    
    return combined_df, assets_df

def analyze_correlations(combined_df):
    """Analyze correlations between personality traits and total assets"""
    print("\nAnalyzing correlations between personality traits and total assets...")
    
    # Select numeric columns for correlation
    numeric_cols = ['confidence', 'risk_tolerance', 'composure', 'impulsivity', 
                   'impact_desire', 'total_assets_gbp']
    
    # Calculate correlation matrix
    corr_matrix = combined_df[numeric_cols].corr()
    
    # Create visualization directory
    viz_dir = 'visualizations'
    if not os.path.exists(viz_dir):
        os.makedirs(viz_dir)
    
    # Plot correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix of Personality Traits and Total Assets')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'correlation_heatmap.png'))
    plt.close()
    
    # Print correlation with total assets
    print("\nCorrelations with Total Assets (GBP):")
    asset_correlations = corr_matrix['total_assets_gbp'].sort_values(ascending=False)
    print(asset_correlations)
    
    return corr_matrix

# def analyze_asset_allocation_trends(assets_df):
#     """Analyze trends in asset allocation"""
#     print("\nAnalyzing asset allocation trends...")
    
#     # Create visualization directory
#     viz_dir = 'visualizations(1)'
#     if not os.path.exists(viz_dir):
#         os.makedirs(viz_dir)
    
#     # Calculate total value and count by asset class
#     allocation_stats = assets_df.groupby('asset_allocation').agg({
#         'asset_value_gbp': ['sum', 'count', 'mean']
#     }).round(2)
    
#     allocation_stats.columns = ['Total Value (GBP)', 'Count', 'Mean Value (GBP)']
#     print("\nAsset Allocation Statistics:")
#     print(allocation_stats)
    
#     # Plot total value by asset class
#     plt.figure(figsize=(12, 6))
#     sns.barplot(data=allocation_stats.reset_index(), 
#                 x='asset_allocation', 
#                 y='Total Value (GBP)')
#     plt.title('Total Asset Value by Asset Class')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.savefig(os.path.join(viz_dir, 'total_value_by_asset_class.png'))
#     plt.close()

def analyze_personality_distributions(combined_df):
    """Analyze distributions of personality traits"""
    print("\nAnalyzing personality trait distributions...")
    
    # Create visualization directory
    viz_dir = 'visualizations'
    if not os.path.exists(viz_dir):
        os.makedirs(viz_dir)
    
    # Create pairplot of personality traits
    personality_traits = ['confidence', 'risk_tolerance', 'composure', 
                         'impulsivity', 'impact_desire']
    
    plt.figure(figsize=(15, 10))
    sns.pairplot(combined_df[personality_traits])
    plt.savefig(os.path.join(viz_dir, 'personality_traits_pairplot.png'))
    plt.close()
    
    # Calculate basic statistics
    print("\nPersonality Trait Statistics:")
    stats_df = combined_df[personality_traits].describe()
    print(stats_df)
    
    return stats_df

def analyze_risk_tolerance_patterns(combined_df):
    """Analyze patterns in risk tolerance"""
    print("\nAnalyzing risk tolerance patterns...")
    
    # Create visualization directory
    viz_dir = 'visualizations'
    if not os.path.exists(viz_dir):
        os.makedirs(viz_dir)
    
    # Create scatter plots of risk tolerance vs other traits
    traits = ['confidence', 'composure', 'impulsivity', 'impact_desire']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.ravel()
    
    for idx, trait in enumerate(traits):
        sns.scatterplot(data=combined_df, 
                       x='risk_tolerance', 
                       y=trait, 
                       ax=axes[idx])
        axes[idx].set_title(f'Risk Tolerance vs {trait.capitalize()}')
    
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'risk_tolerance_correlations.png'))
    plt.close()
    
    # Calculate correlations with risk tolerance
    risk_correlations = combined_df[['risk_tolerance'] + traits].corr()['risk_tolerance']
    print("\nCorrelations with Risk Tolerance:")
    print(risk_correlations)

def main():
    # Load and prepare data
    combined_df, assets_df = load_and_prepare_data()
    
    # Perform analyses
    corr_matrix = analyze_correlations(combined_df)
    # analyze_asset_allocation_trends(assets_df)
    personality_stats = analyze_personality_distributions(combined_df)
    analyze_risk_tolerance_patterns(combined_df)
    
    print("\nAnalysis complete! Check the visualizations folder for plots.")

if __name__ == "__main__":
    main() 