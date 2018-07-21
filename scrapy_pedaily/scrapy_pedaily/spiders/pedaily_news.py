# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib
from scrapy_pedaily.items import PedailyNewsScrapyItem
import math

from .module_config import (
    INTERNET,
    IT,
    MOBILENTERNET,
    HEALTH_SERVICE,
    MEDICINE,
    HEALTHNDUSTRY,
    TRADUTIONAL_CONSUMPTION,
    TOURISM,
    EDUCATION,
    GAME,
    CULTURALNDUSTRY,
    MOVIES,
    US_STOCKS, A_STOCKS, ASSET_MANAGEMENT, AGRICULTURE, GREEN_ENERGY, MANUFACTURING

)

class PedailyNewSpider(scrapy.Spider):
    index = 8
    module_index = 7
    name = 'pedaily_new'
    allowed_domains = ['pedaily.cn']
    start_urls = ['http://news.pedaily.cn/i-internet/',
                  'http://news.pedaily.cn/i-it/',
                  'http://news.pedaily.cn/i-mobilenternet/',
                  'http://news.pedaily.cn/i-health-service/',
                  'http://news.pedaily.cn/i-medicine/',
                  'http://news.pedaily.cn/i-healthndustry/',
                  'http://news.pedaily.cn/i-traditional-consumption/',
                  'http://news.pedaily.cn/i-tourism/',
                  'http://news.pedaily.cn/i-education/',
                  'http://news.pedaily.cn/i-game/',
                  'http://news.pedaily.cn/i-culturalndustry/',
                  'http://news.pedaily.cn/i-movies/',
                  'http://news.pedaily.cn/i-us-stocks/',
                  'http://news.pedaily.cn/i-a-stocks/',
                  'http://news.pedaily.cn/i-asset-management/',
                  'http://news.pedaily.cn/i-agriculture/',
                  'http://news.pedaily.cn/i-green-energy/',
                  'http://news.pedaily.cn/i-manufacturing/']
    modules_index = {
        1: "互联网",
        2: "it",
        3: "移动互联网",
        4: "医疗服务",
        5: "医药",
        6: "健康",
        7: "传统消费",
        8: "旅游",
        9: "教育培训",
        10: "游戏",
        11: "文化产业",
        12: "影视",
        13: "美股",
        14: "A股",
        15: "资产管理",
        16: "农业",
        17: "环保能源",
        18: "制造业"

    }
    modules_page_num = [INTERNET, IT, MOBILENTERNET,
                        HEALTH_SERVICE,
                        MEDICINE,
                        HEALTHNDUSTRY,
                        TRADUTIONAL_CONSUMPTION,
                        TOURISM,
                        EDUCATION,
                        GAME,
                        CULTURALNDUSTRY,
                        MOVIES,
                        US_STOCKS, A_STOCKS, ASSET_MANAGEMENT, AGRICULTURE, GREEN_ENERGY, MANUFACTURING]
    base_url = 'http://news.pedaily.cn'

    def parse(self, response):
        print("**********", response.url)
        if response.status == 200:
            if response.url in self.start_urls:
                index = self.start_urls.index(response.url)
                # index = 1
                # if response.url != self.start_urls[index]:
                #     return
                total_page = self.modules_page_num[index]
                id_prefix = '8-7-' + str(int(index) + 1)
                cate = self.modules_index.get(int(index) + 1)
                print(total_page, id_prefix, cate)
                # for page_num in range(1, 2):
                for page_num in range(1, int(total_page) + 1):
                    url = response.url + str(page_num) + '/'
                    yield scrapy.Request(url, meta={'id_prefix': id_prefix, 'category': cate}, callback=self.parse)
                    # time.sleep(random.randint(1, 3))
            else:
                id_prefix = response.meta['id_prefix']
                cate = response.meta['category']
                info_list = response.css('div.news-list > ul#newslist-all li')
                for info in info_list:
                    industryid = info.css('li::attr("data-industryid")').extract_first()
                    page_url = info.css('div.img a::attr("href")').extract_first()
                    title = info.css('h3 a::text').extract_first()
                    tag_desc = info.css('div.tag a::text').extract()
                    if tag_desc:
                        tag = ','.join(tag_desc)
                    else:
                        tag = ''
                    print(page_url, industryid, title, tag)
                    yield scrapy.Request(page_url, meta={'id_prefix': id_prefix,
                                                         'category': cate,
                                                         'industryid': industryid,
                                                         'title': title,
                                                         'tag': tag,
                                                         },
                                         callback=self.parse_content)
                    time.sleep(random.randint(1, 3))

    def parse_content(self, response):
        if response.status == 200:
            print("#########", response.url)
            md5 = hashlib.md5()
            md5.update(response.url.encode(encoding='utf-8'))
            item = PedailyNewsScrapyItem()
            id_prefix = response.meta['id_prefix']
            item['id'] = id_prefix + "-" + md5.hexdigest()
            item['url'] = response.url
            item['industryid'] = response.meta['industryid']
            item['tag'] = response.meta['tag']
            item['title'] = response.meta['title']
            item['category'] = response.meta['category']
            # 详情页解析
            item['date'] = response.css('div.info div.box-l span.date::text').extract_first()
            # 来源
            source_desc = response.css('div.info div.box-l::text').extract_first()
            if source_desc:
                item['source'] = source_desc.replace(u'\u3000', '').replace(u'\t', '').strip()
            else:
                item['source'] = ''
            # 主题
            item['subject'] = response.css('div.subject ::text').extract_first()
            # 内容
            details = response.css('div#news-content').extract_first()
            if details:
                dr = re.compile(r'<[^>]+>', re.S)
                dd = dr.sub('', details)
                item['content'] = dd.replace(u'\u3000', '').replace(u'\t', '').replace(u'\xa0', '').replace(u'\u2003',
                                                                                                            '').strip()
            else:
                item['content'] = ''

            # print(item)

            yield item
