# Create your views here.
from datetime import datetime
import requests
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import Portfolio
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Coin
from django.contrib import messages

def home(request):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    coins = response.json()
    return render(request, 'tracker/home.html', {'coins': coins})



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})






@login_required
def portfolio(request):
    portfolio_items = Portfolio.objects.filter(user=request.user)
    total_investment = sum(item.amount for item in portfolio_items)

    for item in portfolio_items:
     
        item.current_price = get_coin_current_price(item.symbol)

    return render(request, 'tracker/portfolio.html', {
        'portfolio_items': portfolio_items,
        'total_investment': total_investment
    })

def get_coin_current_price(symbol):

    coin_prices = {
        'btc': 60000,
        'eth': 4000,
        'ltc': 200,
    
    }
    return coin_prices.get(symbol.lower(), 0) 



@login_required
def add_to_portfolio(request):
    if request.method == 'POST':
        try:
            coin_name = request.POST.get('coin_name')
            symbol = request.POST.get('symbol')
            amount = request.POST.get('amount')

            if not coin_name or not symbol or not amount:
                return render(request, 'error.html', {'message': 'Missing required fields'})

            Portfolio.objects.create(
                user=request.user,
                coin_name=coin_name,
                symbol=symbol,
                amount=float(amount)
            )

            return redirect('home')

        except Exception as e:
           
            return render(request, "tracker/error.html", {"message": "Invalid coin data"})

    return redirect('portfolio')

@login_required
def delete_coin(request, id):
    coin = Portfolio.objects.get(id=id, user=request.user)
    coin.delete()
    return redirect('portfolio')






def coin_detail(request, coin_id):
    coin = get_object_or_404(Coin, id=coin_id)
    coin.history_1h = 50000  
    coin.history_6h = 51000  
    coin.history_12h = 52000  
    coin.history_24h = 55000  
    coin.history_7d = 60000   

    return render(request, 'tracker/coin_detail.html', {
        'coin': coin
    })




def get_crypto_news(request):
    url = 'https://newsapi.org/v2/everything?q=crypto&apiKey=ef09c99c33714783a205801d8be24866'
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get('articles', [])
    return render(request, 'tracker/news.html', {'articles': articles})

def coin_chart(request, coin_id):
    api_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=7&interval=hourly"
    response = requests.get(api_url)
    data = response.json()

    prices = data.get("prices", [])  # [timestamp, price]
    labels = [point[0] for point in prices]
    values = [point[1] for point in prices]

    context = {
        'coin_id': coin_id,
        'labels': labels,
        'values': values,
    }
    return render(request, 'tracker/coin_chart.html', context)


import requests
import csv
from django.http import HttpResponse
def download_csv(request):
    response_api = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False,
    })
    coins_data = response_api.json()  # API se data mil gaya

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="coins_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Symbol', 'Current Price'])

    for coin in coins_data:
        writer.writerow([coin['name'], coin['symbol'], coin['current_price']])

    return response





# def coins_table(request):
#     response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
#         'vs_currency': 'usd',
#         'order': 'market_cap_desc',
#         'per_page': 20,
#         'page': 1,
#         'sparkline': False
#     })
#     coins = response.json()
#     return render(request, 'tracker/coins_table.html', {'coins': coins})

# # def chart_view(request, symbol):
# #     return render(request, 'tracker/chart.html', {'symbol': symbol})


# def chart_view(request, symbol):
#     # Yahan aap apne symbol ke basis par chart ko render karenge
#     return render(request, 'tracker/chart.html', {'symbol': symbol})




# views.py
import requests
from django.shortcuts import render

# Mapping from coin symbol to CoinGecko coin ID
COIN_ID_MAP = {
    'btc': 'bitcoin',
    'eth': 'ethereum',
    'ltc': 'litecoin',
    'xrp': 'ripple',
    'bnb': 'binancecoin',
    'sol': 'solana',
    'ada': 'cardano',
    'doge': 'dogecoin',
    'dot': 'polkadot',
    'matic': 'matic-network',
    # Add more as needed
}

# View for showing coins table
def coins_table(request):
    response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 20,
        'page': 1,
        'sparkline': False
    })
    coins = response.json()
    return render(request, 'tracker/coins_table.html', {'coins': coins})

# View for showing chart based on coin symbol
# def chart_view(request, symbol):
#     symbol = symbol.lower()
#     coin_id = COIN_ID_MAP.get(symbol)

#     if coin_id:
#         return render(request, 'tracker/chart.html', {'symbol': coin_id})
#     else:
#         # If symbol not found, default to Bitcoin chart
#         return render(request, 'tracker/chart.html', {'symbol': 'bitcoin'})


def chart_view(request, symbol):
    tradingview_symbols = {
        'btc': 'BINANCE:BTCUSDT',
        'eth': 'BINANCE:ETHUSDT',
        'ada': 'BINANCE:ADAUSDT',
        'xrp': 'BINANCE:XRPUSDT',
        'doge': 'BINANCE:DOGEUSDT',
        # aur bhi coin chaho toh add kar sakte ho
    }

    # Default agar symbol match na ho
    tradingview_symbol = tradingview_symbols.get(symbol.lower(), 'BINANCE:BTCUSDT')

    return render(request, 'tracker/chart.html', {
        'tradingview_symbol': tradingview_symbol,
        'coin_name': symbol.upper()
    })

