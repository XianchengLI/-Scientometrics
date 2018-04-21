# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy import Request
from arxivspider.items import WikiVenueItem
from arxivspider.pipelines import GetVenue
from lxml import html
import requests
import socket


class WikiVenueSpider(Spider):
    name = 'wikispider'
    handle_httpstatus_list = [404, 302]
    spider_id = socket.getfqdn(socket.gethostname())
    url_limit = 100
    undo_url = 100
    countries = []

    def start_requests(self):
        page = requests.get('https://www.state.gov/misc/list/')
        tree = html.fromstring(page.text)
        self.countries = tree.xpath('//div[@class="l-wrap"]/ul[@class="no-bullet"]/li/a/text()') # 获取国家列表
        self.countries.append('United States')
        response = GetVenue.get_affs(self.url_limit, self.spider_id)
        for item in response:
            url = 'https://en.wikipedia.org/w/index.php?search=' + item[1].replace(" ", "%20")
            yield Request(url=url, meta={'raw_aff_id': item[0]})

    def parse(self, response):
        if response.status == 302:
            yield Request(url=response.headers['location'], meta={'raw_aff_id': response.meta['raw_aff_id']})
            return
        item = WikiVenueItem()
        status = response.xpath('//h1[@id="firstHeading"]/text()').re(ur'Search results.*')
        if status:
            item['status'] = 'search'
        else:
            item['status'] = 'find'

        item['raw_aff_id'] = response.meta['raw_aff_id']
        item['wiki_name'] = ''
        item['established_year'] = ''
        item['website'] = ''
        item['country'] = ''
        item['state'] = ''
        item['locality'] = ''

        item['wiki_name'] = response.xpath('//h1[@id="firstHeading"]/text()').extract_first()
        item['established_year'] = response.xpath('//table[@class="infobox vcard"]/tr/th[text()="Founded"]/following-sibling::td/text()|//table[@class="infobox vcard"]/tr/th[text()="Established"]/following-sibling::td/text()').extract_first()
        item['website'] = response.xpath('//table[@class="infobox vcard"]/tr/th[text()="Website"]/following-sibling::td/span/a/@href').extract_first()

        xpath_country = '//table[@class="infobox vcard"]/tr/th[text()="Headquarters"]/following-sibling::td/span[@class="country-name"]/a/@title|'\
                        '//table[@class="infobox vcard"]/tr/th[text()="Headquarters"]/following-sibling::td/span[@class="country-name"]/text()|'\
                        '//table[@class="infobox vcard"]/tr/th[text()="Address"]/following-sibling::td/span[@class="country-name"]/a/@title|'\
                        '//table[@class="infobox vcard"]/tr/th[text()="Address"]/following-sibling::td/span[@class="country-name"]/text()|'\
                        '//table[@class="infobox vcard"]/tr/th[text()="Location"]/following-sibling::td/span[@class="country-name"]/a/@title|'\
                        '//table[@class="infobox vcard"]/tr/th[text()="Location"]/following-sibling::td/span[@class="country-name"]/text()'
        countries = response.xpath(xpath_country).extract()
        if len(countries) == 1:
            item['country'] = countries[0]
            if countries[0] not in self.countries:
                item['status'] = 'county_not_find'
        else:
            if len(countries) == 0:
                xpath_country = '//table[@class="infobox vcard"]/tr/th[text()="Headquarters"]/following-sibling::td|'\
                        '//table[@class="infobox vcard"]/tr/th[text()="Address"]/following-sibling::td|'\
                        '//table[@class="infobox vcard"]/tr/th[text()="Location"]/following-sibling::td'
                parent = response.xpath(xpath_country)
                if len(parent) > 0:
                    xpath_country = './text()|.//span/text()|.//a/@title'
                    print parent
                    text = parent[0].xpath(xpath_country).extract()
                    for i in text:
                        countries += map(self.strip,i.split(','))
                print countries
            for c in countries:
                if c in self.countries:
                    item['country'] = c

        print item['country']
        if item['country'] == '' and item['status'] == 'find':
            item['status'] = 'county_not_find'

        xpath_state = '//table[@class="infobox vcard"]/tr/th[text()="Headquarters"]/following-sibling::td/span[@class="state"]/a/@title|'\
                      '//table[@class="infobox vcard"]/tr/th[text()="Headquarters"]/following-sibling::td/span[@class="state"]/text()|'\
                      '//table[@class="infobox vcard"]/tr/th[text()="Address"]/following-sibling::td/span[@class="state"]/a/@title|'\
                      '//table[@class="infobox vcard"]/tr/th[text()="Address"]/following-sibling::td/span[@class="state"]/text()|'\
                      '//table[@class="infobox vcard"]/tr/th[text()="Location"]/following-sibling::td/span[@class="state"]/a/@title|'\
                      '//table[@class="infobox vcard"]/tr/th[text()="Location"]/following-sibling::td/span[@class="state"]/text()'
                      
        item['state'] = response.xpath(xpath_state).extract_first()

        xpath_locality = '//table[@class="infobox vcard"]/tr/th[text()="Headquarters"]/following-sibling::td/span[@class="locality"]/a/@title|'\
                      '//table[@class="infobox vcard"]/tr/th[text()="Headquarters"]/following-sibling::td/span[@class="locality"]/text()|'\
                      '//table[@class="infobox vcard"]/tr/th[text()="Address"]/following-sibling::td/span[@class="locality"]/a/@title|'\
                      '//table[@class="infobox vcard"]/tr/th[text()="Address"]/following-sibling::td/span[@class="locality"]/text()|'\
                      '//table[@class="infobox vcard"]/tr/th[text()="Location"]/following-sibling::td/span[@class="locality"]/a/@title|'\
                      '//table[@class="infobox vcard"]/tr/th[text()="Location"]/following-sibling::td/span[@class="locality"]/text()'
                      
        item['locality'] = response.xpath(xpath_locality).extract_first()

        yield item
        self.undo_url -= 1
        print '------UNDO:%d-----' %(self.undo_url)

        if self.undo_url <= self.url_limit * 0.3 :
            self.undo_url = self.url_limit
            response = GetVenue.get_affs(self.url_limit, self.spider_id)
            print response
            for item in response:
                url = 'https://en.wikipedia.org/w/index.php?search=' + item[1].replace(" ", "%20")
                yield Request(url=url, meta={'raw_aff_id': item[0]})
    
    @classmethod
    def strip(cls,x):
        return x.strip()
            

