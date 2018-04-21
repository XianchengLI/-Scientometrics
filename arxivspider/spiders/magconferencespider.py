# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy import signals
from scrapy import Request
from arxivspider.items import *
from arxivspider.pipelines import GetTitle
import urllib2
import urllib
import json
import socket


class MAGConferenceSpider(Spider):
    name = 'magconferencespider'
    handle_httpstatus_list = [404]
    spider_id = socket.getfqdn(socket.gethostname())
    url_limit = 200
    undo_url = 200
    get_cnt = 0
    countries = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MAGConferenceSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        self.start_requests()

    def start_requests(self):
        response = GetTitle.get_conference(self.url_limit, self.spider_id, self.get_cnt)
        self.get_cnt += 1
        for item in response:
            url = 'https://academic.microsoft.com/api/browse/GetEntityDetails?'
            body = {'entityId' : item}
            try:
                yield Request(url=url + urllib.urlencode(body), meta={'id': item}, headers=HEADER)
            except:
                self.undo_url -= 1



    def parse(self, response):
        result = json.loads(response.body_as_unicode())

        #print result['entity']

        try:
            item = MAGConferenceItem()

            item['conference_id'] = response.meta['id']

            if 'cc' in result['entity']:
                item['cite_count'] = result['entity']['cc']
            else:
                item['cite_count'] = 0

            if 'ecc' in result['entity']:
                item['e_cite_count'] = result['entity']['ecc']
            else:
                item['e_cite_count'] = 0

            if 'pc' in result['entity']['extended']:
                item['paper_count'] = result['entity']['extended']['pc']
            else:
                item['paper_count'] = 0

            if 'fieldsOfStudy' in result:
                item['fields'] = result['fieldsOfStudy']
            else:
                item['fields'] = ''

            if 'dn' in result['entity']['extended']:
                item['whole'] = result['entity']['extended']['dn']
            else:
                item['whole'] = ''

            if 'sn' in result['entity']['extended']:
                item['short'] = result['entity']['extended']['sn']
            else:
                item['short'] = ''

            yield item

            self.undo_url -= 1
        except:
            self.undo_url -= 1

        print '------UNDO:%d-----' %(self.undo_url)

        if self.undo_url <= self.url_limit * 0.4 :
            self.undo_url += self.url_limit
            response = GetTitle.get_conference(self.url_limit, self.spider_id, self.get_cnt)
            self.get_cnt += 1
            for item in response:
                url = 'https://academic.microsoft.com/api/browse/GetEntityDetails?'
                body = {'entityId': item}
                try:
                    yield Request(url=url + urllib.urlencode(body), meta={'id': item}, headers=HEADER)
                except:
                    self.undo_url -= 1
        

HEADER={
    "Host": "academic.microsoft.com",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Referer": "https://academic.microsoft.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cookie": "msacademic=3c0d0eab-29ac-4905-b1ca-1630498d553c; ARRAffinity=796e069c102ca480e86bc9b2032525de5577107eddaa871904dc146f45adc854; ai_user=/t9iZ|2017-10-01T10:10:10.850Z; ai_session=xg7kr|1506852598778|1506852610856.78",
    }

            

