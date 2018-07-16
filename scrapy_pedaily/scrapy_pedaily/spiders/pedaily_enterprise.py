# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib
from scrapy_pedaily.items import PedailyEnterScrapyItem
import math


class PedailyEnterpriseSpider(scrapy.Spider):
    index = 8
    module_index = 6
    name = 'pedaily_enterprise'
    allowed_domains = ['pedaily.cn']
    start_urls = ['http://zdb.pedaily.cn/enterprise/p1']
    category_index = {'enterprise': '6'}
    category_desc = {'enterprise': '企业库'}
    url_descs = ['企业库']
    base_url = 'http://zdb.pedaily.cn'
    comapys_base_url = 'http://zdb.pedaily.cn/enterprise/p{}/'

    def parse(self, response):
        print("**********", response.url)
        if response.status == 200:
            id_prefix = '8-6'
            cate = '企业库'
            if response.url in self.start_urls:
                total_page_desc = response.css('span.title > span.total::text').extract_first()
                if total_page_desc.isdigit():
                    total_page = math.floor(int(total_page_desc) / 20) + int(math.fmod(int(total_page_desc), 20))
                    for pageNum in range(1, total_page + 1):
                        url = self.comapys_base_url.format(str(pageNum))
                        # print(url)
                        yield scrapy.Request(url, callback=self.parse)
                        time.sleep(random.randint(1, 3))
                else:
                    self.logger.warning("has no next page!!!")
            print('scan page list')
            info_list = response.css('div.box-news-list ul#enterprise-list > li[class!="head"]')
            for info in info_list:
                name = info.css('h3 a::text').extract_first()
                page_url = self.base_url + info.css('div.img > a::attr("href")').extract_first()
                icon = info.css('div.img > a > img::attr("src")').extract_first()
                tag = info.css('div.img > a > img::attr("alt")').extract_first()
                location = info.css('h3 span.location::text').extract_first()
                cm_desc = info.css('div.desc::text').extract_first()
                print(page_url)

                yield scrapy.Request(page_url, meta={'id_prefix': id_prefix,
                                                     'category': cate,
                                                     'name': name,
                                                     'icon': icon,
                                                     'tag': tag,
                                                     'location': location,
                                                     'cm_desc': cm_desc},
                                     callback=self.parse_content)
                time.sleep(random.randint(1, 6))

    def parse_content(self, response):
        if response.status == 200:
            print("#########", response.url)
            md5 = hashlib.md5()
            md5.update(response.url.encode(encoding='utf-8'))
            item = PedailyEnterScrapyItem()
            id_prefix = response.meta['id_prefix']
            item['id'] = id_prefix + "-" + md5.hexdigest()
            item['name'] = response.meta['name']
            item['url'] = response.url
            item['icon'] = response.meta['icon']
            item['tag'] = response.meta['tag']
            item['location'] = response.meta['location']
            item['cm_desc'] = response.meta['cm_desc']
            # 详情页解析
            infos = response.css('div.info ul> li')
            if infos:
                # 机构总部
                item['headquarters'] = infos[0].css('li::text').extract_first()
                # 注册地址
                item['reg_place'] = infos[1].css('li::text').extract_first()
                # 成立时间
                item['setup_time'] = infos[2].css('li::text').extract_first()
                # 所属行业
                item['industry_cate'] = infos[3].css('li::text').extract_first()
                # 官方网站
                item['office_website'] = infos[4].css('li a::text').extract_first()

                # 简介
                short_detail_desc = response.css('div#desc').extract_first()
                if short_detail_desc:
                    dr = re.compile(r'<[^>]+>', re.S)
                    dd = dr.sub('', short_detail_desc)
                    # short_detail = dd
                    item['short_detail'] = dd
                # print(item)

                yield item
