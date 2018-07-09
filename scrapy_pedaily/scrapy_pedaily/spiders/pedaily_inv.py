# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib
from scrapy_pedaily.items import PedailyInvScrapyItem
import requests
import math
import logging


# 投资事件
class PedailyInvSpider(scrapy.Spider):
    logger = logging.getLogger(__name__)
    index = 8
    name = 'pedaily_inv'
    allowed_domains = ['pedaily.cn']
    start_urls = ['http://zdb.pedaily.cn/inv/']
    base_url = 'http://zdb.pedaily.cn'
    def parse(self, response):
        print("**********", response.url)
        if response.status == 200:
            if response.url in self.start_urls:
                total_page_desc = response.css('span.title > span.total::text').extract_first()
                if total_page_desc.isdigit():
                    total_page = math.floor(int(total_page_desc) / 20) + int(math.fmod(int(total_page_desc), 20))
                    for pageNum in range(1, total_page + 1):
                        url = response.url + 'p' + str(pageNum)
                        # print(url)
                        yield scrapy.Request(url, callback=self.parse)
                        time.sleep(random.randint(1, 6))
                else:
                    self.logger.warning("has no next page!!!")
            else:
                id_prefix = '8-1'
                cate = '投资事件'
                info_list = response.css('div.box-news-list ul#inv-list > li[class!="head"]')
                dr = re.compile(r'<[^>]+>', re.S)
                for info in info_list:
                    date = info.css('span.time::text').extract_first()
                    company = info.css('dt.company::text').extract_first()
                    if not company:
                        company = info.css('dt.company > a::text').extract_first()
                    industry = info.css('dt.industry > a::text').extract_first()
                    inv_cate = info.css('span.r::text').extract_first()
                    acc_cate = info.css('span.d::text').extract_first()
                    acc_num = info.css('span.m::text').extract_first()
                    investor_desc = info.css('dt.group').extract_first()
                    investor = dr.sub('', investor_desc)

                    href = self.base_url + info.css('dt.view a::attr("href")').extract_first()

                    yield scrapy.Request(href, meta={'id_prefix': id_prefix,
                                                     'category': cate,
                                                     'company': company,
                                                     'industry': industry,
                                                     'inv_cate': inv_cate,
                                                     'acc_cate': acc_cate,
                                                     'acc_num': acc_num,
                                                     'investor': investor,
                                                     'date': date},
                                         callback=self.parse_content)
                    time.sleep(random.randint(1, 6))

    def parse_content(self, response):
        print("#########", response.url)
        if response.status == 200:
            md5 = hashlib.md5()
            md5.update(response.url.encode(encoding='utf-8'))
            item = PedailyInvScrapyItem()
            id_prefix = response.meta['id_prefix']
            item['id'] = id_prefix + "-" + md5.hexdigest()
            title_desc = response.css('div.info h1::text').extract_first()
            if title_desc:
                item['title'] = title_desc.strip()
            item['company'] = response.meta['company']
            item['financing_time'] = response.meta['date']
            item['industry'] = response.meta['industry']
            item['inv_cate'] = response.meta['inv_cate']
            item['acc_cate'] = response.meta['acc_cate']
            item['acc_num'] = response.meta['acc_num']
            item['investor'] = response.meta['investor']
            item['url'] = response.url
            # 详情页解析
            financing_party = response.css('div.info ul>li.full::text').extract_first()
            if financing_party and len(financing_party) >= 2:
                item['financing_party'] = financing_party.strip()
            else:
                financing_party = response.css('div.info ul>li.full > a::text').extract_first()
                if financing_party:
                    item['financing_party'] = financing_party.strip()
                else:
                    item['financing_party'] = ''

            ind_desc = response.css('div.info ul>li:last-child').extract_first()
            if ind_desc:
                dr = re.compile(r'<[^>]+>', re.S)
                dd = dr.sub('', ind_desc)
                item['industry_desc'] = dd.replace(u'所属行业：', '')
            item['short_detail'] = response.css('div#desc > p::text').extract_first()
            yield item
