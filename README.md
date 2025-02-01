# TOTO Analysis Project

This project analyzes Singapore TOTO lottery data to study various betting strategies and their effectiveness over time.

## Overview

The project includes several Python scripts that perform different types of analysis on TOTO lottery data:

1. `toto_random_analysis.py`: Calculates theoretical win probabilities and expected values for random guessing
2. `toto_trend_analysis.py`: Analyzes historical win rates and trends using different lookback periods
3. `toto_optimize_replot.py`: Creates visualizations of optimization results
4. `toto_backtest.py`: Core backtesting engine for strategy evaluation
5. `toto_analyzer.py`: Utility functions for data processing and analysis

## Features

- **Random Analysis**: Calculates theoretical probabilities for each prize tier and expected value of a random ticket
- **Trend Analysis**: 
  - Analyzes win rates over different years
  - Tests multiple lookback periods (1-7 draws)
  - Compares strategy performance against random guessing baseline
  - Visualizes both win rates and total winning draws per year
- **Strategy Optimization**: 
  - Tests different combinations of parameters
  - Creates heatmaps of optimization results
  - Helps identify optimal strategy configurations

## Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib
- scipy

## Installation

1. Clone this repository:
```bash
git clone https://github.com/maliangone/toto-analysis.git
cd toto-analysis
```

2. Install required packages:
```bash
pip install pandas numpy matplotlib scipy
```

## Usage

1. Place your TOTO data file (`ToTo.csv`) in the project directory
2. Run the random analysis:
```bash
python toto_random_analysis.py
```
3. Run the trend analysis:
```bash
python toto_trend_analysis.py
```

## Data Format

The input data (`ToTo.csv`) should contain the following columns:
- Date: Draw date in DD/MM/YYYY format
- Winning numbers (6 numbers + 1 additional)
- Prize information for each tier

## Results

The analysis generates several visualizations:
- `toto_yearly_trends.png`: Shows yearly win rates and winning draw counts for different strategies
- Win rates are compared against the theoretical random guess baseline (2.179%)
- Results are broken down by lookback period to identify the most effective strategy parameters

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Feel free to open issues or submit pull requests with improvements.

## Disclaimer

This project is for educational purposes only. It does not guarantee any lottery wins and should not be used as financial advice. 