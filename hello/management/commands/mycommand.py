# Amazon product price tracker using Python 
from django.core.management.base import BaseCommand, CommandError
# importing libraries 
import schedule 
from push_notifications.models import WebPushDevice 
from hello.models import Items
import requests
from bs4 import BeautifulSoup
import time

# set the headers and user string
headers = {
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}


#print(soup.prettify())

# function to check if the price has dropped below 20,000
def check_price(soup,amount,user_id,user_availability):
  # title = soup.find(id= "productTitle").get_text()
  pre=""
  try:
    pre=soup.find(id = "priceblock_ourprice")
    print(pre)
  except:
    pass
  try:
    pre=soup.find(id = "priceblock_saleprice")
    print(pre)
  except:
    pass
  print(pre)
  price =pre.get_text().replace(',', '').replace('₹', '').replace(' ', '').strip()
  #print(price)
  availability=soup.find(id="availability").get_text().strip()
  # print(availability)
  #converting the string amount to float
  converted_price = float(price[0:5])
  wp=WebPushDevice.objects.filter(user_id=user_id,active=True)
  if user_availability and amount ==0:
    if availability == 'In stock.':
      wp.send_message("Dear user, the given product is in STOCK ,so book the product as soon as possible")
  elif user_availability== False and amount > 0:
    if converted_price < amount:
      wp.send_message("Dear user, price for the given product has been DECREASED , so book the product as soon as possible")
  elif user_availability and amount > 0:
    if availability == 'In stock.' and converted_price < amount:
      wp.send_message("Dear user, the given product is in STOCK and its price has been DECREASED , so Book the product as soon as possible")


def mainprogram(url,amount,user_id,availability):
	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.content, 'html.parser')
	soup.encode('utf-8')
	check_price(soup,amount,user_id,availability)

while(True):
  items_list=Items.objects.all()
  # print("Tracking")
  for item in items_list:
    print(item.url)
    mainprogram(item.url,item.amount,item.user_id,item.availability) 
  time.sleep(1)
