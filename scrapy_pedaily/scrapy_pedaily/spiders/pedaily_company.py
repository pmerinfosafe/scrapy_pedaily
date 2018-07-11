# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib
from scrapy_pedaily.items import PedailyPeScrapyItem
import math

class PedailyCompanySpider(scrapy.Spider):
    index = 8
    module_index = 5
    name = 'pedaily_company'
    allowed_domains = ['pedaily.cn']
    start_urls = ['http://zdb.pedaily.cn/company/p1/']
    category_index = {'company': '5'}
    category_desc = {'company': '投资机构'}
    url_descs = ['投资机构']
    base_url = 'http://zdb.pedaily.cn'
    comapys_base_url = 'http://zdb.pedaily.cn/company/p{}/'

    def parse(self, response):
        print("**********", response.url)
        if response.status == 200:
            if response.url in self.start_urls:
                total_page_desc = response.css('span.title > span.total::text').extract_first()
                if total_page_desc.isdigit():
                    total_page = math.floor(int(total_page_desc) / 20) + int(math.fmod(int(total_page_desc), 20))
                    for pageNum in range(1, total_page + 1):
                        url = self.comapys_base_url.format(str(pageNum))
                        print(url)
                        # yield scrapy.Request(url, callback=self.parse)
                        # time.sleep(random.randint(1, 6))
                else:
                    self.logger.warning("has no next page!!!")
