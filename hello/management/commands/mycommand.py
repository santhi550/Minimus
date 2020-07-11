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
def check_price(soup,amount,user_id):
  title = soup.find(id= "productTitle").get_text()
  pre=soup.find(id = "priceblock_saleprice")
  if pre is None:
	  pre=soup.find(id = "priceblock_ourprice")
  price =pre.get_text().replace(',', '').replace('₹', '').replace(' ', '').strip()
  #print(price)

  #converting the string amount to float
  converted_price = float(price[0:5])
  wp=WebPushDevice.objects.filter(user_id=user_id,active=True)
  if converted_price < amount:
	  wp.send_message("Dear user, your price for the "+title.strip()+" has been decreased , so Book the product as early as possible") 


def mainprogram(url,amount,user_id):
	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.content, 'html.parser')
	soup.encode('utf-8')
	check_price(soup,amount,user_id)

while(True):
  items_list=Items.objects.all()
  print("Tracking")
  for item in items_list:
    print(item.url)
    mainprogram(item.url,item.amount,item.user_id) 
  time.sleep(5)
