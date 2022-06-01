from lxml.html import fromstring
import requests
from datetime import datetime

import schedule
import time

URL = 'https://free-proxy-list.net/'

def get_proxies():
	response = requests.get(URL)
	parser = fromstring(response.text)
	proxies = set()

	for i in parser.xpath('//tbody/tr')[:]:
		if i.xpath('.//td[7][contains(text(),"yes")]'):
			proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
			proxies.add(proxy)
	return proxies


TIMEOUT = 3


def job():
	print(f"Collecting proxies {datetime.now()}")
	proxies = get_proxies()
	valid_proxies = []
	for proxy in proxies:
		try:
			response = requests.get(URL, proxies={"http": proxy, "https": proxy}, timeout=TIMEOUT)
			print(f'Good proxy: {proxy}')
			valid_proxies.append(proxy)
		except:
			print(f'Bad proxy: {proxy}')
	
	print(f'Saving proxies ({len(valid_proxies)}):{valid_proxies}')
	output = open('scraper/tmp/proxies.txt', 'w')
	for p in valid_proxies:
		output.write(p + '\n')
	output.close()

job()
schedule.every(2).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)


