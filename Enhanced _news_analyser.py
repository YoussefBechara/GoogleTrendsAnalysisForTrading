from bs4 import BeautifulSoup
import requests
import yfinance as yf
import os

def ask_hugchat(text):
    from hugchat import hugchat
    from hugchat.login import Login
    email= input('Insert Your hugchat email: ')
    passwd = input('Insert Your hugchat password: ')
    sign = Login(email, passwd)
    cookies = sign.login()
    current_dir = os.getcwd()
    cookie_path_dir = os.path.join(current_dir, "cookies_snapshot")
    sign.saveCookiesToDir(cookie_path_dir)
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    response = chatbot.chat(text)
    return str(response)

def init_claude():
    import time
    from sys import exit as sys_exit
    from claude_api.client import (
        ClaudeAPIClient,
        SendMessageResponse,
    )
    from claude_api.session import SessionData, get_session_data
    from claude_api.errors import ClaudeAPIError, MessageRateLimitError, OverloadError

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
    cookie_header = "__stripe_mid=c9003624-f5cc-4358-affc-30aee52f93a8516e11; __ssid=ff6a565c7191b3a075ff6ea308d0f19; intercom-device-id-lupk8zyo=09c3d444-db0d-4d1d-880d-ccdb0433822d; CH-prefers-color-scheme=dark; sessionKey=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; lastActiveOrg=b4787981-7208-48d8-ac30-7f19e40a1a22; intercom-session-lupk8zyo=QmV5c0lXWmFSYTVZeHpSMGhPMWpQUjRrSlk0Q0lTVEdKNHh6ZTM2K2tpc0N4OVlEUjJnQ3NUZTlaUlE0SFFtby0tVk85NWMxSVVvQVhoNm0wOGwvczRkQT09…FZOpspgLtX_jI1VMIrrfF8e2dPHlAqnowrRAbR3oMa5H3UQrg1ikMK98xegAP.SnVcrJ6D5wJ8VyUULv3JX2802Mm5tyKJIRDgMGGYxyNA5DhaZ8vNLVzAl2dpbYCL3JewwQHhdYmW2tDYj6CTJlNV8FeejHtZ0sNF4r7MCPVoxWr7N6UeX.lp.iWbmXS1VODwhQKmPg_IIUNG7M_2l2dblcE4I1RHg.zysf2Z.UxkktAnhJbpjs3ydYpudddPDqYRhhJL1cN6YkaPEF87hDSJEYwHlndLNEq5eeEE3O4r4N3H0YJaRzxNru2PEVJxfWglnjPI3yKZojpTXriZrQsID_kvBtOX5c; __cf_bm=g2svOLZAs0YeG0pCVV6BrMW0w4rRlxU6VGJTIp128rs-1724414656-1.0.1.1-p6IOmcjqG56gamCR6VMDdpymmg5Gv6Ph5XXZ7mDEOXIhEKRZBfJ2.Wm53Xl8_osBAKiGy3AwldQ5Bpnd24Jcdw"
    cookie_header = cookie_header.replace('…', '...')

    for i in range(5):
        try:
            session = SessionData(cookie_header, user_agent)
            global client
            client = ClaudeAPIClient(session, timeout=240)
            global chat_id
            chat_id = client.create_chat()
            if not chat_id:
                print("\nMessage limit hit, cannot create chat...")
                sys_exit(1)
        except RuntimeError as r:
            print(r+'Were going to try again')
            time.sleep(60)
def ask_claude(txt):
    from sys import exit as sys_exit
    from claude_api.client import (
          ClaudeAPIClient,
          SendMessageResponse,
      )
    from claude_api.session import SessionData, get_session_data
    from claude_api.errors import ClaudeAPIError, MessageRateLimitError, OverloadError
    res = None
    try:
        res: SendMessageResponse = client.send_message(
            chat_id, f"{txt}"
        )

    except ClaudeAPIError as e:
        if isinstance(e, MessageRateLimitError):
            print(f"\nMessage limit hit, resets at {e.reset_date}")
            print(f"\n{e.sleep_sec} seconds left until -> {e.reset_timestamp}")
        elif isinstance(e, OverloadError):
            print(f"\nOverloaded error: {e}")
        else:
            print(f"\nGot unknown Claude error: {e}")
    return res.answer


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

def main(llm_model = 'claude'):
    stock_symbol = input("Enter a forex or stock symbol: ").upper()
    number_of_articles = int(input("How many articles do you want to scan (8 max): "))
    articles = get_articles(stock_symbol, num_articles=number_of_articles)
    ratings_list = []
    print(f"Top {len(articles)} articles for {stock_symbol}:")
    i=0
    for idx, article in enumerate(articles, start=1):
        content = scrape_article_content(article['link'])
        msg = f"""Im going to share with you a news article about {stock_symbol}, ONLY respond with a rating of n/100 of how good the news are concerning the {stock_symbol} (e.g if you gave 95/100 it means the stock will go up) OR if you there isnt any news then give it 50/100, here's the article: {content}. PLEASE ONLY RESPOND WITH A NUMBER NOTHING ELSE!!!!!!"""
        if llm_model.lower() == 'hugchat':
            ai_response = ask_hugchat(msg)
        elif llm_model.lower() == 'claude':
            if i == 0:
              init_claude()
            ai_response = ask_claude(msg)
        else:
            print(f'The llm {llm_model} is unsupported! Available LLMs: hugchat, claude')
        splitted = ai_response.split('/100')
        try:
            rating = int(splitted[0][-3:])
            ratings_list.append(rating)
            newsometer = f"{rating}/100"
            print(newsometer +' '+ article['link'])
        except:
            pass
        i+=1
    avg_score = calc_avg_list(ratings_list)
    print(f"The average score for {stock_symbol} is {avg_score}/100")

if __name__ == "__main__":
    main(llm_model = 'hugchat')