import pandas as pd
import numpy as np
from collections import defaultdict

def read_toto_data(file_path):
    """Read TOTO data from CSV file."""
    return pd.read_csv(file_path)

def get_all_numbers_from_row(row):
    """Extract all winning numbers and additional number from a row."""
    numbers = []
    # Get winning numbers
    winning_numbers = []
    for col in ['Winning Number 1', '2', '3', '4', '5', '6']:
        if pd.notna(row[col]):  # Check if the value is not NaN
            winning_numbers.append(int(row[col]))
    numbers = sorted(winning_numbers)  # Sort winning numbers
    
    # Add additional number
    if pd.notna(row['Additional Number']):
        numbers.append(int(row['Additional Number']))
    return numbers, winning_numbers

def calculate_weighted_frequencies(data, target_draw, lookback_draws, least_weight=0.1):
    """Calculate weighted frequency of numbers in the specified lookback period."""
    # Find the index of the target draw
    target_idx = data[data['Draw'] == target_draw].index[0]

    # Get the lookback data before the target draw
    lookback_data = data.iloc[target_idx + 1:target_idx + lookback_draws + 1]
    
    # Initialize dictionary for weighted frequencies
    weighted_frequencies = defaultdict(float)
    
    # Calculate weights (linear decay)
    # Most recent draw gets weight 1.0, oldest draw gets weight 0.1
    weights = np.linspace(1.0, least_weight, len(lookback_data))

    # Process each draw with its corresponding weight
    for idx, (_, row) in enumerate(lookback_data.iterrows()):
        numbers, _ = get_all_numbers_from_row(row)
        weight = weights[idx]
        
        # Update weighted frequencies
        for number in numbers:
            weighted_frequencies[number] += weight
    
    return weighted_frequencies

def get_suggested_numbers(weighted_frequencies, num_picks=6):
    """Get suggested numbers based on weighted frequencies."""
    # Sort numbers by frequency
    sorted_numbers = sorted(weighted_frequencies.items(), 
                          key=lambda x: x[1], reverse=True)
    
    # Return top num_picks numbers
    return sorted([num for num, _ in sorted_numbers[:num_picks]])

def check_winning(picked_numbers, winning_numbers, additional_number):
    """Check winning status and return prize."""
    picked_set = set(picked_numbers)
    winning_set = set(winning_numbers)
    
    matches = len(picked_set.intersection(winning_set))
    has_additional = additional_number in picked_set
    
    # Prize structure
    if matches == 6:
        return 1000000  # Group 1 - 6 numbers
    elif matches == 5 and has_additional:
        return 100000   # Group 2 - 5 numbers + additional
    elif matches == 5:
        return 2000     # Group 3 - 5 numbers
    elif matches == 4 and has_additional:
        return 400      # Group 4 - 4 numbers + additional
    elif matches == 4:
        return 50       # Group 5 - 4 numbers
    elif matches == 3 and has_additional:
        return 25       # Group 6 - 3 numbers + additional
    elif matches == 3:
        return 10       # Group 7 - 3 numbers
    return 0

def main():
    try:
        # Read the data
        data = read_toto_data('ToTo.csv')
        
        # Get user input for target draw
        while True:
            try:
                target_draw = int(input("Enter the draw number to analyze (e.g., 4048): "))
                if target_draw in data['Draw'].values:
                    break
                print("Draw number not found in data. Please enter a valid draw number.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get user input for lookback period
        while True:
            try:
                lookback = int(input("Enter the number of draws to look back (1-100): "))
                if 1 <= lookback <= 100:
                    break
                print("Please enter a number between 1 and 100.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Calculate weighted frequencies
        weighted_frequencies = calculate_weighted_frequencies(data, target_draw, lookback)
        
        # Get suggested numbers
        suggested_numbers = get_suggested_numbers(weighted_frequencies)
        
        # Get actual winning numbers for the target draw
        target_row = data[data['Draw'] == target_draw].iloc[0]
        actual_numbers, actual_winning = get_all_numbers_from_row(target_row)
        actual_additional = actual_numbers[-1]
        
        # Calculate prize
        prize = check_winning(suggested_numbers, actual_winning, actual_additional)
        
        # Print results
        print(f"\nAnalysis for Draw #{target_draw}:")
        print(f"Based on {lookback} previous draws")
        print("\nSuggested numbers (sorted):", suggested_numbers)
        print("\nActual winning numbers:", actual_winning)
        print("Actual additional number:", actual_additional)
        
        print("\nBetting Result:")
        print(f"Cost: $1")
        print(f"Prize: ${prize}")
        print(f"Net Profit: ${prize - 1}")
        
        # Print weight explanation
        print("\nWeight Distribution Used:")
        print(f"Most recent draw: 100% weight")
        print(f"Oldest analyzed draw: 10% weight")
        print("(Weights decrease linearly for draws in between)")

    except FileNotFoundError:
        print("Error: ToTo.csv file not found in the current directory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 
