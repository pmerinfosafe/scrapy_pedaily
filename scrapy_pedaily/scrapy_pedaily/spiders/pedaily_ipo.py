# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib
from pedailyprj.items import PedailyIpoScrapyItem

# 上市事件
class PedailyIpoSpider(scrapy.Spider):
    index = 8
    module_index =2
    name = 'pedaily_ipo'
    allowed_domains = ['pedaily.cn']
    start_urls = ['http://zdb.pedaily.cn/ipo/']
    category_index = {'ipo': '2'}
    category_desc = {'ipo': '上市事件'}
    url_descs = ['上市事件']
    industry_classification = {'h5537': '互联网',
                               # 'h4823': '移动互联网', 'h690': 'IT', 'h4973': '房地产',
                               # 'h5044': '汽车', 'h119': '连锁及零售', 'h1154': '能源及矿产', 'h1381': '广播电视',
                               # 'h2164': '娱乐传媒', 'h2359': '物流', 'h2869': '教育与培训', 'h2947': '清洁技术',
                               # 'h3052': '农林牧渔', 'h3362': '金融', 'h3456': '食品&饮料', 'h3601': '半导体',
                               # 'h3622': '医疗健康', 'h4023': '机械制造', 'h4238': '化工原料', 'h4971': '建筑工程',
                               # 'h5643': '纺织及服装', 'h5851': '光电设备', 'h2861': '其他'
                               }
    industry_classification_url = ['h5537',
                                   # 'h4823', 'h690', 'h4973',
                                   # 'h5044', 'h119', 'h1154', 'h1381',
                                   # 'h2164', 'h2359', 'h2869', 'h2947',
                                   # 'h3052', 'h3362', 'h3456', 'h3601',
                                   # 'h3622', 'h4023', 'h4238', 'h4971',
                                   # 'h5643', 'h5851', 'h2861'
                                   ]
    base_url = 'http://zdb.pedaily.cn'

    def parse(self, response):
        print("**********", response.url)
        if response.status == 200:
            id_prefix = ''
            cate = ''
            industry_cate = ''
            if response.url in self.start_urls:
                cate_index = self.start_urls.index(response.url)
                id_prefix = str(self.index) + '-' + str(self.module_index)
                cate = self.url_descs[cate_index]
                for part_url in self.industry_classification_url:
                    url = response.url + part_url
                    industry_cate = self.industry_classification.get(part_url)
                    yield scrapy.Request(url, meta={'id_prefix': id_prefix, 'category': cate,
                                                    'industry_cate': industry_cate}, callback=self.parse)
            else:
                id_prefix = response.meta['id_prefix']
                cate = response.meta['category']
                industry_cate = response.meta['industry_cate']
                # next_page_link = response.css('div.page-list.page > a.next')
                next_page_link = response.css('div.page-list.page').xpath('//a[contains(.,"下一页")]')
                if next_page_link:
                    url = self.base_url + next_page_link.css('::attr("href")').extract_first()
                    print("#%%%%%%%%%", response.css('div.page-list.page > a.next').extract())
                    yield scrapy.Request(url, meta={'id_prefix': id_prefix, 'category': cate,
                                                    'industry_cate': industry_cate}, callback=self.parse)
                    time.sleep(3)

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
                                                     'industry_cate': industry_cate,
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
            item['industry_cate'] = response.meta['industry_cate']
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
