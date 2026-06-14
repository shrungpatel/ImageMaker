import requests

def get_quotes_from_api():
    response = requests.get("https://zenquotes.io/api/quotes/")
    data = response.json()
    api_quotes = []
    for item in data:
        api_quotes.append(item['q'])
    return api_quotes