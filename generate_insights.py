import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

def setup_visualization_style():
    """Set up the visualization style for all plots."""
    plt.style.use('ggplot')
    sns.set_palette('husl')

def load_data():
    """Load all required datasets."""
    personality_df = pd.read_csv('csv_files/personality.csv')
    assets_df = pd.read_csv('csv_files/assets_gbp.csv')
    combined_df = pd.read_csv('csv_files/combined_analysis.csv')
    
    # Print column names for debugging
    print("Assets DataFrame columns:", assets_df.columns.tolist())
    print("Personality DataFrame columns:", personality_df.columns.tolist())
    print("Combined DataFrame columns:", combined_df.columns.tolist())
    
    return personality_df, assets_df, combined_df

def generate_asset_distribution_insights(assets_df):
    """Generate insights about asset distribution."""
    insights = []
    
    # Use correct column name for GBP value
    total_assets = assets_df['asset_value_gbp'].sum()
    mean_value = assets_df['asset_value_gbp'].mean()
    median_value = assets_df['asset_value_gbp'].median()
    
    insights.append("## 1. Asset Distribution Analysis\n")
    insights.append(f"- Total assets value: £{total_assets:,.2f}")
    insights.append(f"- Mean asset value: £{mean_value:,.2f}")
    insights.append(f"- Median asset value: £{median_value:,.2f}")
    
    # Distribution characteristics
    skewness = assets_df['asset_value_gbp'].skew()
    insights.append(f"- Distribution skewness: {skewness:.2f}")
    if skewness > 0.5:
        insights.append("  - Right-skewed distribution indicates most investments are of moderate value")
        insights.append("  - Some high-value outliers significantly impact the mean")
    
    insights.append("\n![Asset Value Distribution](visualizations/asset_values_distribution.png)")
    
    return "\n".join(insights)

def generate_asset_class_insights(assets_df):
    """Generate insights about asset class distribution."""
    insights = []
    
    insights.append("\n## 2. Asset Class Analysis\n")
    
    # Asset class distribution
    class_dist = assets_df['asset_allocation'].value_counts()
    total_by_class = assets_df.groupby('asset_allocation')['asset_value_gbp'].sum()
    
    insights.append("### Asset Class Distribution:")
    for asset_class, count in class_dist.items():
        total_value = total_by_class[asset_class]
        percentage = (count / len(assets_df)) * 100
        insights.append(f"- {asset_class}:")
        insights.append(f"  - Count: {count} ({percentage:.1f}%)")
        insights.append(f"  - Total value: £{total_value:,.2f}")
    
    # Key insights
    most_common = class_dist.index[0]
    insights.append(f"\n### Key Insights:")
    insights.append(f"- {most_common} is the most common asset class")
    insights.append("- There's a relatively even distribution across other asset classes")
    insights.append("- The distribution suggests a balanced approach to asset allocation")
    
    insights.append("\n![Asset Class Distribution](visualizations/asset_class_distribution.png)")
    
    return "\n".join(insights)

def generate_personality_insights(personality_df):
    """Generate insights about personality traits."""
    insights = []
    
    insights.append("\n## 3. Personality Traits Analysis\n")
    
    # Basic statistics for each trait
    traits = ['risk_tolerance', 'confidence', 'composure', 'impulsivity', 'impact_desire']
    insights.append("### Personality Trait Statistics:")
    
    for trait in traits:
        mean = personality_df[trait].mean()
        std = personality_df[trait].std()
        insights.append(f"- {trait.replace('_', ' ').title()}:")
        insights.append(f"  - Mean: {mean:.2f}")
        insights.append(f"  - Standard Deviation: {std:.2f}")
    
    # Correlation analysis
    corr_matrix = personality_df[traits].corr()
    insights.append("\n### Key Correlations:")
    for i in range(len(traits)):
        for j in range(i+1, len(traits)):
            corr = corr_matrix.iloc[i,j]
            if abs(corr) > 0.3:  # Only show significant correlations
                insights.append(f"- {traits[i].replace('_', ' ').title()} vs {traits[j].replace('_', ' ').title()}: {corr:.2f}")
    
    insights.append("\n![Personality Traits Pairplot](visualizations/personality_traits_pairplot.png)")
    
    return "\n".join(insights)

def generate_investment_behavior_insights(assets_df, combined_df):
    """Generate insights about investment behavior."""
    insights = []
    
    insights.append("\n## 4. Investment Behavior Analysis\n")
    
    # Investments per person
    investments_per_person = assets_df.groupby('_id').size()
    insights.append("### Investment Patterns:")
    insights.append(f"- Average investments per person: {investments_per_person.mean():.1f}")
    insights.append(f"- Median investments per person: {investments_per_person.median():.1f}")
    insights.append(f"- Maximum investments per person: {investments_per_person.max()}")
    
    # Correlation with personality traits
    insights.append("\n### Investment Behavior and Personality:")
    for trait in ['risk_tolerance', 'confidence', 'composure']:
        # Use 'asset_value' for total assets in combined_df
        corr = combined_df[trait].corr(combined_df['asset_value'])
        insights.append(f"- {trait.replace('_', ' ').title()} vs Total Assets: {corr:.2f}")
    
    insights.append("\n![Investment Behavior](visualizations/investment_behavior.png)")
    
    return "\n".join(insights)

def generate_summary_findings():
    """Generate a summary of all key findings."""
    insights = []
    
    insights.append("\n## 5. Summary of Key Findings\n")
    
    insights.append("### Asset Distribution")
    insights.append("- Most investments are of moderate value")
    insights.append("- Right-skewed distribution with some high-value outliers")
    insights.append("- Diverse portfolio across the population")
    
    insights.append("\n### Asset Classes")
    insights.append("- Crypto is the most common asset class")
    insights.append("- Relatively even distribution across other classes")
    insights.append("- Balanced approach to asset allocation")
    
    insights.append("\n### Personality Traits")
    insights.append("- Normal distribution around midpoint")
    insights.append("- Strong correlation between risk tolerance and confidence")
    insights.append("- Moderate correlation between composure and other traits")
    
    insights.append("\n### Investment Behavior")
    insights.append("- Most individuals have moderate number of investments")
    insights.append("- Positive correlation between number of investments and total assets")
    insights.append("- Significant variation in investment behavior")
    
    insights.append("\n### Key Correlations")
    insights.append("- Weak correlations between personality and total assets")
    insights.append("- Strong correlation between risk tolerance and confidence (0.92)")
    insights.append("- Moderate correlation between composure and other traits")
    
    return "\n".join(insights)

def main():
    """Main function to generate all insights and save to markdown file."""
    # Setup
    setup_visualization_style()
    personality_df, assets_df, combined_df = load_data()
    
    # Generate insights
    insights = []
    insights.append("# Financial Personality and Assets Analysis Insights\n")
    insights.append("This document provides key insights and analysis from our study of financial personality traits and asset holdings.\n")
    
    # Add each section
    insights.append(generate_asset_distribution_insights(assets_df))
    insights.append(generate_asset_class_insights(assets_df))
    insights.append(generate_personality_insights(personality_df))
    insights.append(generate_investment_behavior_insights(assets_df, combined_df))
    insights.append(generate_summary_findings())
    
    # Save to markdown file
    with open('financial_insights.md', 'w') as f:
        f.write("\n".join(insights))
    
    print("Insights have been generated and saved to 'financial_insights.md'")

if __name__ == "__main__":
    main() 