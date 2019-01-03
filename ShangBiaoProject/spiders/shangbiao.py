# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import scrapy
import json
from ShangBiaoProject.items import ShangbiaoprojectItem

class ShangbiaoSpider(scrapy.Spider):
    name = 'shangbiao'
    #allowed_domains = ['http://sbgg.saic.gov.cn']
    start_urls = ['http://sbgg.saic.gov.cn:9080/']

    def start_requests(self):
        url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/getAnnType.html'
        #yield Request(url, callback=self.parse)
        yield scrapy.FormRequest(
            url = url,
            formdata = {"annNum": "1626"},
            callback = self.parse_typeCode
        )

    def parse_typeCode(self, response):
        url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html'
        data = json.loads(response.text)
        for item in data:
            item = dict(item)
            if item.get("ann_type") == "送达公告":
                code = item["ann_type_code"]
                print(code)
                yield scrapy.FormRequest(
                    url = url,
                    formdata = {"annNum": "1626", "annTypecode": str(code)},
                    callback = self.parse_id
                )

    def parse_id(self, response):

        #url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/imageView.html'
        print(response.text)
        #yield scrapy.FormRequest(
        #    url=url,
        #    formdata={"id": response.text, "pageNum": "1", "flag": "1"},
        #    callback=self.parse
        #)




    def parse(self, response):
        print("parse解析的值为%s" % response.text)
        item = ShangbiaoprojectItem()
        item['images'] = response.imaglist
        yield item
