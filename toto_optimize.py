import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from toto_backtest import run_backtest
from toto_analyzer import read_toto_data

def test_parameters(data, lookback_range=(1, 20), lookback_step=1, 
                   weight_range=(0.1, 1), weight_step=0.1):
    """Test different combinations of lookback periods and least weights."""
    results = []
    
    lookbacks = np.arange(lookback_range[0], lookback_range[1] + 1, lookback_step)
    weights = np.arange(weight_range[0], weight_range[1] + 0.01, weight_step)
    
    total_combinations = len(lookbacks) * len(weights)
    current = 0
    
    for lookback in lookbacks:
        for least_weight in weights:
            current += 1
            print(f"Testing combination {current}/{total_combinations}: "
                  f"Lookback={lookback}, Least Weight={least_weight:.1f}")
            
            # Run backtest for this parameter combination
            backtest_results, total_cost, total_prize, wins = run_backtest(
                data, lookback, least_weight=least_weight)
            
            # Calculate metrics
            avg_profit = (total_prize - total_cost) / len(backtest_results) if backtest_results else 0
            win_rate = (wins / len(backtest_results) * 100) if backtest_results else 0
            
            result = {
                'Lookback': lookback,
                'Least_Weight': least_weight,
                'Average_Profit': avg_profit,
                'Win_Rate': win_rate,
                'Total_Draws': len(backtest_results),
                'Total_Wins': wins,
                'Total_Cost': total_cost,
                'Total_Prize': total_prize,
                'Net_Profit': total_prize - total_cost
            }
            results.append(result)
    
    return pd.DataFrame(results)

def plot_heatmaps(results_df):
    """Create heatmap visualizations of the results."""
    # Create pivot tables for different metrics
    metrics = {
        'Average Profit per Draw ($)': 'Average_Profit',
        'Win Rate (%)': 'Win_Rate',
        'Total Net Profit ($)': 'Net_Profit'
    }
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle('TOTO Strategy Analysis: Impact of Parameters', fontsize=16, y=1.05)
    
    for idx, (title, metric) in enumerate(metrics.items()):
        pivot_data = results_df.pivot(
            index='Least_Weight',
            columns='Lookback',
            values=metric
        )
        
        # Create heatmap
        sns.heatmap(pivot_data, 
                   annot=True, 
                   fmt='.1f' if metric != 'Net_Profit' else '.0f',
                   cmap='RdYlGn',
                   center=0,
                   ax=axes[idx])
        
        axes[idx].set_title(title)
        axes[idx].set_xlabel('Lookback Period (draws)')
        axes[idx].set_ylabel('Least Weight')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('toto_optimization_heatmaps.png', bbox_inches='tight', dpi=300)
    plt.close()

def main():
    try:
        # Read the data
        data = read_toto_data('ToTo.csv')
        
        print("Testing parameter combinations...")
        print("-" * 50)
        
        # Test parameter combinations
        results_df = test_parameters(data)
        
        # Create visualizations
        plot_heatmaps(results_df)
        
        # Find best performing combinations
        best_avg_profit = results_df.loc[results_df['Average_Profit'].idxmax()]
        best_win_rate = results_df.loc[results_df['Win_Rate'].idxmax()]
        best_net_profit = results_df.loc[results_df['Net_Profit'].idxmax()]
        
        # Print summary
        print("\nOptimization Results:")
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
        
        print("\nResults have been saved to 'toto_optimization_heatmaps.png'")
        
        # Save results to CSV for further analysis
        results_df.to_csv('optimization_results.csv', index=False)
        print("Detailed results have been saved to 'optimization_results.csv'")
        
    except FileNotFoundError:
        print("Error: ToTo.csv file not found in the current directory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 