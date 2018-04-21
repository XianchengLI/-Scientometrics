# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy import Request
from arxivspider.items import *
from arxivspider.pipelines import GetTitle
import urllib2
import json
import socket


class DBLPArticleSpider(Spider):
    name = 'dblpspider'
    handle_httpstatus_list = [404]
    spider_id = socket.getfqdn(socket.gethostname())
    url_limit = 200
    undo_url = 200
    get_cnt = 0
    countries = []

    def start_requests(self):
        response = GetTitle.get_titles(self.url_limit, self.spider_id, self.get_cnt)
        self.get_cnt += 1
        for item in response:
            url = 'http://dblp.uni-trier.de/search?q=' + item[1].replace(" ", "%20")
            yield Request(url=url, meta={'id': item[0], 'arxiv_link': item[2], 'authors': item[3]})

    def parse(self, response):
        xpath_list = '//ul[@class="publ-list"]/li[@class="entry article"]|'\
                        '//ul[@class="publ-list"]/li[@class="entry inproceedings"]|'\
                        '//ul[@class="publ-list"]/li[@class="entry informal"]|'\
                        '//ul[@class="publ-list"]/li[@class="entry withdrawn"]'
        article_list = response.xpath(xpath_list)
        authors_list = []
        item_cnt = 0
        if_withdrawn = False
        if_notfound = False

        if len(article_list) == 0:
            if_notfound = True

        for article in article_list:
            raw_url = article.xpath('.//nav[@class="publ"]/ul/li[1]/div[@class="body"]/ul/li/a/@href').extract_first()
            if raw_url is None:
                continue
            else:
                raw_url = raw_url.split('/')[-1]
            if raw_url == response.meta['arxiv_link'].split('/')[-1]:
                authors_list = article.xpath('.//div[@class="data"]/span[@itemprop="author"]/a/span/text()').extract()
                break

        if len(authors_list) == 0: # arxiv paper not found
            authors_list = response.meta['authors'].split(',')

        for article in article_list:
            if article.xpath('.//div[@class="data"]/span[@class="title"]/text()').extract_first() == '(Withdrawn)':
                if_withdrawn = True
                break

            item = DBLPArticleItem()

            item['arxiv_article_id'] = response.meta['id']

            item['dblp_key'] = article.xpath('.//nav[@class="publ"]/ul/li[2]/div[@class="body"]/ul[@class="bullets"]/li/small/text()').extract_first()
            item['raw_link'] = article.xpath('.//nav[@class="publ"]/ul/li[1]/div[@class="body"]/ul/li/a/@href').extract()
            item['authors_link'] = article.xpath('.//div[@class="data"]/span[@itemprop="author"]/a/@href').extract()
            authors = article.xpath('.//div[@class="data"]/span[@itemprop="author"]/a/span/text()').extract()
            flag = False
            for author in authors:
                if author in authors_list:
                    flag = True
                    break

            if flag:
                item['authors'] = authors
            else:
                continue

            item['title'] = article.xpath('.//div[@class="data"]/span[@class="title"]/text()').extract_first()
            item['venue_link'] = article.xpath('.//div[@class="data"]/a/@href').extract_first()
            item['periodical'] = article.xpath('.//div[@class="data"]/a/span[@itemtype="http://schema.org/Periodical"]/span/text()').extract_first()
            item['publication_volume'] = article.xpath('.//div[@class="data"]/a/span[@itemtype="http://schema.org/PublicationVolume"]/span/text()').extract_first()
            item['publication_issue'] = article.xpath('.//div[@class="data"]/a/span[@itemtype="http://schema.org/PublicationIssue"]/span/text()').extract_first()
            item['series'] = article.xpath('.//div[@class="data"]/a/span[@itemtype="http://schema.org/Series"]/span/text()').extract_first()
            item['date_published'] = article.xpath('.//div[@class="data"]/a/span[@itemprop="datePublished"]/text()|.//div[@class="data"]/span[@itemprop="datePublished"]/text()').extract_first()
            item['pagination'] = article.xpath('.//div[@class="data"]/span[@itemprop="pagination"]/text()').extract_first()
            item['status'] = article.xpath('./@class').extract_first()[6:]

            for value in item:
                if item[value] is None:
                    item[value] = ''

            yield item
            item_cnt += 1

        item = UpdateArticleItem()
        item['arxiv_article_id'] = response.meta['id']
        item['num'] = item_cnt
        if if_withdrawn:
            item['mark'] = 'WITHDRAWN'
        if if_notfound:
            item['mark'] = 'NOTFOUND'
        else:
            item['mark'] = 'DONE'
        yield item

        self.undo_url -= 1
        print '------UNDO:%d-----' %(self.undo_url)

        if self.undo_url <= self.url_limit * 0.5 :
            self.undo_url += self.url_limit
            response = GetTitle.get_titles(self.url_limit, self.spider_id, self.get_cnt)
            self.get_cnt += 1
            for item in response:
                url = 'http://dblp.uni-trier.de/search?q=' + item[1].replace(" ", "%20")
                yield Request(url=url, meta={'id': item[0], 'arxiv_link': item[2], 'authors': item[3]})

            

