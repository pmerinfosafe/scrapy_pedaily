# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib
from scrapy_pedaily.items import PedailyIpoScrapyItem
import math

# 上市事件
class PedailyIpoSpider(scrapy.Spider):
    index = 8
    module_index =2
    name = 'pedaily_ipo'
    allowed_domains = ['pedaily.cn']
    start_urls = ['http://zdb.pedaily.cn/ipo/']
    base_url = 'http://zdb.pedaily.cn'

    def parse(self, response):
        print("**********", response.url)
        if response.status == 200:
            if response.url in self.start_urls:
                total_page_desc = response.css('span.title > span.total::text').extract_first()
                if total_page_desc.isdigit():
                    total_page = math.floor(int(total_page_desc) / 20) + int(math.fmod(int(total_page_desc), 20))
                    for pageNum in range(1, total_page + 1):
                    # for pageNum in range(1, 2):
                        url = response.url + 'p' + str(pageNum)
                        yield scrapy.Request(url, callback=self.parse)
                        # time.sleep(random.randint(1, 6))
                else:
                    self.logger.warning("has no next page!!!")
            else:
                id_prefix = '8-2'
                cate = '上市事件'
                info_list = response.css('div.box-news-list ul#ipo-list > li[class!="head"]')
                dr = re.compile(r'<[^>]+>', re.S)
                for info in info_list:
                    # print('date :', info.css('span.time::text').extract_first())
                    date = info.css('span.time::text').extract_first()
                    print('date:', date)
                    company = info.css('dt.company::text').extract_first()
                    if not company:
                        company = info.css('dt.company > a::text').extract_first()
                    print('company:', company)
                    print('industry:', info.css('dt.industry > a::text').extract_first())
                    industry = info.css('dt.industry > a::text').extract_first()
                    money = info.css('dt.money>span.d::text').extract_first()
                    unit = info.css('dt.money>span.m::text').extract_first()
                    print('money:', money)
                    print('unit:', unit)
                    place = info.css('dt.place > a::text').extract_first()
                    print('place:', place)

                    href = self.base_url + info.css('dt.view a::attr("href")').extract_first()
                    print('href', href)

                    yield scrapy.Request(href, meta={'id_prefix': id_prefix,
                                                     'category': cate,
                                                     'company': company,
                                                     'industry': industry,
                                                     'money': money,
                                                     'unit': unit,
                                                     'place': place,
                                                     'date': date},
                                         callback=self.parse_content)
                    time.sleep(random.randint(1, 6))

    def parse_content(self, response):
        print("#########", response.url)
        if response.status == 200:
            md5 = hashlib.md5()
            md5.update(response.url.encode(encoding='utf-8'))
            item = PedailyIpoScrapyItem()
            id_prefix = response.meta['id_prefix']
            item['id'] = id_prefix + "-" + md5.hexdigest()
            title_desc = response.css('div.info h1::text').extract_first()
            if title_desc:
                item['title'] = title_desc.strip()
            item['company'] = response.meta['company']
            item['financing_time'] = response.meta['date']
            item['industry'] = response.meta['industry']
            item['money'] = response.meta['money']
            item['unit'] = response.meta['unit']
            item['place'] = response.meta['place']
            #         item['investor'] = response.meta['investor']
            item['url'] = response.url
            infos = response.css('div.info ul> li')
            if infos:
                # 企业名称详情
                company_detail_desc = infos[0].css('li::text').extract_first()
                if company_detail_desc:
                    item['company_detail'] = company_detail_desc.strip()
                else:
                    company_detail_desc = infos[0].css('li a::text').extract_first()
                    if company_detail_desc:
                        item['company_detail'] = company_detail_desc.strip()
                    else:
                        item['company_detail'] = ''
                # 所属行业
                industry_desc = infos[1].css('li').extract_first()
                if industry_desc:
                    dr = re.compile(r'<[^>]+>', re.S)
                    dd = dr.sub('', industry_desc)
                    item['industry_desc'] = dd.replace(u'所属行业：', '')
                    # item['industry_desc'] = industry_desc.strip()
                # 投资方
                investor_desc = infos[2].css('li::text').extract_first()
                if investor_desc:
                    item['investor'] = investor_desc.strip()
                else:
                    investor_desc = infos[2].css('li a::text').extract_first()
                    if investor_desc:
                        item['investor'] = investor_desc.strip()
                    else:
                        item['investor'] = ''
                # 发行价
                offering_price = infos[4].css('li::text').extract_first()
                if offering_price:
                    item['offering_price'] = offering_price.strip()
                else:
                    item['offering_price'] = ''
                # 交易所
                stock_exchange_place_desc = infos[5].css('li::text').extract_first()
                if stock_exchange_place_desc:
                    item['stock_exchange_place'] = stock_exchange_place_desc.strip()
                else:
                    stock_exchange_place_desc = infos[5].css('li a::text').extract_first()
                    if stock_exchange_place_desc:
                        item['stock_exchange_place'] = stock_exchange_place_desc.strip()
                    else:
                        item['stock_exchange_place'] = ''
                # 发行量
                circulation_desc = infos[6].css('li::text').extract_first()
                if circulation_desc:
                    item['circulation'] = circulation_desc.strip()
                else:
                    item['circulation'] = ''
                # 股票代码
                stock_code_desc = infos[7].css('li::text').extract_first()
                if stock_code_desc:
                    item['stock_code'] = stock_code_desc.strip()
                else:
                    item['stock_code'] = ''
                # 是否支持 vc_pe
                vc_pe_support_desc = infos[8].css('li::text').extract_first()
                if vc_pe_support_desc:
                    item['vc_pe_support'] = vc_pe_support_desc.strip()
                else:
                    item['vc_pe_support'] = ''

            # print(item)
            yield item
