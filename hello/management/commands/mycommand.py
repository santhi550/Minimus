# Amazon product price tracker using Python 
from django.core.management.base import BaseCommand, CommandError
# importing libraries 
import bs4 as bs 
import sys 
import schedule 
import time 
import urllib.request 
from PyQt5.QtWebEngineWidgets import QWebEnginePage 
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtCore import QUrl 
from push_notifications.models import WebPushDevice 
from hello.models import Items
import re

class Page(QWebEnginePage): 

	def __init__(self, url): 
		self.app = QApplication(sys.argv) 
		QWebEnginePage.__init__(self) 
		self.html = '' 
		self.loadFinished.connect(self._on_load_finished) 
		self.load(QUrl(url)) 
		self.app.exec_() 

	def _on_load_finished(self): 
		self.html = self.toHtml(self.Callable) 
		print('Load finished') 

	def Callable(self, html_str): 
		self.html = html_str 
		self.app.quit() 

def exact_url(url): 
	index = url.find("B0") 
	index = index + 10
	current_url = "" 
	current_url = url[:index] 
	return current_url 
	

def mainprogram(url,amount,user_id): 
	url = url
	exacturl = exact_url(url) # main url to extract data 
	page = Page(exacturl) 
	soup = bs.BeautifulSoup(page.html, 'html.parser') 
	js_test = soup.find('span', id ='priceblock_ourprice') 
	if js_test is None: 
		js_test = soup.find('span', id ='priceblock_saleprice')		 
	str = "" 
	
	for line in js_test.stripped_strings : 
		str = line 

	# convert to integer 
	#str = str.replace(", ", "")
	
	current_price = float(re.sub(r"[^\d.]", "", str))
	your_price = int(amount)
	wp=WebPushDevice.objects.get(user_id=user_id)
	if current_price < your_price : 
		wp.send_message("Dear user, your price for the given product has been decreased , so Book the product as early as possible") 
	
def job(): 
	print("Tracking....")
	items_list=Items.objects.all()
	for item in items_list:
		print(item)
		mainprogram(item.url,item.amount,item.user_id) 

# main code 
schedule.every(1).minutes.do(job) 

while True: 
	schedule.run_pending() 
	time.sleep(1) 
