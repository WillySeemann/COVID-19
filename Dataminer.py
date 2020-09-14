import bs4 as bs
import pickle
import requests
import os
import pandas_datareader as web
import datetime as dt
import pandas as pd

def save_sp500_tickers():
    respons = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(respons.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for reihe in table.findAll('tr')[1:]:
        ticker = reihe.findAll('td')[1].text
        tickers.append(ticker)
        
    with open("sp500tickers.pickle",'wb') as f:
        pickle.dump(tickers,f)
        
    return tickers


def lade_preise_von_yahoo(ticker_neuladen=False):
    if ticker_neuladen:
      tickers = save_sp500_tickers()
    else:
     with open("sp500tickers.pickle",'rb') as f:
          tickers = pickle.load(f)
    if not os.path.exists('kursdaten'):
     os.makedirs('kursdaten')
    start = dt.datetime(2010,1,1)
    end = dt.datetime(2019,12,31)
    print(tickers)
    for ticker in tickers:        
     if not os.path.exists('kursdaten/{}.csv'.format(ticker)):
      print("{} wird geladen...".format(ticker))
      df = web.DataReader(ticker, 'yahoo', start, end)
      df.to_csv('kursdaten/{}.csv'.format(ticker))
    else:
        print("{} bereits vorhanden!".format(ticker))


def daten_kompilieren():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for ticker in tickers:
        df = pd.read_csv("kursdaten/{}.csv".format(ticker))
        df.set_index("Date", inplace=True)

        df.rename(columns={"Adj Close": ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
    main_df.to_csv('sp500_daten.csv')
print("Daten kompeliert!")


lade_preise_von_yahoo(ticker_neuladen=True)
