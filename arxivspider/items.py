# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArxivArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    authors_link = scrapy.Field()
    authors_venue = scrapy.Field()
    comments = scrapy.Field()
    report_number = scrapy.Field()
    journal_reference = scrapy.Field()
    DOI = scrapy.Field()
    DOI_link = scrapy.Field()
    first_submit_time = scrapy.Field()
    abstract = scrapy.Field()
    subjects = scrapy.Field()
    primary_subject = scrapy.Field()
    arxiv_link = scrapy.Field()
    arxiv_id = scrapy.Field()
    arxiv_pdf_link = scrapy.Field()
    submission_history = scrapy.Field()
    submitor = scrapy.Field()

class WikiVenueItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    wiki_name = scrapy.Field()
    locality = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()
    raw_aff_id = scrapy.Field()
    established_year = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()

class DBLPArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    arxiv_article_id = scrapy.Field()
    dblp_key = scrapy.Field()
    raw_link = scrapy.Field()
    authors_link = scrapy.Field()
    authors = scrapy.Field()
    title = scrapy.Field() 
    venue_link = scrapy.Field()
    periodical = scrapy.Field()
    publication_volume = scrapy.Field()
    publication_issue = scrapy.Field()
    series = scrapy.Field()
    date_published = scrapy.Field()
    pagination = scrapy.Field()
    status = scrapy.Field()

class MAGArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    arxiv_article_id = scrapy.Field()
    mag_id = scrapy.Field()
    title = scrapy.Field()
    display_title = scrapy.Field()
    year_published = scrapy.Field()
    date_published = scrapy.Field()
    references = scrapy.Field() 
    references_count = scrapy.Field()
    references_query = scrapy.Field()
    abstract = scrapy.Field()
    journal_id = scrapy.Field()
    journal_name = scrapy.Field()
    conference_id = scrapy.Field()
    conference_name = scrapy.Field()
    conference_instance_id = scrapy.Field()
    conference_instance_name = scrapy.Field()
    published_type = scrapy.Field()
    venue_fullname = scrapy.Field()
    venue_shortname = scrapy.Field()
    venue_info = scrapy.Field()
    keywords = scrapy.Field()
    doi = scrapy.Field()
    cite_count = scrapy.Field()
    e_cite_count = scrapy.Field()
    fields = scrapy.Field()
    authors = scrapy.Field()
    author_id = scrapy.Field()
    author_index = scrapy.Field()

class MAGAuthorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author_id = scrapy.Field()
    cite_count = scrapy.Field()
    e_cite_count = scrapy.Field()
    paper_count = scrapy.Field()
    hindex = scrapy.Field()
    i10index = scrapy.Field()
    ccf_a_count = scrapy.Field()
    ccf_b_count = scrapy.Field()
    ccf_c_count = scrapy.Field()

    fields = scrapy.Field()
    co_authors = scrapy.Field()
    journals = scrapy.Field()
    conferences = scrapy.Field()

class MAGConferenceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    conference_id = scrapy.Field()
    cite_count = scrapy.Field()
    e_cite_count = scrapy.Field()
    paper_count = scrapy.Field()
    fields = scrapy.Field()
    whole = scrapy.Field()
    short = scrapy.Field()

class MAGJournalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    journal_id = scrapy.Field()
    cite_count = scrapy.Field()
    e_cite_count = scrapy.Field()
    paper_count = scrapy.Field()
    fields = scrapy.Field()
    name = scrapy.Field()

class CCFItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    abbr = scrapy.Field()
    dblplink = scrapy.Field()
    type = scrapy.Field()
    pub = scrapy.Field()
    classification = scrapy.Field()
    category = scrapy.Field()

class UpdateArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    arxiv_article_id = scrapy.Field()
    num = scrapy.Field()
    mark = scrapy.Field()
