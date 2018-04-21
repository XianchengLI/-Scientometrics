# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy import Request
from arxivspider.items import *
from arxivspider.pipelines import GetTitle
from fuzzywuzzy import fuzz
import urllib2
import urllib
import json
import socket
import random
import string


class MAGArticleSpider(Spider):
    name = 'magspider'
    handle_httpstatus_list = [404]
    spider_id = socket.getfqdn(socket.gethostname()) + '_' + str(random.randint(0, 100))
    url_limit = 200
    undo_url = 200
    get_cnt = 0
    countries = []

    def start_requests(self):
        response = GetTitle.get_titles_mag(self.url_limit, self.spider_id, self.get_cnt)
        self.get_cnt += 1
        print response
        for item in response:
            url = 'https://academic.microsoft.com/api/search/GetEntityResults'
            body = {'Query' : '@' + item[1] + '@',}
            try:
                yield Request(url='https://academic.microsoft.com/api/search/GetEntityResults?correlationId=591669b2-5a23-4d7c-9c59-6040cfbf67a5', 
                body=urllib.urlencode(body),
                method="POST",meta={'id': item[0], 'name': self.parse_string(item[1]), 'authors': map(self.parse_string, item[2])},
                headers=HEADER)
            except:
                self.undo_url -= 1

    def parse_string(self, s):
        s = s.replace('-', ' ')
        for c in string.punctuation:
            s = s.replace(c, "")
        s = ' '.join(s.split())
        s = s.lower()
        return s

    def replace_string(self, s):
        tmp = s.split(' ')
        tmp_arr = []
        for word in tmp:
            word = word.encode('utf-8')
            flag = True
            for i in range(len(word)):
                if not (str(word[i]).isalnum() or word[i] in ['-', ',', ':']):
                    flag = False
                    break
            if flag:
                tmp_arr.append(word)
        return ' '.join(tmp_arr)

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        print response.meta['authors']

        num = 0
        try:
            for result in jsonresponse['results']:

                '''
                flag = False
                if response.meta['name'] == self.parse_string(result['extended']['dn']) : flag = True
                if response.meta['name'] == self.parse_string(result['ti'][8:-9]) : flag = True
                if flag == False : continue
                '''

                if fuzz.ratio(response.meta['name'], self.parse_string(self.replace_string(result['extended']['dn']))) < 80:
                    continue
                else:
                    print '_____________!!!!!!name is match!!!!!!!!_________'
                    print response.meta['name']
                    print self.parse_string(self.replace_string(result['extended']['dn']))

                if len(response.meta['authors']) > 0:
                    not_found_cnt = 0
                    for author in result['aa']:
                        flag = True
                        for name in response.meta['authors']:
                            if fuzz.token_sort_ratio(author['auN'], name) > 60 or fuzz.partial_ratio(author['auN'], name) > 60:
                                flag = False
                        if flag:
                            not_found_cnt += 1
                            continue
                    if len(result['aa']) == not_found_cnt:
                        print '_____________!!!!!!author not match!!!!!!!!_________'
                        continue

                num += 1
                item = MAGArticleItem()

                item['arxiv_article_id'] = response.meta['id']
                item['mag_id'] = result['id']
                item['title'] = result['ti'][8:-9]
                item['display_title'] = result['extended']['dn']
                item['year_published'] = result['y']
                item['date_published'] = result['d']
                if 'rId' in result:
                    item['references'] = ','.join(map(lambda x: str(x), result['rId']))
                else:
                    item['references'] = ''

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

                item['authors'] = result['aa']

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

            item = UpdateArticleItem()
            item['arxiv_article_id'] = response.meta['id']
            item['num'] = num
            if num == len(jsonresponse['results']) and num != 0:
                item['mark'] = 'DONE_FUZZY'
            elif num == 0:
                item['mark'] = 'NOTFOUND_FUZZY'
            else:
                item['mark'] = 'PARTLY_FUZZY'
            yield item

            self.undo_url -= 1
        except:
            self.undo_url -= 1

        print '------UNDO:%d-----' %(self.undo_url)

        if self.undo_url <= self.url_limit * 0.4 :
            self.undo_url += self.url_limit
            response = GetTitle.get_titles_mag(self.url_limit, self.spider_id, self.get_cnt)
            self.get_cnt += 1
            for item in response:
                url = 'https://academic.microsoft.com/api/search/GetEntityResults'
                body = {'Query' : '@' + item[1] + '@',}
                try:
                    yield Request(
                        url='https://academic.microsoft.com/api/search/GetEntityResults?correlationId=591669b2-5a23-4d7c-9c59-6040cfbf67a5',
                        body=urllib.urlencode(body),
                        method="POST", meta={'id': item[0], 'name': self.parse_string(item[1]),
                                             'authors': map(self.parse_string, item[2])},
                        headers=HEADER)
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

            

