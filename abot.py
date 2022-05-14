## HCISS Binance Trading Bot
# @denizumutdereli
#OOP env. UNDER CONSTRUCTION. 
##
import os
import sys
import time
#import ccxt
import ccxt.async_support as ccxt # link against the asynchronous version of ccxt

import talib as ta
import numpy as np
import argparse
import logging as log
from rich import print
from rich.pretty import pprint
from rich.progress import track
from prettytable import PrettyTable
from modules.Settings import Settings
from classes.config.Config import Config
from classes.exchanges.Comm import Comm
from classes import Log

#for fun!
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Help Open:1 / Close:0')
    parser.add_argument('-b', '--balance', type=int, default=0, help='Display the balance')
    parser.add_argument('-w', '--wallet', type=int, default=1, help='Displays the coin balance')
    parser.add_argument('--buy', type=int, default=1, help='Buy Permission')
    parser.add_argument('--sell', type=int, default=1, help='Sell Permission')
    parser.add_argument('-s', '--sounds', type=int, default=0, help='Sounds Open:1 / Close:0')
    parser.add_argument('-c', '--config', type=str, default="default", help='Config file')
    parser.add_argument('-v', '--verbose', help='print debugging messages',action="store_true")
    parser.add_argument('-y', help='accept all warnings',action="store_true")

    args = parser.parse_args()
   
    # log debug messages if verbose argument specified
    #importing config
    config = Config(args.config,Settings(args.verbose))
    config.buy_permission = args.buy
    config.sell_permission = args.sell
    config.balance = args.balance
    config.wallet = args.wallet
    config.settings.sounds = args.sounds
    config.settings.accept = 1 if args.y else 0
 
    #connection and state management
    connection = Comm(config)
    print(dir(connection))
    connection.get_balance('usdt')


    exit()
    #Welcome screen
    helpers.loading(5, '[cyan]Trading bot starting...[/cyan]')
    helpers.clear()
    play("info")
    cprint(figlet_format('aBot', font='starwars'),
       'white', 'on_blue', attrs=['bold'])
 
    #variables
    orderId = None
    recentOrder = None

   #account Info
    # get balances for all assets & some account information
    if args.balance == 1:
        print(connection.client.get_account())
        input('Please enter to continue...')

    wallet = connection.client.get_asset_balance(asset=stake_currency)
    asset = connection.client.get_asset_balance(asset=symbol)

    if tradingCoin != 'BNB':
        play("alert")
        print('\n[black on white]Caution, you did not select BNB. The commusion will be %0.1 not %0.075[/]')
        answer = menu.yes_or_no("Please confirm:")
        if answer == False:
            exit()
        helpers.clear()
 
    commission =  0.075 if tradingCoin == 'BNB' else 0.1 #binance commission commission 0.1% All, 0.0750% BNB
  
    while True:
        #sleep for n seconds - avoid api violation
        time.sleep(args.loop)

        #remaining
        print('\n[black on white]Wallet/Assets[/]')
        t = PrettyTable(['Name', 'Free', 'Locked'])
        t.add_row([wallet['asset'], wallet['free'], wallet['locked']])
        t.add_row([asset['asset'], asset['free'], asset['locked']])
        print(t)

        wallet['locked'] = int(float(wallet['locked']))
        asset['free'] = int(float(asset['free']))
        #print("\n[green on white]Wallet/Assets:[/]", wallet, asset)

        # get balances for futures account
        #print(connection.client.futures_account_balance())

        # get balances for margin account
        #print(client.get_margin_account())

        try:
            klines = connection.client.get_klines(symbol=pairs, interval=interval, limit=config.limit)
        except Exception as exp:
            print(exp.status_code, flush=True)
            print(exp.message, flush=True)

        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]

        last_closing_price = close[-1]

        previous_closing_price = close[-2]

        ##orders info
        
        ordersAll = connection.client.get_all_orders(symbol=pairs, limit=10)
        openOrders = list(filter(lambda x: (x['status'] == 'NEW'), ordersAll)) 
       
        t = PrettyTable(['LCP', 'PCP', 'AO'])
        t.add_row([last_closing_price, previous_closing_price, len(openOrders)]) #, openOrders[0]['status'] if len(openOrders)>0 else 0 ])
        print(t)
 
        # if recentOrder is not None and len(recentOrder)>0:
        #     print('[green]Your orders[/green]')
        #     print('[blue]Recent order:[/blue]')
        #     t = PrettyTable(['SIDE', 'PRICE', 'QTY', 'STATUS'])
        #     t.add_row([recentOrder[0]['side'], recentOrder[0]['price'], recentOrder[0]['origQty'], openOrders[0]['status']])
        #     print(t)

        #orders full list
        if len(ordersAll) >= 1: # if recentOrder and len(recentOrder)>0 else 1:
            t = PrettyTable(['SIDE', 'PRICE', 'QTY', 'STATUS'])
            for i in range(len(ordersAll)):
                #if ordersAll[i]['status'] != 'NEW':
                t.add_row([ordersAll[i]['side'], ordersAll[i]['price'], ordersAll[i]['origQty'], ordersAll[i]['status']])
            print(t)
 
 
        close_array = np.asarray(close)
        close_finished = close_array[:-1]

        macd, macdsignal, macdhist = ta.MACD(close_finished, fastperiod=12, slowperiod=26, signalperiod=9)
        rsi = ta.RSI(close_finished, timeperiod=14)
        #print(rsi)
        #print(macd)
        if len(macd) > 0:
            last_macd = macd[-1]
            
            last_macd_signal = macdsignal[-1]

            previous_macd = macd[-2]
            previous_macd_signal = macdsignal[-2]

            rsi_last = rsi[-1]

            macd_cross_up = last_macd > last_macd_signal and previous_macd < previous_macd_signal

            print("Computed data:", macd_cross_up, rsi_last)
  
            ##coin info
            info = connection.client.get_symbol_info(pairs)
            #print("Asset Logic:",info,'--------------------------------------------------------------\n')
            minQty = int(float(info['filters'][3]['minNotional']))
            #print(minQty)
            #exit() 

            if len(openOrders)>0:
                #print("[blue on white]Open Orders:\n[/]",openOrders,"--------------------------------------------------------------------\n")
                pass

            if macd_cross_up and rsi_last > 49:
                print('[green]Buy now signal![/green]', minQty, last_closing_price * commission, flush=True)
                if lockLimit >= wallet['locked'] and len(openOrders) <= concurrentTradeLimit and maxTrade < asset['free']:
                    try:
                        if real == 1 and buyP == 1:
                            buy_limit = connection.client.create_order(
                                symbol=pairs,
                                side='BUY',
                                type='LIMIT',
                                timeInForce='GTC',
                                quantity=minQty,
                                price=last_closing_price)
                        elif real == 0 or buyP == 0:
                            buy_limit = [{
                                "symbol": pairs,
                                "side": 'BUY',
                                "type": 'LIMIT',
                                "timeInForce": 'GTC',
                                "quantity": minQty,
                                "price": last_closing_price #last_closing_price / commission -> this for more intelligent Will check.
                            }]

                        play('sent')
                        wallet['locked'] += minQty
                        print("Buy order completed:\n", buy_limit)

                    except BinanceAPIException as e:
                        # error handling goes here
                        print(e)
                    except BinanceOrderException as e:
                        # error handling goes here
                        print(e)
                else:
                    print('Locked Order:', wallet['locked'])

            
            if macd_cross_up == False and rsi_last < 30 and asset['free'] >= minQty:
                print('[red]Sale signal![/red]', minQty, last_closing_price * commission, flush=True)

                #cancel if pending order
                if len(openOrders) > 0 and real == 1:
                    print('[red]Deleting all pending orders..', len(openOrders))
                    #connection.client.cancel_orders(symbol=pairs) need to find some another way. API not has this endpoint.
                    
                    # result = connection.client.cancel_order(
                    # symbol=pairs,
                    # orderId=openOrders[0]['orderId']) #assuming 1 order at a time
                    #print('Deleting orders:', result)

                if lockLimit >= wallet['locked']:
                    try:
                        if real == 1 and sellP == 1:
                            sell_limit = connection.client.create_order(
                                symbol=pairs,
                                side='SELL',
                                type='LIMIT',
                                timeInForce='GTC',
                                quantity=asset['free'],
                                price=last_closing_price)
                        elif real == 0 or sellP == 0:
                            sell_limit = [{
                                "symbol": pairs,
                                "side": 'SELL',
                                "type": 'LIMIT',
                                "timeInForce": 'GTC',
                                "quantity": asset['free'], #sell all -> temporary. density required!
                                "price": last_closing_price * commission * 10
                            }]

                        play('sent')
                        wallet['locked'] += minQty
                        print("Sell order completed:\n", sell_limit)
 
                    except BinanceAPIException as e:
                        # error handling goes here
                        print(e)
                    except BinanceOrderException as e:
                        # error handling goes here
                        print(e)
                else:
                    print('Locked Order:', wallet['locked'])
