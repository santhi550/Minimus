# Amazon product price tracker using Python 

# importing libraries 
import bs4 as bs 
import sys 
import schedule 
import time 
import urllib.request 
from PyQt5.QtWebEngineWidgets import QWebEnginePage 
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtCore import QUrl 
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
	

def mainprogram(): 
	url = "https://www.amazon.in/Tarkan-Rugged-Charging-Android-Supports/dp/B07YB9R3W2/ref=lp_1389401031_1_1_sspa?s=electronics&ie=UTF8&qid=1594367074&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExTjlYT084S0lIR1kxJmVuY3J5cHRlZElkPUEwMDYyMjc0MkQzM01ZQVZSNDg3RSZlbmNyeXB0ZWRBZElkPUEwNDQzODg0MUdGT1AzSTUyMUpMVyZ3aWRnZXROYW1lPXNwX2F0Zl9icm93c2UmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl"
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
	your_price = 600
	if current_price < your_price : 
		print("Price decreased book now") 
	else: 
		print("Price is high please wait for the best deal") 
	
def job(): 
	print("Tracking....")	 
	mainprogram() 

# main code 
schedule.every(1).minutes.do(job) 

while True: 
	schedule.run_pending() 
	time.sleep(1) 
