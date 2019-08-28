import csv
import requests
import time
from bs4 import BeautifulSoup

with open('./csv2.csv', newline='') as f:
    stocks = []
    path = './rank.csv'
    
    reader = csv.reader(f)

    for row in reader:
        url = "https://www.bloomberg.co.jp/quote/" + row[0] + ":US"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # 値上がりと値下がりでDOM要素が変わる
        price = soup.select("#content > div > div > div.basic-quote > div > div.price-container.down > div.price") 
        price2 = soup.select("#content > div > div > div.basic-quote > div > div.price-container.up > div.price")
        payout = soup.select_one("#content > div > div > div.detailed-quote.show > div > div > div:nth-child(13) > div.cell__value.cell__value_")
        payout2 = soup.select_one("#content > div > div > div.detailed-quote.show > div > div > div:nth-child(15) > div.cell__value.cell__value_")

        # 配当利回りもDOMが違うことがある
        if payout is None:
            payout = payout2

        if len(price) == 0:
            price = price2

        payout = payout.string.strip()
        price_int = float(price[0].string)
        payout_int = float(payout.rstrip("%"))

        stock = {'tip':row[0], 'price':price_int, 'payout':payout, 'payout_int':payout_int}
        stocks.append(stock)

    stocks = sorted(stocks, key=lambda x:-x['payout_int'])
    print(stocks)

    path_w = './rank.txt'

    for r in stocks:
        with open(path_w, mode='a') as f:
            f.write(r['tip'] + ',' + str(r['price']) + ',' + str(r['payout']))
            
