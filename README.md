markdown

# Google Trends Analysis for Trading

## Overview

This project provides a tool for analyzing Google Trends data for potential trading insights. It calculates a weighted standard deviation of search interest, giving more importance to recent trends. This can be used to gauge public interest in various topics or assets, which might be relevant for trading decisions.

## Features

- Fetches and analyzes Google Trends data
- Calculates a weighted standard deviation of search interest
- Puts more emphasis on recent data points
- Compares the result to an average baseline of 50
- Provides insights that could be valuable for trading strategies

## Installation

1. Clone the repository:

git clone https://github.com/YoussefBechara/GoogleTrendsAnalysisForTrading.git


2. Navigate to the project directory:

cd GoogleTrendsAnalysisForTrading


3. Install required dependencies:

pip install -r requirements.txt
 
4. If you want to use hugchat LLM, follow the installation of this repository by Soulter: https://github.com/Soulter/hugging-chat-api

5. If you want to use Claude LLM, follow the installation of this repository by st1vms: https://github.com/st1vms/unofficial-claude-api 

## Usage

Run the main script:

python GTREND_trading.py
livecodeserver


The program will return a standard deviation value. Interpret the results as follows:
- The higher the number compared to the average (50), the more people are interested in the topic.
- Recent values have a bigger weight on the standard deviation.

## Files

- `GTREND_trading.py`: Main script for Google Trends analysis
- `Enhanced_news_analyser.py`: Enhanced version of the news analyzer
- `Enhancednewsanalysernotebook.ipynb`: Jupyter notebook with enhanced news analysis

## How It Works

1. The program fetches Google Trends data for a specified topic or asset.
2. It calculates a weighted standard deviation, giving more importance to recent data points.
3. The result is compared to a baseline average of 50.
4. A higher standard deviation suggests increased public interest, which could be relevant for trading decisions.

## Contributing

Contributions to improve the analysis or extend the functionality are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This tool is for informational purposes only. It should not be considered financial advice. Always do your own research and consult with a qualified financial advisor before making trading decisions.

---

Developed by Youssef Bechara
