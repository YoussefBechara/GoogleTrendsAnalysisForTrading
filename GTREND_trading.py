import time
from pytrends.request import TrendReq
import pytrends.exceptions

def get_interest_data(symbol, category, timeframe, retries=5):
    pytrend = TrendReq(hl='en-US', tz=360)
    
    # Build the payload for the symbol
    kw_list = [f'{symbol} {category}']
    pytrend.build_payload(kw_list, cat=0, timeframe=timeframe, geo='', gprop='')

    # Try to get the data with retries
    for attempt in range(retries):
        try:
            # Introduce a delay before making the request
            time.sleep(30 * (attempt + 1))
            
            # Get interest over time
            interest_over_time_df = pytrend.interest_over_time()
            return interest_over_time_df
        except pytrends.exceptions.TooManyRequestsError:
            print(f"Too many requests made to Google Trends. Attempt {attempt + 1} of {retries}. Retrying after delay...")

    print("Failed to fetch data after multiple attempts. Please try again later.")
    return None

def calculate_weighted_average_interest(interest_data, symbol, category):
    if not interest_data.empty:
        weights = [i + 1 for i in range(len(interest_data))]
        weighted_average_interest = (interest_data[f'{symbol} {category}'] * weights).sum() / sum(weights)
        return weighted_average_interest
    else:
        return None

def calculate_interest_deviation(interest_data, symbol, category):
    if not interest_data.empty:
        current_interest = interest_data[f'{symbol} {category}'].iloc[-1]
        weighted_average_interest = calculate_weighted_average_interest(interest_data, symbol, category)

        # Calculate the deviation score
        deviation_score = ((current_interest - weighted_average_interest) / weighted_average_interest) * 50 + 50
        return deviation_score
    else:
        return None

if __name__ == "__main__":
    symbol = input("Enter the symbol (e.g., TSLA, EURUSD): ").upper()
    category = input("Enter the category (e.g., stock, forex): ").lower()
    timeframe = 'now 7-d'  # You can adjust the timeframe as needed

    interest_data = get_interest_data(symbol, category, timeframe)

    if interest_data is not None:
        deviation_score = calculate_interest_deviation(interest_data, symbol, category)
        
        if deviation_score is not None:
            print(f"Interest deviation score for {symbol} {category}: {deviation_score:.2f}")
        else:
            print(f"No data available for {symbol} {category}. Please check the symbol and category.")
