import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from toto_backtest import run_backtest
from toto_analyzer import read_toto_data

def analyze_yearly_trends(data, lookback_periods=[1, 2, 3, 5, 7], least_weights=[0.5]):
    """Analyze win rate trends by year for different parameter combinations."""
    # Convert date to datetime
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
    
    results = []
    
    # Test each combination
    for lookback in lookback_periods:
        for weight in least_weights:
            print(f"Processing: Lookback={lookback}, Weight={weight}")
            
            # Run backtest
            backtest_results, _, _, _ = run_backtest(data, lookback, least_weight=weight)
            
            # Convert results to DataFrame
            df_results = pd.DataFrame(backtest_results)
            df_results['Date'] = pd.to_datetime(df_results['Date'], format='%d/%m/%Y')
            df_results['Year'] = df_results['Date'].dt.year
            df_results['Win'] = df_results['Prize'] > 0
            
            # Calculate yearly win rates and win counts
            yearly_stats = df_results.groupby('Year').agg({
                'Win': ['mean', 'sum', 'count']
            }).reset_index()
            yearly_stats.columns = ['Year', 'win_rate', 'win_count', 'total_count']
            yearly_stats['win_rate'] = yearly_stats['win_rate'] * 100
            
            # Store results
            results.append({
                'lookback': lookback,
                'weight': weight,
                'years': yearly_stats['Year'],
                'win_rates': yearly_stats['win_rate'],
                'win_counts': yearly_stats['win_count'],
                'total_counts': yearly_stats['total_count']
            })
    
    return results

def plot_yearly_trends(results):
    """Create subplots showing yearly win rates and win counts for all configurations."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), height_ratios=[1, 1])
    
    # Get unique years across all results
    all_years = sorted(list(set(year for r in results for year in r['years'])))
    
    # Calculate bar positions
    n_configs = len(results)
    bar_width = 0.8 / n_configs
    
    # Plot win rates (top subplot)
    for i, result in enumerate(results):
        x_positions = np.arange(len(all_years)) + (i * bar_width) - (bar_width * (n_configs-1)/2)
        
        # Create a mask for years present in this result
        mask = [year in result['years'].values for year in all_years]
        win_rates = [result['win_rates'].values[result['years'] == year][0] if year in result['years'].values else 0 for year in all_years]
        
        ax1.bar(x_positions[mask], 
                [w for m, w in zip(mask, win_rates) if m],
                width=bar_width,
                label=f"Lookback={result['lookback']}, Weight={result['weight']:.1f}",
                alpha=0.8)
    
    ax1.set_title('Yearly Win Rates by Strategy Configuration', fontsize=14, pad=20)
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Win Rate (%)', fontsize=12)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Set x-axis ticks to years
    ax1.set_xticks(range(len(all_years)))
    ax1.set_xticklabels(all_years, rotation=45)
    
    # Add horizontal line for random guess win rate
    ax1.axhline(y=2.179, color='r', linestyle='--', alpha=0.5, 
                label='Random Guess (2.179%)')
    
    # Plot win counts (bottom subplot)
    for i, result in enumerate(results):
        x_positions = np.arange(len(all_years)) + (i * bar_width) - (bar_width * (n_configs-1)/2)
        
        # Create a mask for years present in this result
        mask = [year in result['years'].values for year in all_years]
        win_counts = [result['win_counts'].values[result['years'] == year][0] if year in result['years'].values else 0 for year in all_years]
        
        ax2.bar(x_positions[mask], 
                [c for m, c in zip(mask, win_counts) if m],
                width=bar_width,
                label=f"Lookback={result['lookback']}, Weight={result['weight']:.1f}",
                alpha=0.8)
    
    ax2.set_title('Total Number of Winning Draws per Year', fontsize=14, pad=20)
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Number of Wins', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Set x-axis ticks to years
    ax2.set_xticks(range(len(all_years)))
    ax2.set_xticklabels(all_years, rotation=45)
    
    plt.tight_layout()
    plt.savefig('toto_yearly_trends.png', bbox_inches='tight', dpi=300)
    plt.close()

def main():
    try:
        # Read the data
        data = read_toto_data('ToTo.csv')
        
        # Define parameters to analyze
        lookback_periods = [1, 2, 3, 4, 5, 6, 7]  # Short, medium, long term
        least_weights = [0.5]  # Low, medium, high weights
        
        print("Analyzing yearly trends...")
        results = analyze_yearly_trends(data, lookback_periods, least_weights)
        
        print("Generating plot...")
        plot_yearly_trends(results)
        
        print("\nTrend analysis complete!")
        print("Generated plot saved as 'toto_yearly_trends.png'")
        
    except FileNotFoundError:
        print("Error: ToTo.csv file not found in the current directory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 