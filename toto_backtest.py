import pandas as pd
from toto_analyzer import (read_toto_data, get_all_numbers_from_row,
                         calculate_weighted_frequencies, get_suggested_numbers,
                         check_winning)

def run_backtest(data, lookback_period, start_draw=None, end_draw=None, least_weight=0.1):
    """Run backtest over specified period."""
    results = []
    
    # Get draw numbers to test
    draws = data['Draw'].values
    if start_draw:
        draws = draws[draws <= start_draw]
    if end_draw:
        draws = draws[draws >= end_draw]
    
    total_cost = 0
    total_prize = 0
    wins = 0
    
    for draw in draws:
        # Skip last few draws where we don't have enough lookback data
        if len(data[data['Draw'] < draw]) < lookback_period:
            continue
            
        # Calculate suggested numbers for this draw
        weighted_frequencies = calculate_weighted_frequencies(data, draw, lookback_period, least_weight)
        suggested_numbers = get_suggested_numbers(weighted_frequencies)
        
        # Get actual results
        target_row = data[data['Draw'] == draw].iloc[0]
        actual_numbers, actual_winning = get_all_numbers_from_row(target_row)
        actual_additional = actual_numbers[-1]
        
        # Calculate prize
        prize = check_winning(suggested_numbers, actual_winning, actual_additional)
        
        # Record result
        result = {
            'Draw': draw,
            'Date': target_row['Date'],
            'Suggested_Numbers': suggested_numbers,
            'Winning_Numbers': actual_winning,
            'Additional_Number': actual_additional,
            'Prize': prize,
            'Profit': prize - 1
        }
        results.append(result)
        
        # Update statistics
        total_cost += 1
        total_prize += prize
        if prize > 0:
            wins += 1
    
    return results, total_cost, total_prize, wins

def main():
    try:
        # Read the data
        data = read_toto_data('ToTo.csv')
        
        # Get user input for lookback period
        while True:
            try:
                lookback = int(input("Enter the number of draws to look back (1-100): "))
                if 1 <= lookback <= 100:
                    break
                print("Please enter a number between 1 and 100.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Run backtest
        results, total_cost, total_prize, wins = run_backtest(data, lookback, least_weight=0.1)
        
        # Print summary
        print("\nBacktest Results:")
        print(f"Strategy: Using {lookback} previous draws for frequency analysis")
        print(f"\nTotal draws played: {len(results)}")
        print(f"Total cost: ${total_cost}")
        print(f"Total prize money: ${total_prize}")
        print(f"Net profit/loss: ${total_prize - total_cost}")
        print(f"Number of wins: {wins}")
        if len(results) > 0:
            print(f"Win rate: {wins/len(results)*100:.2f}%")
            print(f"Average return per bet: ${(total_prize - total_cost)/len(results):.2f}")
        
        # Print detailed results for wins
        print("\nDetailed Results for Winning Draws:")
        print("-" * 80)
        for result in results:
            if result['Prize'] > 0:
                print(f"\nDraw #{result['Draw']} ({result['Date']}):")
                print(f"Suggested numbers: {result['Suggested_Numbers']}")
                print(f"Winning numbers: {result['Winning_Numbers']}")
                print(f"Additional number: {result['Additional_Number']}")
                print(f"Prize: ${result['Prize']}")
                print(f"Net profit: ${result['Profit']}")
                print("-" * 40)

    except FileNotFoundError:
        print("Error: ToTo.csv file not found in the current directory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 