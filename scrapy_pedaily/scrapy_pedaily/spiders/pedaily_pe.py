# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib
from scrapy_pedaily.items import PedailyPeScrapyItem
import math


# 募资事件
class PedailyPeSpider(scrapy.Spider):
    index = 8
    module_index = 4
    name = 'pedaily_pe'
    allowed_domains = ['pedaily.cn']
    start_urls = ['http://zdb.pedaily.cn/pe/']
    category_index = {'pe': '3'}
    category_desc = {'pe': '募资事件'}
    url_descs = ['募资事件']
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
                        print(url)
                        yield scrapy.Request(url, callback=self.parse)
                        time.sleep(random.randint(1, 6))
                else:
                    self.logger.warning("has no next page!!!")
            else:
                id_prefix = '8-4'
                cate = '募资事件'
                info_list = response.css('div.box-news-list ul#pe-list > li[class!="head"]')
                dr = re.compile(r'<[^>]+>', re.S)
                for info in info_list:
                    date = info.css('span.time::text').extract_first()
                    fund = info.css('dt.fund::text').extract_first()
                    if not fund:
                        fund = info.css('dt.fund > a::text').extract_first()

                    group = info.css('dt.group::text').extract_first()
                    if not group:
                        group = info.css('dt.group > a::text').extract_first()
                    acc_cate = info.css('span.d::text').extract_first()
                    acc_num = info.css('span.m::text').extract_first()

                    href = self.base_url + info.css('dt.view a::attr("href")').extract_first()

                    yield scrapy.Request(href, meta={'id_prefix': id_prefix,
                                                     'category': cate,
                                                     'fund': fund,
                                                     'group': group,
                                                     'acc_cate': acc_cate,
                                                     'acc_num': acc_num,
                                                     'date': date},
                                         callback=self.parse_content)
                    time.sleep(random.randint(1, 6))

    def parse_content(self, response):
        if response.status == 200:
            print("#########", response.url)
            md5 = hashlib.md5()
            md5.update(response.url.encode(encoding='utf-8'))
            item = PedailyPeScrapyItem()
            id_prefix = response.meta['id_prefix']
            item['id'] = id_prefix + "-" + md5.hexdigest()
            title_desc = response.css('div.info h1::text').extract_first()
            if title_desc:
                item['title'] = title_desc.strip()
            item['fund'] = response.meta['fund']
            item['group'] = response.meta['group']
            item['date'] = response.meta['date']
            item['acc_cate'] = response.meta['acc_cate']
            item['acc_num'] = response.meta['acc_num']
            item['url'] = response.url

            # 详情页解析
            infos = response.css('div.info ul> li')
            if infos:
                # 并购方
                fund_desc = infos[0].css('li::text').extract_first()
                if fund_desc:
                    item['fund_full_name'] = fund_desc.strip()
                else:
                    fund_desc = infos[0].css('li a::text').extract_first()
                    if fund_desc:
                        item['fund_full_name'] = fund_desc.strip()
                    else:
                        item['fund_full_name'] = ''
                # 币种
                currency_desc = infos[1].css('li::text').extract_first()
                if currency_desc:
                    item['currency'] = currency_desc.strip()
                # 创立时间
                setup_time_desc = infos[2].css('li::text').extract_first()
                if setup_time_desc:
                    item['setup_time'] = setup_time_desc.strip()
                # 募集状态
                status_desc = infos[3].css('li::text').extract_first()
                if status_desc:
                    item['status'] = status_desc.strip()
                # 管理机构
                man_org_desc = infos[3].css('li::text').extract_first()
                if man_org_desc:
                    item['man_org'] = man_org_desc.strip()
                else:
                    man_org_desc = infos[0].css('li a::text').extract_first()
                    if man_org_desc:
                        item['man_org'] = man_org_desc.strip()
                    else:
                        item['man_org'] = ''
                # 目标金额
                target_mount_desc = infos[4].css('li::text').extract_first()
                if target_mount_desc:
                    item['target_mount'] = target_mount_desc.strip()

                capital_type_desc = infos[4].css('li::text').extract_first()
                if capital_type_desc:
                    item['capital_type'] = capital_type_desc.strip()

            # print("****************", item)
            yield item
