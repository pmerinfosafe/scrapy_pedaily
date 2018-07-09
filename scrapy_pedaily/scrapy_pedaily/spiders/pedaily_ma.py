# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib
from scrapy_pedaily.items import PedailyMaScrapyItem
import math
# 并购事件
class PedailyMaSpider(scrapy.Spider):
    index = 8
    module_index = 3
    name = 'pedaily_ma'
    allowed_domains = ['pedaily.cn']
    start_urls = ['http://zdb.pedaily.cn/ma/']
    category_index = {'ma': '3'}
    category_desc = {'ma': '并购事件'}
    url_descs = ['并购事件']
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
                id_prefix = '8-3'
                cate = '并购事件'
                info_list = response.css('div.box-item-list ul#inv-list > li[class!="head"]')
                dr = re.compile(r'<[^>]+>', re.S)
                for info in info_list:
                    date = info.css('span.time::text').extract_first()
                    company = info.css('dt.company::text').extract_first()
                    if not company:
                        company = info.css('dt.company > a::text').extract_first()
                    industry = info.css('dt.industry > a::text').extract_first()
                    acc_cate = info.css('span.r::text').extract_first()
                    acc_num = info.css('span.d::text').extract_first()
                    investor_desc = info.css('dt.company2::text').extract_first()
                    if investor_desc:
                        investor = investor_desc.strip()
                    else:
                        investor_desc = info.css('dt.company2 > a::text').extract_first()
                        if investor_desc:
                            investor = investor_desc.strip()
                        else:
                            investor = ''
                    href = self.base_url + info.css('dt.view a::attr("href")').extract_first()

                    print(date, company, industry, acc_cate, acc_num, investor, href)

                    yield scrapy.Request(href, meta={'id_prefix': id_prefix,
                                                     'category': cate,
                                                     'company': company,
                                                     'industry': industry,
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
            item = PedailyMaScrapyItem()
            id_prefix = response.meta['id_prefix']
            item['id'] = id_prefix + "-" + md5.hexdigest()
            title_desc = response.css('div.info h1::text').extract_first()
            if title_desc:
                item['title'] = title_desc.strip()
            item['company'] = response.meta['company']
            item['financing_time'] = response.meta['date']
            item['industry'] = response.meta['industry']
            item['acc_cate'] = response.meta['acc_cate']
            item['acc_num'] = response.meta['acc_num']
            item['investor'] = response.meta['investor']
            item['url'] = response.url
            # 详情页解析
            infos = response.css('div.info ul> li')
            if infos:
                # 并购方
                acquirer_desc = infos[0].css('li::text').extract_first()
                if acquirer_desc:
                    item['acquirer'] = acquirer_desc.strip()
                else:
                    acquirer_desc = infos[0].css('li a::text').extract_first()
                    if acquirer_desc:
                        item['acquirer'] = acquirer_desc.strip()
                    else:
                        item['acquirer'] = ''
                # 被并购方
                acquired_party_desc = infos[1].css('li::text').extract_first()
                if acquired_party_desc:
                    item['acquired_party'] = acquired_party_desc.strip()
                else:
                    acquired_party_desc = infos[1].css('li a::text').extract_first()
                    if acquired_party_desc:
                        item['acquired_party'] = acquired_party_desc.strip()
                    else:
                        item['acquired_party'] = ''
                status_desc = infos[2].css('li::text').extract_first()
                if status_desc:
                    item['status'] = status_desc.strip()

                    # 所属行业
                    industry_desc = infos[3].css('li').extract_first()
                if industry_desc:
                    dr = re.compile(r'<[^>]+>', re.S)
                    dd = dr.sub('', industry_desc)
                    item['industry_desc'] = dd.replace(u'所属行业：', '')
                # 股权
                stock_rights_num_desc = infos[4].css('li::text').extract_first()
                if stock_rights_num_desc:
                    item['stock_rights_num'] = stock_rights_num_desc.strip()
                else:
                    item['stock_rights_num'] = ''

                # 开始时间
                start_time_desc = infos[5].css('li::text').extract_first()
                if start_time_desc:
                    item['start_time'] = start_time_desc.strip()
                else:
                    start_time_desc = infos[5].css('li a::text').extract_first()
                    if start_time_desc:
                        item['start_time'] = start_time_desc.strip()
                    else:
                        item['start_time'] = ''
                #  结束时间
                end_time_desc = infos[6].css('li::text').extract_first()
                if end_time_desc:
                    item['end_time'] = end_time_desc.strip()
                else:
                    end_time_desc = infos[6].css('li a::text').extract_first()
                    if end_time_desc:
                        item['end_time'] = end_time_desc.strip()
                    else:
                        item['end_time'] = ''
                # 是否支持 vc_pe
                vc_pe_support_desc = infos[7].css('li::text').extract_first()
                if vc_pe_support_desc:
                    item['vc_pe_support'] = vc_pe_support_desc.strip()
                else:
                    item['vc_pe_support'] = ''

                item['short_detail'] = response.css('div#desc > p::text').extract_first()
                # print(item)
                yield item
