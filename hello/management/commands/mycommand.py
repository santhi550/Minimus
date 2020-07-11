# Amazon product price tracker using Python 
from django.core.management.base import BaseCommand, CommandError
# importing libraries 
import schedule 
from push_notifications.models import WebPushDevice 
from hello.models import Items
import requests
from bs4 import BeautifulSoup
import time
import types
# set the headers and user string
# headers = {
# "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
# }

# function to check if the price has dropped below 20,000
def check_price(soup,amount,user_id,user_availability):
  # title = soup.find(id= "productTitle").get_text()
  pre=soup.find('span',id = "priceblock_ourprice")
  print(pre)
  if pre is None:
    pre=soup.find('span',id = "priceblock_saleprice")
    print(pre)
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
  site='https://www.amazon.in/gp/sign-in.html'

  session = requests.Session()
  
  '''define session headers'''
  session.headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Referer': site
  }

  resp = session.get(site)
  html = resp.text
  
  '''get BeautifulSoup object of the html of the login page'''
  soup = BeautifulSoup(html , 'lxml')
  data = {}
  form = soup.find('form', {'name': 'signIn'})
  for field in form.find_all('input'):
    try:
        data[field['name']] = field['value']
    
    except:
        pass
  data[u'email'] = 'santhikiran2000@gmail.com'
  data[u'password'] = 'spring@123'
  post_resp = session.post('https://www.amazon.in/ap/signin', data = data)
  #print(soup.prettify())
  post_soup = BeautifulSoup(post_resp.content , 'lxml')
  
  if post_soup.find_all('title')[0].text == 'Your Account':
      print('Login Successfull')
  else:
      print('Login Failed')
  try:
    response = requests.get(url, headers=session.headers,timeout=600)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(response)
    soup.encode('utf-8')
    check_price(soup,amount,user_id,availability)
  except:
    pass
  session.close()

while(True):
  items_list=Items.objects.all()
  # print("Tracking")
  for item in items_list:
    print(item.url)
    mainprogram(item.url,item.amount,item.user_id,item.availability) 
  time.sleep(5)