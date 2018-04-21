# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy import signals
from scrapy import Request
from arxivspider.items import *


class CCFSpider(Spider):
    name = 'ccfspider'

    def start_requests(self):
        list = [
            'http://www.ccf.org.cn/jsjtxjgbxyfbjsccxt/',
            'http://www.ccf.org.cn/xspj/jsjwl/',
            'http://www.ccf.org.cn/xspj/wlyxxaq/',
            'http://www.ccf.org.cn/xspj/rjgc/xtrj/cxsjyy/',
            'http://www.ccf.org.cn/xspj/sjk/sjwj/nrjs/',
            'http://www.ccf.org.cn/xspj/jsjkxll/',
            'http://www.ccf.org.cn/xspj/jsjtxxydmt/',
            'http://www.ccf.org.cn/xspj/rgzn/',
            'http://www.ccf.org.cn/xspj/rjjhypsjs/',
            'http://www.ccf.org.cn/xspj/jc/zh/xx/',
        ]
        index = 1
        for url in list:
            yield Request(url=url, meta={'id': index})
            index += 1



    def parse(self, response):
        lists = response.xpath('//div[@class="col-md-10"]/div[@class="g-box1"]/ul')

        items = lists[0].xpath('.//li')
        index = 0
        for item in items:
            if index > 0:
                ccf_item = CCFItem()
                texts = item.xpath('.//div/text()').extract()

                ccf_item['abbr'] = texts[1]
                ccf_item['name'] = texts[2]
                ccf_item['pub'] = texts[3]
                ccf_item['dblplink'] = item.xpath('.//div/a/text()').extract_first()
                ccf_item['type'] = 'journal'
                ccf_item['classification'] = 'A'
                ccf_item['category'] = response.meta['id']

                yield ccf_item
            else:
                index += 1

        items = lists[1].xpath('.//li')
        index = 0
        for item in items:
            if index > 0:
                ccf_item = CCFItem()
                texts = item.xpath('.//div/text()').extract()

                ccf_item['abbr'] = texts[1]
                ccf_item['name'] = texts[2]
                ccf_item['pub'] = texts[3]
                ccf_item['dblplink'] = item.xpath('.//div/a/text()').extract_first()
                ccf_item['type'] = 'journal'
                ccf_item['classification'] = 'B'
                ccf_item['category'] = response.meta['id']

                yield ccf_item
            else:
                index += 1

        items = lists[2].xpath('.//li')
        index = 0
        for item in items:
            if index > 0:
                ccf_item = CCFItem()
                texts = item.xpath('.//div/text()').extract()

                ccf_item['abbr'] = texts[1]
                ccf_item['name'] = texts[2]
                ccf_item['pub'] = texts[3]
                ccf_item['dblplink'] = item.xpath('.//div/a/text()').extract_first()
                ccf_item['type'] = 'journal'
                ccf_item['classification'] = 'C'
                ccf_item['category'] = response.meta['id']

                yield ccf_item
            else:
                index += 1

        items = lists[3].xpath('.//li')
        index = 0
        for item in items:
            if index > 0:
                ccf_item = CCFItem()
                texts = item.xpath('.//div/text()').extract()

                ccf_item['abbr'] = texts[1]
                ccf_item['name'] = texts[2]
                ccf_item['pub'] = texts[3]
                ccf_item['dblplink'] = item.xpath('.//div/a/text()').extract_first()
                ccf_item['type'] = 'conference'
                ccf_item['classification'] = 'A'
                ccf_item['category'] = response.meta['id']

                yield ccf_item
            else:
                index += 1

        items = lists[4].xpath('.//li')
        index = 0
        for item in items:
            if index > 0:
                ccf_item = CCFItem()
                texts = item.xpath('.//div/text()').extract()

                ccf_item['abbr'] = texts[1]
                ccf_item['name'] = texts[2]
                ccf_item['pub'] = texts[3]
                ccf_item['dblplink'] = item.xpath('.//div/a/text()').extract_first()
                ccf_item['type'] = 'conference'
                ccf_item['classification'] = 'B'
                ccf_item['category'] = response.meta['id']

                yield ccf_item
            else:
                index += 1

        items = lists[5].xpath('.//li')
        index = 0
        for item in items:
            if index > 0:
                ccf_item = CCFItem()
                texts = item.xpath('.//div/text()').extract()

                ccf_item['abbr'] = texts[1]
                ccf_item['name'] = texts[2]
                ccf_item['pub'] = texts[3]
                ccf_item['dblplink'] = item.xpath('.//div/a/text()').extract_first()
                ccf_item['type'] = 'conference'
                ccf_item['classification'] = 'C'
                ccf_item['category'] = response.meta['id']

                yield ccf_item
            else:
                index += 1



        

HEADER={
    "Host": "academic.microsoft.com",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Referer": "https://academic.microsoft.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cookie": "ARRAffinity=51c0c17ddb58e50423a9be9a5d8f9d40458825e30631dc7968bea62735523936; msacademic=6cdb2e53-7ccb-4fba-b5b2-a6e528741415; ai_user=tMZqE|2017-09-29T12:38:05.778Z; ai_session=Vh572|1506688686606.805|1506688686606.805",
    }

            

