# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy import Request
from arxivspider.items import ArxivArticleItem
import urllib2
import json
import socket


class ArxivArticleSpider(Spider):
    name = 'articlespider'
    host = 'http://192.241.218.11'
    handle_httpstatus_list = [404]
    spider_id = socket.getfqdn(socket.gethostname())
    url_limit = 300
    undo_url = 300

    def start_requests(self):
        response = urllib2.urlopen(self.host + '/getArticle?spider_id=' + self.spider_id + '&limit=' + str(self.url_limit))
        data = json.load(response)
        for url in data['result']:
            print url
            yield Request(url)

    def parse(self, response):
        item = ArxivArticleItem()
        item['title'] = response.xpath('//h1[@class="title mathjax"]/text()').extract_first()[1:]
        item['authors'] = response.xpath('//div[@class="authors"]/a/text()').extract()
        item['authors_link'] = response.xpath('//div[@class="authors"]/a/@href').extract()
        item['first_submit_time'] = response.xpath('//div[@class="dateline"]/text()').extract_first()[14:-1]
        item['abstract'] = response.xpath('//blockquote[@class="abstract mathjax"]/text()').extract()[1].replace("\n", " ")
        item['primary_subject'] = response.xpath('//span[@class="primary-subject"]/text()').extract_first()
        item['subjects'] = response.xpath('string(//td[@class="tablecell subjects"]/text())').extract_first()
        item['arxiv_id'] = response.xpath('//td[@class="tablecell arxivid"]/a/text()').extract_first()
        item['arxiv_link'] = response.xpath('//td[@class="tablecell arxivid"]/a/@href').extract()[0]
        item['arxiv_pdf_link'] = response.xpath('//div[@class="full-text"]/ul/li/a/@href').extract_first()

        submission = response.xpath('//div[@class="submission-history"]/node()').extract()
        item['submitor'] = submission[2][7:-2]
        i = (len(submission) - 7)/4
        sub_arr = []
        while i > 0:
            sub_arr.append(submission[(len(submission) - i*4) + 1][5:])
            i -= 1
        item['submission_history'] = ",".join(sub_arr)

        comments = response.xpath('//td[@class="tablecell comments"]/text()').extract_first()
        if comments:
            item['comments'] = comments
        else:
            item['comments'] = ''

        report_number = response.xpath('//td[@class="tablecell report-number"]/text()').extract_first()
        if report_number:
            item['report_number'] = report_number
        else:
            item['report_number'] = ''

        DOI = response.xpath('//td[@class="tablecell doi"]/a/text()').extract_first()
        if DOI:
            item['DOI'] = DOI
            item['DOI_link'] = response.xpath('//td[@class="tablecell doi"]/a/@href').extract_first()
        else:
            item['DOI'] = ''
            item['DOI_link'] = ''

        journal_reference = response.xpath('//td[@class="tablecell jref"]/text()').extract_first()
        if journal_reference:
            item['journal_reference'] = journal_reference.replace("\n", "")
        else:
            item['journal_reference'] = ''

        yield item
        self.undo_url -= 1
        if self.undo_url < self.url_limit * 0.5 :
            self.undo_url += self.url_limit
            response = urllib2.urlopen(self.host + '/getArticle?spider_id=' + self.spider_id + '&limit=' + str(self.url_limit))
            data = json.load(response)
            for url in data['result']:
                yield Request(url)
            

