
from binance.client import Client
import config_spot as config
import numpy as np
import threading
import websocket
import datetime
import json

#Executer Class 
class Executer:
    def __init__(self):
        self.client = Client(config.API, config.API_secret, testnet=True)

    def order(self, symbol, side, quantity):
        response = self.client.create_test_order(symbol = symbol,
                                                 side = side,
                                                 type = 'MARKET',
                                                 quantity = quantity)
        print(f'{side} --> {symbol} = {quantity}')
        print(response)

    def balance(self, symbol):
        return float(self.client.get_asset_balance(symbol)['free'])

#Pair Class
class Pair:
    A = ['ETHBTC',]
    B = ['ETHUSDT',]
    C = ['BTCUSDT',]
        
fee = 0.00
pair = Pair()
executer = Executer()

def arbitrage_execute(gain, pair_symbol):
    if gain > 1:
        executer.order(pair_symbol[0], 'BUY', executer.balance('BTC'))
        executer.order(pair_symbol[1], 'SELL', executer.balance('ETH'))
        executer.order(pair_symbol[2], 'BUY', executer.balance('USDT'))
        ws.close()

         
def arbitrage_opportunity(data, pair_id):
    try:
        return (1 - 3*fee) / data[pair.A[pair_id]] * data[pair.B[pair_id]] / data[pair.C[pair_id]], [pair.A[pair_id], pair.B[pair_id], pair.C[pair_id]]
    except: 
        return np.nan, np.nan


def arbitrage(date, data):
    date = datetime.datetime.utcfromtimestamp(date/1000).strftime('%Y-%m-%d %H:%M:%S')
    gain, pair_symbol = arbitrage_opportunity(data, 0)
    arbitrage_execute(gain, pair_symbol)
    print(f'{date}, pair->{pair_symbol}, gain={gain}')
        
def on_message(ws, message):
    message = json.loads(message)

    def run(*args):
        arbitrage(message[0]['E'], {m['s']: float(m['c']) for m in message})

    threading.Thread(target=run).start()


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


if __name__ == "__main__":

    socket_spot = 'wss://stream.binance.com/ws/!ticker@arr'
    ws = websocket.WebSocketApp(socket_spot,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

   