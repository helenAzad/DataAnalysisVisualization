import pandas as pd
import requests
from bs4 import BeautifulSoup
import copy
import csv
import datetime
import os
import json
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib import dates as mpl_dates
import colorama
from colorama import init, Fore, Style
import warnings

warnings.filterwarnings('ignore')

def main_func():
    headers= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests' : '1',
        'Cache-Control' : 'max-age=0'
    }
    # corect below code...
    baseurl = "https://www.coingecko.com/?page=1"
    tables = []
    for i in range(1, 4):
        # print('processing page {0}'.format(i))
        params = {
            'page' : i
        }
        rseponse = requests.get(baseurl, headers = headers ,params=params)
        soup = BeautifulSoup(rseponse.content, 'html.parser')
        tables.append(pd.read_html(str(soup))[0])
    master_table = pd.concat(tables)
    master_table['name'] = master_table['Coin'].apply(lambda x: x.split()[0])
    master_table['symbol'] = master_table['Coin'].apply(lambda x: x.split()[1])
    return master_table

def add_crypto(coin):
    master_table = main_func()
    result1 = (master_table['symbol'] == coin).any()
    result2 = (master_table['name'] == coin).any()
    if(result1):
        print(Fore.GREEN + "added successfuly" + Style.RESET_ALL)
        res = master_table[master_table['symbol'] == coin]
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        timee = now.strftime("%H:%M:%S")
        hour = now.hour
        datetimee = now.strftime("%Y-%m-%d %H:%M:%S")
        res['datetime'] = [str(datetimee)]
        res['date'] = [str(date)]
        res['time'] = [str(timee)]
        res['hour'] = [str(hour)]
        res['Price'] = res['Price'].str.replace('$', '')
        if os.path.isfile('added_crypto.csv'):
            res.to_csv('added_crypto.csv', mode='a', header=False, index=False)
        else:
            res.to_csv('added_crypto.csv', index=False)
    elif(result2):
        print(Fore.GREEN + "added successfuly",  + Style.RESET_ALL)
        res = master_table[master_table['name'] == coin]
        if os.path.isfile('added_crypto.csv'):
            res.to_csv('added_crypto.csv', mode='a', header=False, index=False)
        else:
            res.to_csv('added_crypto.csv', index=False)
    else:
        print(Fore.RED + "this crypto does not exist." + Style.RESET_ALL)
    
def see_the_price():
    with open('added_crypto.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(Fore.BLUE + row[-5] + " , " + row[-6] + Style.RESET_ALL)
    print(Fore.YELLOW + "write coins that you want to see their price:(press E to exit)" + Style.RESET_ALL)
    see = input()
    lisee = []
    while(see != "E"):
        with open('added_crypto.csv', 'r') as file:
            reader = csv.reader(file)
            flag = False
            for row in reader:
                if see in row:
                    flag = True
                    lisee.append((see))
                    break
            if flag == False:
                print(Fore.RED +"this coin does not exist in the added crypto list." + Style.RESET_ALL)
        see= input()
    lisee.sort(key=str.lower)
    master_table = main_func() 
    if len(lisee) == 0:
        print(Fore.RED + "no coin to show" + Style.RESET_ALL)
    else:
        with open('see_crypto.csv', 'w', newline='') as file:
            header = ['name', 'symbol', 'Price', 'date', 'time']
            writer = csv.writer(file)
            writer.writerow(header)
        for seee in lisee:
            result1 = (master_table['symbol'] == seee).any()
            result2 = (master_table['name'] == seee).any()
            if(result1):
                sym = master_table.loc[master_table['symbol'] == seee, 'symbol']
                nm = master_table.loc[master_table['symbol'] == seee, 'name']
                res = master_table.loc[master_table['symbol'] == seee, 'Price']
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S") 
                data = pd.DataFrame({
                    'name':[str(nm).split()[1]], 
                    'symbol' :[str(sym).split()[1]], 
                    'Price' :[str(res).split()[1]], 
                    'date' :[str(date)], 
                    'time' :[str(time)]
                })
                print(Fore.BLUE + data + Style.RESET_ALL)
                data.to_csv('see_crypto.csv', mode='a', header=False, index=False)

            elif(result2):
                sym = master_table.loc[master_table['name'] == coin, 'symbol']
                nm = master_table.loc[master_table['name'] == coin, 'name']
                res = master_table.loc[master_table['name'] == coin, 'Price']
                now = datetime.datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S") 
                data = pd.DataFrame({
                    'name':[str(nm).split()[1]], 
                    'symbol' :[str(sym).split()[1]], 
                    'Price' :[str(res).split()[1]], 
                    'date' :[str(date)], 
                    'time' :[str(time)]
                })
                print(Fore.BLUE + data + Style.RESET_ALL)
                data.to_csv('see_crypto.csv', mode='a', header=False, index=False)

def see_the_chart(coin):
    flag = False
    df = pd.DataFrame()
    df = pd.read_csv('added_crypto.csv')
    result1 = (master_table['symbol'] == coin).any()
    timeli = []
    if(result1):
        mask = df['symbol'] == coin
        matching_rows = df.loc[mask]
        matching_rows['date'] = pd.to_datetime(matching_rows['date'])
        mean_prices = matching_rows.groupby(['date', 'hour'])['Price'].mean().reset_index()
        matching_rows = pd.merge(matching_rows, mean_prices, on=['date', 'hour'])
        matching_rows = matching_rows.drop_duplicates(subset=['date', 'hour'])
        df = df.drop_duplicates(subset=['date', 'hour'])
        # print("matching_rows :")
        # print(matching_rows)
        # print("df :")
        # print(df)
        # matching_rows['Price'] = matching_rows['Price'].astype(float)
        matching_rows['Price_x'] = pd.to_numeric(matching_rows['Price_x'],errors='coerce')
        matching_rows.plot(x= 'datetime', y='Price_x', kind='bar')
        plt.show()
        os.remove('added_crypto.csv')
        df.to_csv('added_crypto.csv', index=False)
    else:
        print(Fore.RED + "there os no data for this coin." + Style.RESET_ALL)
    
def CRUD_favarite_crypto():

    with open('added_crypto.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(Fore.BLUE + row[-5] + " , " + row[-6] + Style.RESET_ALL)

    print(Fore.YELLOW + "write d for delete a for add and s to show your favorite cryptoes" + Style.RESET_ALL)
    crud = input()
    if crud == 'd':
        delete = input("enter your coin that you want to delete: ")
        with open('favorite_crypto.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader, None)
            flag = False
            index = 0
            for row in reader:
                if delete in row:
                    flag = True
                    break
                index = index + 1
            rows = list(reader)
            del rows[row_index]
            os.remove('favorite_crypto.csv')
            with open("favorite_crypto.csv", 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(rows)

            print(Fore.BLUE + "your entered coin has been deleted from favorite_crypto.csv" + Style.RESET_ALL)
 

    elif crud == 's':
        print(Fore.BLUE + "FAVORITE COINS :")
        with open('favorite_crypto.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                print(row)
            print("----------------------" + Style.RESET_ALL)
    elif crud == 'a':
        fav = input("write yout fav coin(symbol or name): ")
        with open('added_crypto.csv', 'r') as file:
            reader = csv.reader(file)
            flag = False
            for row in reader:
                if fav in row:
                    flag = True
                    break

        if flag == True:

            result1 = (master_table['symbol'] == fav).any()
            result2 = (master_table['name'] == fav).any()
            if(result1):
                sym = master_table.loc[master_table['symbol'] == fav, 'symbol']
                nm = master_table.loc[master_table['symbol'] == fav, 'name']
                res = master_table.loc[master_table['symbol'] == fav, 'Price'] 
                data = pd.DataFrame({
                    'name':[str(nm).split()[1]], 
                    'symbol' :[str(sym).split()[1]], 
                    'Price' :[str(res).split()[1]] 
                })
                data.to_csv('favorite_crypto.csv', mode='a', header=False, index=False)

            elif(result2):
                sym = master_table.loc[master_table['name'] == fav, 'symbol']
                nm = master_table.loc[master_table['name'] == fav, 'name']
                res = master_table.loc[master_table['name'] == fav, 'Price']
                data = pd.DataFrame({
                    'name':[str(nm).split()[1]], 
                    'symbol' :[str(sym).split()[1]], 
                    'Price' :[str(res).split()[1]]
                })
                data.to_csv('favorite_crypto.csv', mode='a', header=False, index=False)
        else:
            print(Fore.RED + "this coin does not exist in your added list " + Style.RESET_ALL)
    else:
        print(Fore.RED + "please enter a correct symbol" + Style.RESET_ALL)

def construct_download_url(
    ticker,
    period1,
    period2,
    interval='monthly'
):
    """
    :period1 & period2: 'yyyy-mm-dd'
    :interval: {daily, weekly, monthly}
    """
    def convert_to_seconds(period):
        datetime_value = datetime.strptime(period, '%Y-%m-%d')
        total_seconds = int(time.mktime(datetime_value.timetuple())) + 86400
        return total_seconds
    try: 
        interval_reference = {'daily' : '1d', 'weekly' : '1wk', 'monthly': '1mo'}
        _interval = interval_reference.get(interval)
        if _interval is None:
            print('interval code is incorrect')
            return 
        p1 = convert_to_seconds(period1)
        p2 = convert_to_seconds(period2)
        url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={p1}&period2={p2}&interval={_interval}&filter=history'
        return url
    except Exception as e:
        print(e)
        return 

def Review_the_chart():
    day = int(input("please enter the number of your day that you want to see in your chart: "))
    while day > 30 or day < 2:
        print(Fore.RED + "your input in out of context, please enter a number between 2 and 30: " + Style.RESET_ALL)
        day = int(input())
    number = int(input("Enter the number of your desired symbol: "))
    print(Fore.YELLOW + "ENTER youe desired symbol: " + Style.RESET_ALL)
    fig, axs = plt.subplots(number)
    min_perc = x = float('inf')
    best_coin = ""
    for i in range(1 , number + 1):
        symm = input()
        mycoin = symm + '-USD'
        now = datetime.now()
        sec_time = datetime.now() - timedelta(days= day)
        query_url = construct_download_url(mycoin, sec_time.strftime("%Y-%m-%d"), now.strftime('%Y-%m-%d'), 'daily')
        data = pd.read_csv(query_url)
        # print(data)
        csv_name = mycoin + '.csv'
        flag1 = False
        if os.path.isfile(csv_name):
            if sec_time.strftime("%Y-%m-%d") in data['Date'].values and now.strftime('%Y-%m-%d') in data['Date'].values:
                flag1 = True
                df = pd.read_csv(csv_name)
                index = df['Date'].index[df['Date'] == now.strftime('%Y-%m-%d')][0]
                # print("index : ", index)
                df = pd.read_csv(csv_name)
                selected_rows = df['Date'][index:index + day + 1]
                price_date = data['Date']
                price_close = data['Close']
                data['pct_change'] = data['Close'].pct_change() * 100
                sum_a = data['pct_change'].sum()
                print('pct-change :', sum_a)
                # print(Fore.BLUE + 'pct-change :', sum_a + Style.RESET_ALL)
                if(sum_a < min_perc):
                    min_perc = sum_a
                    best_coin = symm
                axs[i-1].step(price_date, price_close)
                # axs[i].set_xticklabels(price_date, rotation=45, ha='right')
                axs[i-1].set_xlabel('Date')
                axs[i-1].set_ylabel(symm)

        if flag1 == False:
            if(os.path.isfile(csv_name)):
                os.remove(path)
            data.to_csv(csv_name, index=False)
            price_date = data['Date']
            price_close = data['Close']
            data['pct_change'] = data['Close'].pct_change() * 100
            sum_a = data['pct_change'].sum()
            print('pct-change :', sum_a)
            # print(Fore.BLUE + 'pct-change :', sum_a + Style.RESET_ALL)
            if(sum_a < min_perc):
                min_perc = sum_a
                best_coin = symm 
            axs[i-1].step(price_date, price_close)
            # axs[i].set_xticklabels(price_date, rotation=45, ha='right')
            axs[i-1].set_xlabel('Date')
            axs[i-1].set_ylabel(symm)
            # axs[i].set_title('Step Chart with Date X-Axis')
    fig.tight_layout()
    plt.show()
    print(Fore.BLUE + f"{symm} has the maximum percent changability with {min_perc}% so it is a good idea to buy it." + Style.RESET_ALL)

# # Index(['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], dtype='object')

master_table = main_func()
# if os.path.isfile('see_crypto.csv'):
    # os.remove('seeed_crypto.csv')

with open('favorite_crypto.csv', 'w', newline='') as file:
    header = ['name', 'symbol', 'Price']
    writer = csv.writer(file)
    writer.writerow(header)
print(Fore.YELLOW, "Add the desired coin to your list and press the Q button to exit")
print("number 1: add crypto")
print("number 2: see the price of my desired crypto")
print("number 3: see the chart")
print("number 4: CRUD for favorite crypto")
print("number 5: Review a chart" + Style.RESET_ALL)
number = input("According to the above, enter the desired number: ")

while(number.isdigit()):
    if(int(number) == 1):
        added_crypto = pd.DataFrame(columns = master_table.columns)
        coin = str(input("Enter your ideal symbol or name:"))
        add_crypto(coin)

    elif(int(number) == 2):
        if os.path.isfile('added_crypto.csv'):
            see_the_price()
        else:
            print(Fore.RED + "there is no entered coin, please first add coin" + Style.RESET_ALL)

    elif(int(number) == 3):
        if os.path.isfile('added_crypto.csv'):
            coin = input(Fore.YELLOW + "inupt your coin to see its chart: " + Style.RESET_ALL)
            see_the_chart(coin)
        else:
            print(Fore.RED + "there is no entered coin, please first add coin" + Style.RESET_ALL)

    elif(int(number) == 4):
        if os.path.isfile('added_crypto.csv'):
            master_table = main_func()
            CRUD_favarite_crypto()
            df = pd.read_csv('favorite_crypto.csv')
            print(Fore.BLUE + "this is your favorite list: ")
            print(df  + Style.RESET_ALL)
        else:
            print(Fore.RED + "there is no entered coin, please first add coin" + Style.RESET_ALL)

    elif(int(number) == 5):
        if os.path.isfile('added_crypto.csv'):
            Review_the_chart()
        else:
            print(Fore.RED + "there is no entered coin, please first add coin" + Style.RESET_ALL)

    number = input("Enter your number: ")