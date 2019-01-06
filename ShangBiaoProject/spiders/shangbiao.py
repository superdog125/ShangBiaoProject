# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import scrapy
import json
from ShangBiaoProject.items import ShangbiaoprojectItem

class ShangbiaoSpider(scrapy.Spider):
    name = 'shangbiao'
    #allowed_domains = ['http://sbgg.saic.gov.cn']
    start_urls = ['http://sbgg.saic.gov.cn:9080/']

    annNum_url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/getAnnType.html?annNum={num}'
    maxnum = '1628'
    num = '900'

    typeCode_url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html?annNum={num}&annTypecode={code}'
    code = ''

    image_url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/imageView.html?id={id}&pageNum={pageNum}&flag={flag}'
    id = ''
    pageNum = ''   # 当前第几页
    flag = '1'

    imaglist = []
    pageSize = ''      # 每页的条数
    totalPage = ''        # 总页数
    def start_requests(self):
        yield Request(self.annNum_url.format(num=self.num), self.parse_typeCode)


    def parse_typeCode(self, response):
        data = json.loads(response.text)
        for item in data:
            item = dict(item)
            if item.get("ann_type") == "送达公告":
                self.code = item["ann_type_code"]
                yield Request(self.typeCode_url.format(num=self.num, code=self.code), self.parse_id)


    def parse_id(self, response):
        url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/imageView.html'
        self.id = response.text
        self.pageNum = "1"
        yield Request(self.image_url.format(id=self.id, pageNum=self.pageNum, flag=self.flag), self.parse_images)


    # 每一页的图片解析保存
    def parse_images(self, response):
        result = json.loads(response.text)
        self.imaglist = result.get('imaglist')
        self.pageSize = result.get('pageSize')
        self.totalPage = result.get('totalPage')
        # print("imaglist解析的值为%s" % self.imaglist)
        item = ShangbiaoprojectItem()
        # 每一页的图片解析保存
        for imag in self.imaglist:
            item['image'] = imag
            yield item
        # 下一页解析
        if int(self.pageNum) < self.totalPage:
            try:
                self.pageNum = str(int(self.pageNum)+1)
                yield Request(self.image_url.format(id=self.id, pageNum=self.pageNum, flag=self.flag), self.parse_images)
                print('next page.....')
            except Exception as e:
                print(e)
                pass
        else:
            print('%sall the pic has been saved, trying to next issue...' % self.num)
            if int(self.num) < int(self.maxnum):
                self.num = str(int(self.num) + 1)
                print('% pic have been scrawling...' % self.num)
                try:
                    self.start_requests(self)
                except Exception as e:
                    print(e)
                    pass
            else:
                print('all issue pic has been scrawl...')
