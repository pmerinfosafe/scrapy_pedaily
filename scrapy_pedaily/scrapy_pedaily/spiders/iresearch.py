# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib
import requests
from bs4 import BeautifulSoup
from scrapy_pedaily.items import IresearchNewsScrapyItem

from .module_config import (
    NEWS,
    COLUMN,
    START
)


class IresearchSpider(scrapy.Spider):
    index = 8
    name = 'iresearch'
    allowed_domains = ['iresearch.cn']
    start_urls = ['http://news.iresearch.cn/',
                  'http://column.iresearch.cn/',
                  'http://start.iresearch.cn/'
                  ]
    modules_index_map = {
        1: "互联网+",
        2: "专栏",
        3: "创投",
    }

    category_num_array = ['5', '5', '1']
    category_map = {
        1: ['移动互联网', '电子商务', '互联网', '网络营销', '网络游戏'],
        2: ['移动互联网', '电子商务', '互联网', '网络营销', '网络游戏'],
        3: ['创业']
    }

    modules_page_num = [NEWS,
                        COLUMN,
                        START]
    base_urls = ['http://news.iresearch.cn', 'http://column.iresearch.cn', 'http://start.iresearch.cn']
    requests_url = ['/include/pages/redis.aspx', '/include/pages/blogRedis.aspx', '/include/pages/redis.aspx']

    def parse(self, response):
        if response.url in self.start_urls:
            index = self.start_urls.index(response.url)
            if index != 0:
                return
            total_page = self.modules_page_num[index]
            id_prefix = '36-' + str(int(index) + 1)
            moudle_name = self.modules_index_map.get(int(index) + 1)
            print(total_page, id_prefix, moudle_name)
            category_num = self.category_num_array[index]
            cate_name_array = self.category_map.get(int(index) + 1)
            cate_page_infos = response.css('div#tab-list > div')
            print('category_num:', category_num)
            for cate_num in range(0, int(category_num)):
                cate_name = cate_name_array[cate_num]
                page_infos = cate_page_infos[cate_num].css('li')
                print('######page_infos:', len(page_infos))
                for page_info in page_infos:
                    info_id = page_info.css('::attr("id")').extract_first()
                    page_url = page_info.css('div.txt h3 a::attr("href")').extract_first()
                    page_sort = page_info.css('div.u-img>a >span::text').extract_first()
                    title = page_info.css('div.txt h3 a::text').extract_first()
                    subject = page_info.css('div.txt p::text').extract_first()
                    tag_arra = page_info.css('div.link a::text').extract_first()
                    if tag_arra:
                        tag = ','.join(tag_arra)
                    publish_date = page_info.css('div.time span::text').extract_first()
                    # print('+++++++++++++++', publish_date)
                    if publish_date and publish_date.find('/') != -1:
                        publish_date = publish_date.replace('/', '-')
                    print('+++++++++++++++', page_url)
                    if page_url is not None:
                        yield scrapy.Request(page_url, meta={'id_prefix': id_prefix + '-' + str(cate_num + 1),
                                                             'category': cate_name,
                                                             'info_id': info_id,
                                                             'title': title,
                                                             'tag': tag,
                                                             'publish_date': publish_date,
                                                             'subject': subject,
                                                             'page_sort': page_sort,
                                                             'moudle_name': moudle_name
                                                             },
                                             callback=self.parse_content)
                        time.sleep(random.randint(1, 3))
                lastId = page_infos[-1].css('::attr("id")').extract_first()
                data_part = cate_page_infos[cate_num].css('::attr("data")').extract_first()
                for page_num in range(1, int(total_page) + 1):
                    data = data_part + '&lastId=' + lastId
                    url = self.base_urls[index] + self.requests_url[index] + '?' + data
                    try:
                        response = requests.get(url)
                    except Exception as e:
                        print(e)
                        break
                    soup = BeautifulSoup(response.text, 'html.parser')
                    page_infos = soup.select('li')
                    # 重设lastIc
                    lastId = page_infos[-1].attrs['id']
                    for page_info in page_infos:
                        info_id = page_info.attrs['id']
                        page_url = page_info.find('h3').find('a').attrs['href']
                        if page_info.find('span', {'class': 'sort'}) is not None:
                            page_sort = page_info.find('span', {'class': 'sort'}).get_text()
                        else:
                            page_sort = ''
                        title = page_info.find('h3').find('a').get_text()
                        subject = page_info.find('div', class_='txt').find('p').get_text()
                        tag_arra = page_info.find('div', {'class': 'link', 'class': 'f-fl'}).findAll('a')
                        tag_str_arra = []
                        for tag_ele in tag_arra:
                            tag_str_arra.append(tag_ele.get_text())
                        if tag_str_arra:
                            tag = ','.join(tag_str_arra)
                        else:
                            tag = ''
                        publish_date = page_info.find('div', class_='txt').find('span').get_text()
                        if publish_date and publish_date.find('/') != -1:
                            publish_date = publish_date.replace('/', '-')
                        print('*******', page_url)
                        yield scrapy.Request(page_url, meta={'id_prefix': id_prefix + '-' + str(cate_num + 1),
                                                             'category': cate_name,
                                                             'info_id': info_id,
                                                             'title': title,
                                                             'tag': tag,
                                                             'publish_date': publish_date,
                                                             'subject': subject,
                                                             'page_sort': page_sort,
                                                             'moudle_name': moudle_name
                                                             },
                                             callback=self.parse_content)
                        time.sleep(random.randint(1, 3))

    def parse_content(self, response):
        if response.status == 200:
            print("#########", response.url)
            md5 = hashlib.md5()
            md5.update(response.url.encode(encoding='utf-8'))
            item = IresearchNewsScrapyItem()
            id_prefix = response.meta['id_prefix']
            # id
            item['id'] = id_prefix + "-" + md5.hexdigest()
            # url
            item['url'] = response.url
            # 信息ID
            item['info_id'] = response.meta['info_id']
            # 标签
            item['tag'] = response.meta['tag']
            # 标题
            item['title'] = response.meta['title']
            # 分类：'移动互联网', '电子商务', '互联网', '网络营销', '网络游戏'
            item['category'] = response.meta['category']
            item['publish_date'] = response.meta['publish_date']
            # 主题
            item['subject'] = response.meta['subject']
            # 页面分类
            item['page_sort'] = response.meta['page_sort']
            # 模块名称 互联网+  专栏 创投
            item['moudle_name'] = response.meta['moudle_name']

            origin = response.css('div.origin span::text').extract_first()
            item['source'] = ''
            item['author'] = ''
            if origin:
                origin_re = re.search('来源：(.*?)作者：(.*?)$', origin)
                if origin_re is not None:
                    # 来源
                    if origin_re.group(1):
                        item['source'] = origin_re.group(1).strip()
                    else:
                        item['source'] = ''
                    # 作者
                    if origin_re.group(2):
                        item['author'] = origin_re.group(1).strip()
                    else:
                        item['author'] = ''
            # 主要内容
            details = response.css('div.m-article').extract_first()
            if details:
                dr = re.compile(r'<[^>]+>', re.S)
                dd = dr.sub('', details)
                item['content'] = dd.replace(u'\u3000', '').replace(u'\t', '').replace(u'\r', '').replace(u'\n',
                                                                                                          '').strip()
            else:
                item['content'] = ''

            yield item
