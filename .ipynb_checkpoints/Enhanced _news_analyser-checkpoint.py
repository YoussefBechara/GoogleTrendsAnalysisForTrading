from bs4 import BeautifulSoup
import requests
from hugchat import hugchat
from hugchat.login import Login
import yfinance as yf

def ask_hugchat(text):
    email= 'yoyobechara11@gmail.com'
    passwd = 'Omggamer,3'
    sign = Login(email, passwd)
    cookies = sign.login()
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    response = chatbot.query(text)
    return str(response)
    
def get_articles(symbol, num_articles=5):
    articles = []
    ticker = yf.Ticker(symbol)
    data = ticker.news
    for iteration in data:
        articles.append({'title': iteration['title'], 'link': iteration['link']})
    try:
        articles_list = articles[:num_articles]
    except:
        print(f"The number of articles you requested is too large, currently the maximum number of articles i can get is {len(articles)}")
    return articles_list
def calc_avg_list(li):
    vals_without_50 = []
    for i in range (len(li)):
        if li[i] == 50:
            continue
        vals_without_50.append(li[i])
    sum_of_nums = 0
    for i in range(len(vals_without_50)):
        sum_of_nums+=vals_without_50[i]
    return sum_of_nums//len(vals_without_50)
def scrape_article_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.text

if __name__ == "__main__":
    stock_symbol = input("Enter a forex or stock symbol: ").upper()
    number_of_articles = int(input("How many articles do you want to scan: "))
    articles = get_articles(stock_symbol, num_articles=number_of_articles)
    ratings_list = []
    print(f"Top {len(articles)} articles for {stock_symbol}:")
    for idx, article in enumerate(articles, start=1):
        content = scrape_article_content(article['link'])
        msg = f"""Im going to share with you a news article about {stock_symbol}, ONLY respond with a rating of n/100 of how good the news are concerning the {stock_symbol} (e.g if you gave 95/100 it means the stock will go up) OR if you there isnt any news then give it 50/100, here's the article: {content}. PLEASE ONLY RESPOND WITH A NUMBER NOTHING ELSE!!!!!!"""
        ai_response = ask_hugchat(msg)
        splitted = ai_response.split('/100')
        try:
            rating = int(splitted[0][-3:])
            ratings_list.append(rating)
            newsometer = f"{rating}/100"
            print(newsometer +' '+ article['link'])
        except:
            pass
    avg_score = calc_avg_list(ratings_list)
    print(f"The average score for {stock_symbol} is {avg_score}/100")
    
