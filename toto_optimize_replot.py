import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_single_heatmap(pivot_data, title, metric, filename, figsize=(12, 8)):
    """Create a single large heatmap."""
    plt.figure(figsize=figsize)
    
    # Create heatmap
    sns.heatmap(pivot_data, 
                annot=True, 
                fmt='.1f' if metric != 'Net_Profit' else '.0f',
                cmap='RdYlGn',
                center=0,
                annot_kws={'size': 8},  # Increase annotation text size
                cbar_kws={'label': metric})
    
    plt.title(title, fontsize=14, pad=20)
    plt.xlabel('Lookback Period (draws)', fontsize=12)
    plt.ylabel('Least Weight', fontsize=12)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=0)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

def main():
    try:
        # Read the optimization results
        results_df = pd.read_csv('optimization_results.csv')
        
        # Create pivot tables for different metrics
        metrics = {
            'Average Profit per Draw ($)': 'Average_Profit',
            'Win Rate (%)': 'Win_Rate',
            'Total Net Profit ($)': 'Net_Profit'
        }
        
        # Plot each metric in a separate heatmap
        for title, metric in metrics.items():
            pivot_data = results_df.pivot(
                index='Least_Weight',
                columns='Lookback',
                values=metric
            )
            
            # Generate filename
            filename = f'toto_optimization_{metric.lower()}.png'
            
            # Create and save heatmap
            plot_single_heatmap(pivot_data, title, metric, filename)
            print(f"Generated {filename}")
        
        # Find and print best combinations
        best_avg_profit = results_df.loc[results_df['Average_Profit'].idxmax()]
        best_win_rate = results_df.loc[results_df['Win_Rate'].idxmax()]
        best_net_profit = results_df.loc[results_df['Net_Profit'].idxmax()]
        
        # Print summary
        print("\nOptimization Results Summary:")
        print("=" * 50)
        
        print(f"\nBest Average Profit per Draw:")
        print(f"Lookback Period: {best_avg_profit['Lookback']} draws")
        print(f"Least Weight: {best_avg_profit['Least_Weight']:.1f}")
        print(f"Average Profit: ${best_avg_profit['Average_Profit']:.2f}")
        print(f"Win Rate: {best_avg_profit['Win_Rate']:.2f}%")
        
        print(f"\nBest Win Rate:")
        print(f"Lookback Period: {best_win_rate['Lookback']} draws")
        print(f"Least Weight: {best_win_rate['Least_Weight']:.1f}")
        print(f"Win Rate: {best_win_rate['Win_Rate']:.2f}%")
        print(f"Average Profit: ${best_win_rate['Average_Profit']:.2f}")
        
        print(f"\nBest Total Net Profit:")
        print(f"Lookback Period: {best_net_profit['Lookback']} draws")
        print(f"Least Weight: {best_net_profit['Least_Weight']:.1f}")
        print(f"Net Profit: ${best_net_profit['Net_Profit']:.2f}")
        print(f"Average Profit: ${best_net_profit['Average_Profit']:.2f}")
        
    except FileNotFoundError:
        print("Error: optimization_results.csv file not found in the current directory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
