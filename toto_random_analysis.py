import math
import numpy as np
from scipy.special import comb
import pandas as pd

def calculate_theoretical_probabilities():
    """Calculate theoretical probabilities for each prize tier."""
    # Total possible combinations for 6 numbers from 1-49
    total_combinations = comb(49, 6)
    
    # Calculate probabilities for each tier
    # Group 1: Match all 6 numbers
    prob_group1 = 1 / total_combinations
    
    # Group 2: Match 5 numbers + additional
    prob_group2 = (comb(6, 5) * 1) / total_combinations
    
    # Group 3: Match 5 numbers (without additional)
    prob_group3 = (comb(6, 5) * comb(43, 1)) / total_combinations
    
    # Group 4: Match 4 numbers + additional
    prob_group4 = (comb(6, 4) * comb(43, 1)) / total_combinations
    
    # Group 5: Match 4 numbers (without additional)
    prob_group5 = (comb(6, 4) * comb(43, 2)) / total_combinations
    
    # Group 6: Match 3 numbers + additional
    prob_group6 = (comb(6, 3) * comb(43, 2)) / total_combinations
    
    # Group 7: Match 3 numbers (without additional)
    prob_group7 = (comb(6, 3) * comb(43, 3)) / total_combinations
    
    return {
        'Group 1 (6 numbers)': prob_group1,
        'Group 2 (5 numbers + additional)': prob_group2,
        'Group 3 (5 numbers)': prob_group3,
        'Group 4 (4 numbers + additional)': prob_group4,
        'Group 5 (4 numbers)': prob_group5,
        'Group 6 (3 numbers + additional)': prob_group6,
        'Group 7 (3 numbers)': prob_group7
    }

def calculate_expected_value():
    """Calculate expected value for a random TOTO ticket."""
    probs = calculate_theoretical_probabilities()
    prizes = {
        'Group 1 (6 numbers)': 1000000,
        'Group 2 (5 numbers + additional)': 100000,
        'Group 3 (5 numbers)': 2000,
        'Group 4 (4 numbers + additional)': 400,
        'Group 5 (4 numbers)': 50,
        'Group 6 (3 numbers + additional)': 25,
        'Group 7 (3 numbers)': 10
    }
    
    expected_value = sum(probs[group] * prizes[group] for group in probs.keys())
    ticket_cost = 1
    
    return expected_value - ticket_cost

def calculate_random_win_probabilities():
    """Calculate probabilities of winning for random guessing."""
    # Total possible combinations for 6 numbers from 1-49
    total_combinations = comb(49, 6)
    
    # Calculate probabilities for each prize tier
    
    # Group 1 (6 numbers)
    prob_group1 = 1 / total_combinations
    
    # Group 2 (5 numbers + additional)
    # First choose 5 from winning numbers (C(6,5)) and match with additional number
    prob_group2 = (comb(6, 5) * 1) / total_combinations
    
    # Group 3 (5 numbers)
    # Choose 5 from winning numbers (C(6,5)) and 1 from remaining non-winning numbers
    prob_group3 = (comb(6, 5) * comb(42, 1)) / total_combinations
    
    # Group 4 (4 numbers + additional)
    prob_group4 = (comb(6, 4) * 1 * comb(42, 1)) / total_combinations
    
    # Group 5 (4 numbers)
    prob_group4_only = (comb(6, 4) * comb(42, 2)) / total_combinations
    
    # Group 6 (3 numbers + additional)
    prob_group6 = (comb(6, 3) * 1 * comb(42, 2)) / total_combinations
    
    # Group 7 (3 numbers)
    prob_group7 = (comb(6, 3) * comb(42, 3)) / total_combinations
    
    # Total probability of winning any prize
    total_win_prob = (prob_group1 + prob_group2 + prob_group3 + prob_group4 + 
                      prob_group4_only + prob_group6 + prob_group7)
    
    # Expected value calculation
    prizes = {
        'Group 1 (6 numbers)': 1000000,
        'Group 2 (5 + additional)': 100000,
        'Group 3 (5 numbers)': 2000,
        'Group 4 (4 + additional)': 400,
        'Group 5 (4 numbers)': 50,
        'Group 6 (3 + additional)': 25,
        'Group 7 (3 numbers)': 10
    }
    
    probabilities = {
        'Group 1 (6 numbers)': prob_group1,
        'Group 2 (5 + additional)': prob_group2,
        'Group 3 (5 numbers)': prob_group3,
        'Group 4 (4 + additional)': prob_group4,
        'Group 5 (4 numbers)': prob_group4_only,
        'Group 6 (3 + additional)': prob_group6,
        'Group 7 (3 numbers)': prob_group7
    }
    
    expected_value = sum(prizes[group] * probabilities[group] for group in prizes)
    
    return probabilities, total_win_prob, expected_value

def main():
    probabilities, total_win_prob, expected_value = calculate_random_win_probabilities()
    
    print("TOTO Random Guess Analysis")
    print("=" * 50)
    
    print("\nWinning Probabilities for Each Prize Group:")
    for group, prob in probabilities.items():
        print(f"{group:25s}: {prob:10.8f} ({prob*100:6.4f}%)")
    
    print("\nSummary:")
    print(f"Total probability of winning any prize: {total_win_prob:10.8f} ({total_win_prob*100:6.4f}%)")
    print(f"Expected value per $1 bet: ${expected_value:.4f}")
    print(f"Expected loss per $1 bet: ${expected_value-1:.4f}")
    
    # Calculate odds
    odds = 1 / total_win_prob
    print(f"\nOdds of winning any prize: 1 in {odds:.2f}")
    
    print("\nComparison with Strategy Results:")
    print("-" * 50)
    try:
        # Load optimization results
        results_df = pd.read_csv('optimization_results.csv')
        best_win_rate = results_df['Win_Rate'].max()
        avg_win_rate = results_df['Win_Rate'].mean()
        
        print(f"Random Guess Win Rate: {total_win_prob*100:.2f}%")
        print(f"Strategy Best Win Rate: {best_win_rate:.2f}%")
        print(f"Strategy Average Win Rate: {avg_win_rate:.2f}%")
        print(f"\nStrategy Improvement over Random:")
        print(f"Best: {(best_win_rate/(total_win_prob*100)-1)*100:.1f}% better")
        print(f"Average: {(avg_win_rate/(total_win_prob*100)-1)*100:.1f}% better")
        
    except FileNotFoundError:
        print("Note: optimization_results.csv not found for comparison")

if __name__ == "__main__":
    main() 


'''Theoretical Probabilities:
Group 1 (6 numbers):
  Probability: 0.00000715%
  Odds: 1 in 13,983,816
Group 2 (5 numbers + additional):
  Probability: 0.00004291%
  Odds: 1 in 2,330,636
Group 3 (5 numbers):
  Probability: 0.00184499%
  Odds: 1 in 54,201
Group 4 (4 numbers + additional):
  Probability: 0.00461247%
  Odds: 1 in 21,680
Group 5 (4 numbers):
  Probability: 0.09686197%
  Odds: 1 in 1,032
Group 6 (3 numbers + additional):
  Probability: 0.12914930%
  Odds: 1 in 774
Group 7 (3 numbers):
  Probability: 1.76504039%
  Odds: 1 in 57

Overall Win Probability:
Chance of winning any prize: 1.9976%
Odds of winning any prize: 1 in 50.1

Expected Value per $1 Ticket: $-0.57

Comparison with Strategy Results:
--------------------------------------------------
Random Guess Win Rate: 2.00%
Strategy Best Win Rate: 2.64%
Strategy Average Win Rate: 1.83%

Strategy Improvement over Random:
Best: 32.1% better
Average: -8.2% better'''