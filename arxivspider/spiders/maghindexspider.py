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
import random


class MAGHindexSpider(Spider):
    name = 'maghindexspider'
    handle_httpstatus_list = [404]
    spider_id = socket.getfqdn(socket.gethostname()) + '_' + str(random.randint(0, 100))
    url_limit = 200
    undo_url = 200
    get_cnt = 0
    ccf_list = {}
    lock = False

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MAGHindexSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        self.start_requests()

    def start_requests(self):
        self.ccf_list = GetTitle.get_CCF_list()

        response = GetTitle.get_authors_mag2(self.url_limit, self.spider_id, self.get_cnt)
        self.get_cnt += 1

        for item in response:

            url = 'https://academic.microsoft.com/api/search/GetEntityResults'
            body = {
                'Query': 'And(Ty=\'0\',Composite(AA.AuId=' + str(item[0]) + '))',
                'Limit': 8,
                'OrderBy': 'ECC',
                'SortAscending': 'false',
                'Offset': 0,
            }
            try:
                yield Request(
                    url=url,
                    body=urllib.urlencode(body),
                    method="POST", meta={'id': item[0], 'offset': 0, 'hindex': 0, 'i10index': 0, 'total': item[1],
                                         'find_h': False, 'find_i': False,
                                         'ccf_a_count': 0, 'ccf_b_count': 0, 'ccf_c_count': 0},
                    headers=HEADER,
                    dont_filter=True)
            except:
                self.undo_url -= 1




    def parse(self, response):
        res = json.loads(response.body_as_unicode())
        print '--------requst id:' + str(response.meta['id'])
        print '--------requst index:' + str(response.meta['offset'])
        print '--------requst total:' + str(response.meta['total'])

        author = {}
        author['author_id'] = response.meta['id']
        author['hindex'] = response.meta['hindex']
        author['i10index'] = response.meta['i10index']
        author['find_h'] = response.meta['find_h']
        author['find_i'] = response.meta['find_i']
        author['ccf_a_count'] = response.meta['ccf_a_count']
        author['ccf_b_count'] = response.meta['ccf_b_count']
        author['ccf_c_count'] = response.meta['ccf_c_count']
        index = response.meta['offset']

        author['total'] = res['entitiesInQuery'][0]['entity']['extended']['pc']

        for result in res['results']:
            item = MAGArticleItem()

            index += 1
            if result['ecc'] < index and not author['find_h']:
                author['hindex'] = index - 1
                author['find_h'] = True

            if result['ecc'] < 10 and not author['find_i']:
                author['i10index'] = index - 1
                author['find_i'] = True

            id = 0
            if 'j' in result:
                id = result['j']['jId']
            elif 'c' in result:
                id = result['c']['cId']

            if id in self.ccf_list['A']:
                author['ccf_a_count'] += 1
            elif id in self.ccf_list['B']:
                author['ccf_b_count'] += 1
            elif id in self.ccf_list['C']:
                author['ccf_c_count'] += 1

            item['mag_id'] = result['id']
            item['title'] = result['ti']
            item['display_title'] = result['extended']['dn']
            item['year_published'] = result['y']
            item['date_published'] = result['d']
            if 'rId' in result:
                item['references'] = ','.join(map(lambda x: str(x), result['rId']))
                item['references_count'] = len(result['rId'])
            else:
                item['references'] = ''
                item['references_count'] = 0

            if 'd' in result['extended']:
                item['abstract'] = result['extended']['d']
            else:
                item['abstract'] = ''

            if 'vfn' in result['extended']:
                item['venue_fullname'] = result['extended']['vfn']
            else:
                item['venue_fullname'] = ''

            if 'vsn' in result['extended']:
                item['venue_shortname'] = result['extended']['vsn']
            else:
                item['venue_shortname'] = ''
            item['venue_info'] = result['extended']['bv']
            item['keywords'] = ','.join(result['w'])

            if 'doi' in result['extended']:
                item['doi'] = result['extended']['doi']
            else:
                item['doi'] = ''
            item['cite_count'] = result['cc']
            item['e_cite_count'] = result['ecc']

            if 'f' in result:
                item['fields'] = result['f']
            else:
                item['fields'] = []

            for au in result['aa']:
                if au['auId'] == response.meta['id']:
                    item['author_id'] = response.meta['id']
                    item['author_index'] = au['s']

            if 'j' in result:
                item['conference_id'] = ''
                item['conference_name'] = ''
                item['conference_instance_id'] = ''
                item['conference_instance_name'] = ''
                item['journal_id'] = result['j']['jId']
                item['journal_name'] = result['j']['jn']
                item['published_type'] = 'journal'
            elif 'c' in result:
                item['conference_id'] = result['c']['cId']
                item['conference_name'] = result['c']['cn']
                if 'ci' in result:
                    item['conference_instance_id'] = result['ci']['ciId']
                    item['conference_instance_name'] = result['ci']['cin']
                else:
                    item['conference_instance_id'] = ''
                    item['conference_instance_name'] = ''
                item['published_type'] = 'conference'
                item['journal_id'] = ''
                item['journal_name'] = ''
            else:
                item['conference_id'] = ''
                item['conference_name'] = ''
                item['conference_instance_id'] = ''
                item['conference_instance_name'] = ''
                item['journal_id'] = ''
                item['journal_name'] = ''

            yield item

        if author['total'] > index and index - response.meta['offset'] > 0:
            url = 'https://academic.microsoft.com/api/search/GetEntityResults'
            body = {
                'Query': 'And(Ty=\'0\',Composite(AA.AuId=' + str(response.meta['id']) + '))',
                'Limit': 8,
                'OrderBy': 'ECC',
                'SortAscending': 'false',
                'Offset': index,
            }
            yield Request(
                url=url,
                body=urllib.urlencode(body),
                method="POST", meta={'id': response.meta['id'], 'offset': index, 'hindex': author['hindex'], 'i10index': author['i10index'], 'total': author['total'],
                                     'find_h': author['find_h'], 'find_i': author['find_i'],
                                     'ccf_a_count': author['ccf_a_count'], 'ccf_b_count': author['ccf_b_count'], 'ccf_c_count': author['ccf_c_count']},
                headers=HEADER,
                dont_filter=True)
        else:
            res = MAGAuthorItem()
            res['author_id'] = author['author_id']
            res['hindex'] = author['hindex']
            res['i10index'] = author['i10index']
            res['ccf_a_count'] = author['ccf_a_count']
            res['ccf_b_count'] = author['ccf_b_count']
            res['ccf_c_count'] = author['ccf_c_count']
            res['paper_count'] = index

            yield res
            self.undo_url -= 1
            print '------UNDO:%d-----' %(self.undo_url)

        if self.undo_url <= self.url_limit * 0.6 and self.lock == False:
            self.lock = True
            response = GetTitle.get_authors_mag2(self.url_limit, self.spider_id, self.get_cnt)
            self.undo_url += self.url_limit
            self.lock = False
            self.get_cnt += 1

            for item in response:

                url = 'https://academic.microsoft.com/api/search/GetEntityResults'
                body = {
                    'Query': 'And(Ty=\'0\',Composite(AA.AuId=' + str(item[0]) + '))',
                    'Limit': 8,
                    'OrderBy': 'ECC',
                    'SortAscending': 'false',
                    'Offset': 0,
                }
                try:
                    yield Request(
                        url=url,
                        body=urllib.urlencode(body),
                        method="POST",
                        meta={'id': item[0], 'offset': 0, 'hindex': 0, 'i10index': 0, 'total': item[1],
                              'find_h': False, 'find_i': False,
                              'ccf_a_count': 0, 'ccf_b_count': 0, 'ccf_c_count': 0},
                        headers=HEADER,
                        dont_filter=True)
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

            

