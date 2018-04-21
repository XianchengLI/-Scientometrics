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


class MAGAuthorSpider(Spider):
    name = 'magauthorspider'
    handle_httpstatus_list = [404]
    spider_id = socket.getfqdn(socket.gethostname())
    url_limit = 200
    undo_url = 200
    get_cnt = 0
    countries = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MAGAuthorSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        self.start_requests()

    def start_requests(self):
        response = GetTitle.get_authors_mag(self.url_limit, self.spider_id, self.get_cnt)
        self.get_cnt += 1
        for item in response:
            url = 'https://academic.microsoft.com/api/browse/GetEntityDetails?'
            body = {'entityId' : item}
            try:
                yield Request(url=url + urllib.urlencode(body), meta={'id': item, 'type': False}, headers=HEADER)
            except:
                self.undo_url -= 1



    def parse(self, response):
        result = json.loads(response.body_as_unicode())

        if response.meta['type']:
            item = MAGAuthorItem()

            item['author_id'] = response.meta['id']
            item['cite_count'] = result['citationCount']
            if 'estimatedCitationCount' in result:
                item['e_cite_count'] = result['estimatedCitationCount']
            else:
                item['e_cite_count'] = result['citationCount']
            item['paper_count'] = result['publicationCount']

            item['fields'] = result['fieldsOfStudy']
            if 'coAuthors' in result:
                item['co_authors'] = result['coAuthors']
            else:
                item['co_authors'] = []

            if 'conferences' in result:
                item['conferences'] = result['conferences']
            else:
                item['conferences'] = []

            if 'journals' in result:
                item['journals'] = result['journals']
            else:
                item['journals'] = []

            yield item

            self.undo_url -= 1

        else:
            if 'userName' in result:
                url = 'https://academic.microsoft.com/api/user/'
                yield Request(url=url + result['userName'], meta={'id': response.meta['id'], 'type': True},
                              headers=HEADER)

            else:
                item = MAGAuthorItem()

                item['author_id'] = response.meta['id']
                item['cite_count'] = result['entity']['cc']
                item['e_cite_count'] = result['estimatedCitationCount']
                item['paper_count'] = result['entity']['extended']['pc']

                if 'fieldsOfStudy' in result:
                    item['fields'] = result['fieldsOfStudy']
                else:
                    item['fields'] = []

                if 'coAuthors' in result:
                    item['co_authors'] = result['coAuthors']
                else:
                    item['co_authors'] = []

                if 'conferences' in result:
                    item['conferences'] = result['conferences']
                else:
                    item['conferences'] = []

                if 'journals' in result:
                    item['journals'] = result['journals']
                else:
                    item['journals'] = []

                yield item

                self.undo_url -= 1

        print '------UNDO:%d-----' %(self.undo_url)

        if self.undo_url <= self.url_limit * 0.4 :
            self.undo_url += self.url_limit
            response = GetTitle.get_authors_mag(self.url_limit, self.spider_id, self.get_cnt)
            self.get_cnt += 1
            for item in response:
                url = 'https://academic.microsoft.com/api/browse/GetEntityDetails?'
                body = {'entityId' : item}
                try:
                    yield Request(url=url + urllib.urlencode(body), meta={'id': item, 'type': False}, headers=HEADER)
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
    "Cookie": "ARRAffinity=51c0c17ddb58e50423a9be9a5d8f9d40458825e30631dc7968bea62735523936; msacademic=6cdb2e53-7ccb-4fba-b5b2-a6e528741415; ai_user=tMZqE|2017-09-29T12:38:05.778Z; ai_session=Vh572|1506688686606.805|1506688686606.805",
    }

            

