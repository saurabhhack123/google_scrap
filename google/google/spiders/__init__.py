# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import requests

import bs4
import csv
import urllib
import time
from scrapy import Selector
import re

class googleSpider(scrapy.Spider):
    name = "google"

    # 4 and 5 => use scrapy to dump table to csv 

    # utility function which is using scrapy to fetch content and crawl site
    # finally storing table in csv for all pages


    def start_requests(self):
        urls = [
            'https://play.google.com/store/apps/collection/promotion_3000e26_androidtv_apps_all?hl=en'
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
   
    def parse(self, response):
    	file_name = "playstore"
    	doc = bs4.BeautifulSoup(response.body,'html.parser').encode('ascii', 'ignore')
    	sel = Selector(text=doc, type="html")
    	# x='//div[@class="details"]//a'
    	div_quelist = response.xpath('//div[@class="details"]//a')
    	to_crawl = []
    	app_to_crawl = []
    	for div in div_quelist:
    		crawl = div.xpath('@href').extract()[0]
    		to_crawl.append(crawl)
        
        regex = re.compile(r'/store/apps/details')
    	app_to_crawl = list(set(filter(regex.search, to_crawl)))
    	print app_to_crawl
  
        app_for_api = []

        for link in app_to_crawl:
        	app_for_api.append(link[23:].encode('ascii', 'ignore'))

        print app_for_api

        payload = { "country": "US"}
        headers = {'Accept-Encoding': 'deflate, gzip'}

        for app_id in app_for_api:
        	response = requests.get("https://api.appmonsta.com/v1/stores/android/details/"+app_id+".json",
                        auth=("API_KEY", "X"),
                        params=payload,
                        headers=headers,
                        stream=True)
        	print response.status_code
        	for line in response.iter_lines():
        		print line
        		fo = open(app_id+".json", "w+")
        		fo.write(line)
        		fo.close
        	break