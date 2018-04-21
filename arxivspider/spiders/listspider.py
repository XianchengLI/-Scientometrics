# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy import Request
from arxivspider.items import ArxivArticleItem


class ArxivListSpider(Spider):
    name = 'listspider'
    handle_httpstatus_list = [404]
    current_year = 93
    end_year = 17
    current_page = 0
    per_page = 2000
    def start_requests(self):
        url = 'https://arxiv.org/list/cs/' + str(self.current_year).zfill(2) + '?skip=' + str(self.current_page * self.per_page) + '&show=' + str(self.per_page)
        yield Request(url)

    def parse(self, response):
        total = int(response.xpath('//div[@id="dlpage"]/small/text()').extract_first()[11:-11])

        if total <= (self.current_page + 1) * self.per_page:
            if self.current_year == self.end_year:
                return
            else:
                if self.current_year == 99:
                    self.current_year = 00
                else:
                    self.current_year += 1
                self.current_page = 0
        else:
            self.current_page += 1

        article_arxiv_info_list = response.xpath('//div[@id="dlpage"]/dl/dt')
        article_list = response.xpath('//div[@id="dlpage"]/dl/dd')
        article_index = 0

        for article in article_list:
            while len(article_arxiv_info_list[article_index].xpath('./text()').re(ur'Error.*')) > 0:
                article_index += 1
            arxiv_info = article_arxiv_info_list[article_index]

            item = ArxivArticleItem()
            item['title'] = article.xpath('.//div[@class="list-title mathjax"]/text()').extract()[1].strip()
            item['authors'] = article.xpath('.//div[@class="list-authors"]/a/text()').extract()
            item['authors_link'] = article.xpath('.//div[@class="list-authors"]/a/@href').extract()

            venue_list = []
            for venue in article.xpath('.//div[@class="list-authors"]/text()').extract()[2:]:
                venue_list.append(venue.strip().strip(','))
            item['authors_venue'] = venue_list

            item['primary_subject'] = article.xpath('.//span[@class="primary-subject"]/text()').extract_first()
            subject_list = []
            subject_list.append(item['primary_subject'])
            for subject in article.xpath('.//div[@class="list-subjects"]/text()').extract()[2].lstrip(';').strip().split(';'):
                subject_list.append(subject.strip())
            item['subjects'] = subject_list

            item['authors_venue'] = venue_list
            item['arxiv_id'] = arxiv_info.xpath('.//span[@class="list-identifier"]/a/text()').extract_first()
            item['arxiv_link'] = arxiv_info.xpath('.//span[@class="list-identifier"]/a/@href').extract_first()
            item['arxiv_pdf_link'] = arxiv_info.xpath('.//span[@class="list-identifier"]/a/@href').extract()[1]

            comments = article.xpath('string(.//div[@class="list-comments"])').extract()[0].strip()
            if comments:
                item['comments'] = comments

            journal_reference = article.xpath('.//div[@class="list-journal-ref"]/text()').extract_first()
            if journal_reference:
                item['journal_reference'] = journal_reference

            yield item
            article_index += 1

        next_url = 'https://arxiv.org/list/cs/' + str(self.current_year).zfill(2) + '?skip=' + str(self.current_page * self.per_page) + '&show=' + str(self.per_page)
        yield Request(next_url)

