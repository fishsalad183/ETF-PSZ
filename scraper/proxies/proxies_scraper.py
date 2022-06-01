from lxml.html import fromstring
import requests
from datetime import datetime
import time

URL = 'https://free-proxy-list.net/'

def scrape_proxies():
	response = requests.get(URL)
	parser = fromstring(response.text)
	proxies = set()

	for i in parser.xpath('//tbody/tr')[:]:
		if i.xpath('.//td[7][contains(text(),"yes")]'):
			proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
			proxies.add(proxy)
	return proxies


TIMEOUT = 3
OUTPUT_FILE = 'scraper/tmp/proxies.txt'

def collect_proxies():
	print(f"Collecting proxies {datetime.now()}")
	proxies = scrape_proxies()
	valid_proxies = []
	for proxy in proxies:
		try:
			response = requests.get(URL, proxies={"http": proxy, "https": proxy}, timeout=TIMEOUT)
			print(f'Good proxy: {proxy}')
			valid_proxies.append(proxy)
		except:
			print(f'Bad proxy: {proxy}')
	
	print(f'Saving proxies ({len(valid_proxies)}) : {valid_proxies}')
	output = open(OUTPUT_FILE, 'w')
	for p in valid_proxies:
		output.write(p + '\n')
	output.close()


while True:
    collect_proxies()
    time.sleep(120)
