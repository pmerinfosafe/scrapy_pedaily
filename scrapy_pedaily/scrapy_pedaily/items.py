# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PedailyInvScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 编号
    id = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 公司
    company = scrapy.Field()
    # 融资时间
    financing_time = scrapy.Field()
    # 简介
    short_detail = scrapy.Field()
    # 所属行业
    industry = scrapy.Field()
    # 所属行业描述
    industry_desc = scrapy.Field()
    # # 分类
    # category = scrapy.Field()
    # 投资类型
    inv_cate = scrapy.Field()
    # 投资货币类型
    acc_cate = scrapy.Field()
    # 投资货币数量
    acc_num = scrapy.Field()
    # 投资方
    investor = scrapy.Field()
    # 融资方
    financing_party = scrapy.Field()
    # 行业分类
    industry_cate = scrapy.Field()
    # 详情路径
    url = scrapy.Field()


class PedailyIpoScrapyItem(scrapy.Item):
    # 编号
    id = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 公司
    company = scrapy.Field()
    # 上市时间
    financing_time = scrapy.Field()
    # 募资金额
    money = scrapy.Field()
    # 募资单位
    unit = scrapy.Field()
    # 交易所
    place = scrapy.Field()
    # 所属行业
    industry = scrapy.Field()
    # 所属行业描述
    industry_desc = scrapy.Field()
    # 企业名称详情
    company_detail = scrapy.Field()
    # 投资方
    investor = scrapy.Field()
    # 发行价
    offering_price = scrapy.Field()
    # 上市地点
    stock_exchange_place = scrapy.Field()
    # 发行量
    circulation = scrapy.Field()
    # 股票代码
    stock_code = scrapy.Field()
    # 行业分类
    industry_cate = scrapy.Field()

    vc_pe_support = scrapy.Field()
    # 详情路径
    url = scrapy.Field()


class PedailyMaScrapyItem(scrapy.Item):
    # 编号
    id = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 公司
    company = scrapy.Field()
    # 融资时间
    financing_time = scrapy.Field()
    # 简介
    short_detail = scrapy.Field()
    # 所属行业
    industry = scrapy.Field()
    # 所属行业描述
    industry_desc = scrapy.Field()
    # 投资货币类型
    acc_cate = scrapy.Field()
    # 投资货币数量
    acc_num = scrapy.Field()
    # 行业分类
    industry_cate = scrapy.Field()
    # 并购方
    acquirer = scrapy.Field()
    # 被并购方
    acquired_party = scrapy.Field()
    # 并购状态
    status = scrapy.Field()
    # 股权
    stock_rights_num = scrapy.Field()
    # 开始时间
    start_time = scrapy.Field()
    # 结束时间
    end_time = scrapy.Field()

    investor = scrapy.Field()

    vc_pe_support = scrapy.Field()
    # 详情路径
    url = scrapy.Field()

class PedailyPeScrapyItem(scrapy.Item):
    # 编号
    id = scrapy.Field()
    # 标题
    title = scrapy.Field()

    date = scrapy.Field()

    # 基金组织
    fund = scrapy.Field()
    # 管理机构
    group = scrapy.Field()
    # 募集资金货币类型
    acc_cate = scrapy.Field()
    # 募集资金货币数量
    acc_num = scrapy.Field()
    # 详情路径
    url = scrapy.Field()
    # 基金全称
    fund_full_name = scrapy.Field()
    # 币种
    currency = scrapy.Field()
    # 成立时间
    setup_time = scrapy.Field()
    # 募集状态
    status = scrapy.Field()
    # 管理机构
    man_org = scrapy.Field()
    # 目标货币金额
    target_mount = scrapy.Field()
    # 资本类型
    capital_type = scrapy.Field()

    collection_amount = scrapy.Field()

# class PedailyPeScrapyItem(scrapy.Item):
#     # 编号
#     id = scrapy.Field()
#     # 标题
#     title = scrapy.Field()
#
#     date = scrapy.Field()
#
#     # 基金组织
#     fund = scrapy.Field()
#     # 管理机构
#     group = scrapy.Field()
#     # 募集资金货币类型
#     acc_cate = scrapy.Field()
#     # 募集资金货币数量
#     acc_num = scrapy.Field()
#     # 详情路径
#     url = scrapy.Field()
#     # 基金全称
#     fund_full_name = scrapy.Field()
#     # 币种
#     currency = scrapy.Field()
#     # 成立时间
#     setup_time = scrapy.Field()
#     # 募集状态
#     status = scrapy.Field()
#     # 管理机构
#     man_org = scrapy.Field()
#     # 目标货币金额
#     target_mount = scrapy.Field()
#     # 资本类型
#     capital_type = scrapy.Field()
#
#     collection_amount = scrapy.Field()

class PedailyCmScrapyItem(scrapy.Item):
    # 编号
    id = scrapy.Field()
    # 名称
    name = scrapy.Field()
    # 图标
    icon = scrapy.Field()
    # 英文名
    english_name = scrapy.Field()
    # 标签
    tag = scrapy.Field()
    # 位置
    location = scrapy.Field()
    # 公司简述
    cm_desc = scrapy.Field()
    # 详情路径
    url = scrapy.Field()
    # 资本类型
    capital_type = scrapy.Field()
    # 机构性质
    org_nature = scrapy.Field()
    # 注册地址
    reg_place = scrapy.Field()
    # 成立时间
    setup_time = scrapy.Field()
    # 机构总部
    headquarters = scrapy.Field()
    #官方网站
    office_website = scrapy.Field()
    # 投资阶段
    investment_stage = scrapy.Field()
    # 简介
    short_detail = scrapy.Field()
    # 联系方式
    contact_info = scrapy.Field()
    # 募集事件
    ma_info = scrapy.Field()
    # 投资事件
    inv_info = scrapy.Field()
    # 相关新闻
    related_news = scrapy.Field()

class PedailyEnterScrapyItem(scrapy.Item):
    # 编号
    id = scrapy.Field()
    # 名称
    name = scrapy.Field()
    # 图标
    icon = scrapy.Field()
    # 英文名
    english_name = scrapy.Field()
    # 标签
    tag = scrapy.Field()
    # 位置
    location = scrapy.Field()
    # 公司简述
    cm_desc = scrapy.Field()
    # 详情路径
    url = scrapy.Field()

    # 注册地址
    reg_place = scrapy.Field()
    # 成立时间
    setup_time = scrapy.Field()
    # 机构总部
    headquarters = scrapy.Field()
    #官方网站
    office_website = scrapy.Field()
    # 所属行业
    industry_cate = scrapy.Field()
    # 简介
    short_detail = scrapy.Field()
    # 联系方式
    contact_info = scrapy.Field()
    # 募集事件
    ma_info = scrapy.Field()
    # 投资事件
    inv_info = scrapy.Field()
    # 相关新闻
    related_news = scrapy.Field()

class PedailyNewsScrapyItem(scrapy.Item):
    # 编号
    id = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 工业ID
    industryid = scrapy.Field()
    # 标签
    tag = scrapy.Field()
    # 分类
    category = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 详情路径
    url = scrapy.Field()
    # 来源
    source = scrapy.Field()
    # 主题
    subject = scrapy.Field()
    # 机构总部
    content = scrapy.Field()






