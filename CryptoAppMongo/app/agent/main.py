import requests
import pymongo
import time
from collections import OrderedDict 

def get_db_connection(uri):
    client = pymongo.MongoClient(uri) 
    return client.cryptongo

API_URL = 'https://api.coinmarketcap.com/v1/ticker/' 


def get_cryptocurrencies_from_api():
    r = requests.get(API_URL) 
    if r.status_code == 200: 
        result = r.json() 
        return result 
    raise Exception('API Error')
    
def first_element(elements): 
    return elements[0]

def get_hash(value):
    from hashlib import sha512
    return sha512(value.encode('utf-8')).hexdigest() 


def get_ticker_hash(ticker_data):
    
    ticker_data = OrderedDict(
        sorted( ticker_data.items(), 
                key = first_element,
                reverse=False
        )
    )
    ticker_value = ''
    for _, value in ticker_data.items():  
        ticker_value += str(value) 
    return get_hash(ticker_value) 

def check_exist_tickers(connection, ticker_hash): 
    
    if connection.data.find_one({'tickerhash' : ticker_hash}):
        return True
    else: 
        return False

def save_ticker(connection, ticker_data=None): 
    if not ticker_data:
        return False  

    ticker_hash = get_ticker_hash(ticker_data)
    if check_exist_tickers(connection,  ticker_hash): 
        return False

    ticker_data['tickerhash'] = get_ticker_hash(ticker_data) 

    connection.data.insert_one(ticker_data) 
    return True



if __name__ == "__main__":
    while True:
        print("Guardando información en CryptoMongo")
        connection = get_db_connection('mongodb://mongo-crypto:27017/')
        tickers = get_cryptocurrencies_from_api()

        for ticker in tickers:
            save_ticker(connection, ticker)
        time.sleep(240)