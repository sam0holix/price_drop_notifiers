import sys
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup 

def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

def price_in_int(string):
    price_list = (string[2:len(string)-3].split(','))
    price = ''
    for x in price_list:
        price+=x
    return int(price)

def ask_user():
    check = input('Do you want to get notified for price drops ? (y/n)')
    try:
        if check[0] == 'y':
            return True
        elif check[0] =='n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception:
        print('Please enter valid inputs')
        return ask_user()

    def mail_notifier():
        pass
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0","Cache-Control": "no-cache", "Pragma": "no-cache"}  #change this if you want to

if len(sys.argv)<2:
    print('Type -h for help')

elif sys.argv[1] == '-h':
    print('-u url           Enter the url of the product you want to visit. Ex. "www.example.com/product"')

elif sys.argv[1] == '-u':
    link = sys.argv[2]
    try:
        response=requests.get(link,headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content,'html.parser')
        title = soup.find(id="productTitle").get_text().strip()
        print(title)
        try:
            our_price = soup.find(id="priceblock_ourprice").get_text().strip()
            print(f'Price:{our_price}')
            our_price_int = price_in_int(our_price)
        except AttributeError as mrp_price:
            retail_price = soup.find(has_class_but_no_id,class_='priceBlockStrikePriceString').get_text().strip()
            print(f'Retail Price {retail_price}')
            retail_price_int = price_in_int(retail_price)
        try:
            deal_price = soup.find(id="priceblock_dealprice").get_text().strip()
            print(f'Offer Price:{deal_price}')
            deal_price_int = price_in_int(deal_price)
        except AttributeError as no_deal:
            print('Currently no deal is going on')
        
        ask_user()
    except HTTPError as http_err:
        err_string = str(http_err)[:16]
        print(f'{err_string}\n  Check your link again?')

