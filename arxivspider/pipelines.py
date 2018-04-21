# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

host = '2400:dd01:1034:1c00:569f:35ff:fe22:1bd8'
port = 3306
user = 'root'
passwd = 'xxxx'
db_name = 'arxiv_article'
charset = 'utf8'
db = MySQLdb.connect(host= host, port = port, user= user, passwd= passwd, db= db_name, charset= charset)
cursor = db.cursor()


class GetTitle(object):

    @classmethod
    def get_titles(cls, num, spider_name, get_cnt):
        num = str(num)
        get_cnt =str(get_cnt)
        sql="UPDATE articles SET mark = '%s %s' WHERE mark is NULL LIMIT %s;" %(spider_name, get_cnt, num)
        cursor.execute(sql)
        db.commit()
        sql="SELECT id, title, arxiv_link, authors FROM articles WHERE mark = '%s %s'  LIMIT %s;" %(spider_name, get_cnt, num)
        cursor.execute(sql)
        result=cursor.fetchall()  #fetchall返回所有数据列表
        res = []
        for row in result:
            tmp = row[1].split(' ')
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
            res.append((row[0], ' '.join(tmp_arr) ,row[2], row[3]))
        return res

    @classmethod
    def get_titles_mag(cls, num, spider_name, get_cnt):
        num = str(num)
        get_cnt =str(get_cnt)
        sql="UPDATE articles SET mag_mark = '%s %s' WHERE mag_mark is NULL OR mag_mark = 'DUP' LIMIT %s;" %(spider_name, get_cnt, num)
        cursor.execute(sql)
        db.commit()
        #sql = "SELECT id, title, authors FROM articles WHERE mag_num = 0  LIMIT %s;" % (num)
        sql = "SELECT id, title, authors FROM articles WHERE mag_mark = '%s %s'  LIMIT %s;" %(spider_name, get_cnt, num)
        cursor.execute(sql)
        result=cursor.fetchall()  #fetchall返回所有数据列表
        res = []
        for row in result:
            tmp = row[1].split(' ')
            tmp_arr1 = []
            for word in tmp:
                word = word.encode('utf-8')
                flag = True
                for i in range(len(word)):
                    if not (str(word[i]).isalnum() or word[i] in ['-', ',', ':']):
                        flag = False
                        break
                if flag:
                    tmp_arr1.append(word)
            tmp = row[2].split(',')
            tmp_arr2 = []
            for word in tmp:
                word = word.encode('utf-8')
                flag = True
                for i in range(len(word)):
                    if not (str(word[i]).isalnum() or word[i] in ['-', ',', ':', '.', ' ']):
                        flag = False
                        break
                if flag:
                    tmp_arr2.append(word)
            res.append((row[0], ' '.join(tmp_arr1), tmp_arr2))
        return res

    @classmethod
    def get_authors_mag(cls, num, spider_name, get_cnt):
        num = str(num)
        get_cnt =str(get_cnt)
        sql="UPDATE mag_authors_copy SET mark = '%s %s' WHERE mark is NULL LIMIT %s;" %(spider_name, get_cnt, num)
        cursor.execute(sql)
        db.commit()
        sql="SELECT mag_author_id FROM mag_authors_copy WHERE mark = '%s %s'  LIMIT %s;" %(spider_name, get_cnt, num)
        cursor.execute(sql)
        result=cursor.fetchall()  #fetchall返回所有数据列表
        res = []
        for row in result:
            res.append((row[0]))
        return res

    @classmethod
    def get_authors_mag2(cls, num, spider_name, get_cnt):
        local_db = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db_name, charset=charset)
        cursor = local_db.cursor()
        num = str(num)
        get_cnt = str(get_cnt)
        sql = "UPDATE mag_authors_copy2 SET mark = '%s %s' WHERE mark is NULL LIMIT %s;" % (spider_name, get_cnt, num)
        cursor.execute(sql)
        db.commit()
        sql = "SELECT mag_author_id, paper_count FROM mag_authors_copy2 WHERE mark = '%s %s'  LIMIT %s;" % (spider_name, get_cnt, num)
        cursor.execute(sql)
        result = cursor.fetchall()  # fetchall返回所有数据列表
        res = []
        for row in result:
            res.append((row[0], row[1]))
        return res

    @classmethod
    def get_ref(cls, num, spider_name, get_cnt):
        num = str(num)
        get_cnt =str(get_cnt)
        sql="UPDATE mag_articles_copy SET mark = '%s %s' WHERE mark is NULL LIMIT %s;" %(spider_name, get_cnt, num)
        cursor.execute(sql)
        db.commit()
        sql="SELECT mag_id FROM mag_articles_copy WHERE mark = '%s %s'  LIMIT %s;" %(spider_name, get_cnt, num)
        cursor.execute(sql)
        result=cursor.fetchall()  #fetchall返回所有数据列表
        res = []
        for row in result:
            res.append((row[0]))
        return res

    @classmethod
    def get_conference(cls, num, spider_name, get_cnt):
        num = str(num)
        get_cnt = str(get_cnt)
        sql = "UPDATE mag_conferences_copy SET mark = '%s %s' WHERE mark is NULL LIMIT %s;" % (spider_name, get_cnt, num)
        cursor.execute(sql)
        db.commit()
        sql = "SELECT mag_conference_id FROM mag_conferences_copy WHERE mark = '%s %s'  LIMIT %s;" % (spider_name, get_cnt, num)
        cursor.execute(sql)
        result = cursor.fetchall()  # fetchall返回所有数据列表
        res = []
        for row in result:
            res.append((row[0]))
        return res

    @classmethod
    def get_journal(cls, num, spider_name, get_cnt):
        num = str(num)
        get_cnt = str(get_cnt)
        sql = "UPDATE mag_journals_copy SET mark = '%s %s' WHERE mark is NULL LIMIT %s;" % (
        spider_name, get_cnt, num)
        cursor.execute(sql)
        db.commit()
        sql = "SELECT mag_journal_id FROM mag_journals_copy WHERE mark = '%s %s'  LIMIT %s;" % (
        spider_name, get_cnt, num)
        cursor.execute(sql)
        result = cursor.fetchall()  # fetchall返回所有数据列表
        res = []
        for row in result:
            res.append((row[0]))
        return res

    @classmethod
    def get_CCF_list(cls):
        res = {}
        for class_name in ['A', 'B', 'C']:
            list = []
            sql = "SELECT mag_conference_id FROM mag_conferences WHERE CCF_classification = '%s' ;" % (class_name)
            cursor.execute(sql)
            result = cursor.fetchall()  # fetchall返回所有数据列表
            for row in result:
                list.append((row[0]))
            sql = "SELECT mag_journal_id FROM mag_journals WHERE CCF_classification = '%s' ;" % (class_name)
            cursor.execute(sql)
            result = cursor.fetchall()  # fetchall返回所有数据列表
            for row in result:
                list.append((row[0]))
            res[class_name] = list
        return res

class GetVenue(object):

    @classmethod
    def get_affs(cls, num, spider_name):
        num = str(num)
        sql="UPDATE raw_aff SET country = '%s', mark = 'SEND' WHERE mark is NULL LIMIT %s;" %(spider_name, num)
        cursor.execute(sql)
        db.commit()
        sql="SELECT raw_aff_id, raw_aff_name FROM raw_aff WHERE country = '%s'  LIMIT %s;" %(spider_name, num)
        cursor.execute(sql)
        result=cursor.fetchall()  #fetchall返回所有数据列表
        res = []
        for row in result:
            res.append((row[0],row[1]))
        return res


class ArxivspiderPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        #读取settings中配置的数据库参数
        dbparams = dict(
            host=settings['MYSQL_HOST'],  
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        if spider.name == 'wikispider':
            query = self.dbpool.runInteraction(self.wiki_update, item)  # 调用插入的方法
        elif spider.name == 'articlespider':
            query = self.dbpool.runInteraction(self.article_update, item)  # 调用插入的方法
        elif spider.name == 'dblpspider':
            try:
                num = item['num']
                query = self.dbpool.runInteraction(self.dblp_arxiv_update, item) # 调用插入的方法
            except:
                query = self.dbpool.runInteraction(self.dblp_update, item) # 调用插入的方法
        elif spider.name == 'magspider':
            try:
                num = item['title']
                query = self.dbpool.runInteraction(self.mag_update, item) # 调用插入的方法
            except:
                query = self.dbpool.runInteraction(self.mag_arxiv_update, item) # 调用插入的方法
        elif spider.name == 'magauthorspider':
            query = self.dbpool.runInteraction(self.mag_author_update, item) # 调用插入的方法
        elif spider.name == 'magnewspider':
            query = self.dbpool.runInteraction(self.mag_new_update, item) # 调用插入的方法
        elif spider.name == 'ccfspider':
            query = self.dbpool.runInteraction(self.ccf_update, item) # 调用插入的方法
        elif spider.name == 'magconferencespider':
            query = self.dbpool.runInteraction(self.mag_conference_update, item) # 调用插入的方法
        elif spider.name == 'magjournalspider':
            query = self.dbpool.runInteraction(self.mag_journal_update, item) # 调用插入的方法
        elif spider.name == 'maghindexspider':
            try:
                num = item['hindex']
                query = self.dbpool.runInteraction(self.mag_hindex_author_update, item)  # 调用插入的方法
            except:
                query = self.dbpool.runInteraction(self.mag_hindex_update, item)  # 调用插入的方法

        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法

        return item

    # 写入数据库中
    # SQL语句在这里
    def article_update(self, tx, item):
        sql = "UPDATE arxiv_article.articles SET DOI = %s, first_submit_time = %s, report_number = %s , abstract = %s, journal_reference = %s,"\
              "DOI_link = %s, submission_history = %s, submitor = %s WHERE arxiv_id = %s"
        params = (item['DOI'], item['first_submit_time'], item['report_number'], item['abstract'], item['journal_reference'],item['DOI_link'],item['submission_history'],item['submitor'],item['arxiv_id'])
        tx.execute(sql, params)

    # 写入数据库中
    # SQL语句在这里
    def wiki_update(self, tx, item):
        sql = "UPDATE arxiv_article.raw_aff SET country = N%s, state = %s, locality = N%s , established_year = %s, website = %s,"\
              "mark = %s, wiki_name = N%s WHERE raw_aff_id = %s"
        params = (item['country'], item['state'], item['locality'], item['established_year'], item['website'],item['status'],item['wiki_name'],item['raw_aff_id'])
        tx.execute(sql, params)

    def dblp_update(self, tx, item):
        authors = ','.join(item['authors'])
        authors_link = ','.join(item['authors_link'])
        raw_link = ','.join(item['raw_link'])
        sql = "INSERT INTO arxiv_article.dblp_articles (arxiv_id, title, authors, authors_link, date_published, venue_link, dblp_key, status, raw_link, pagination, periodical, publication_issue, publication_volume, series)"\
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
        params = (item['arxiv_article_id'], item['title'], authors, authors_link, item['date_published'],item['venue_link'],item['dblp_key'],item['status'],raw_link,item['pagination'],item['periodical'],item['publication_issue'],item['publication_volume'],item['series'])
        tx.execute(sql, params)

    def dblp_arxiv_update(self, tx, item):
        sql = "UPDATE arxiv_article.articles SET mark = %s, dblp_num = %s WHERE id = %s"
        params = (item['mark'], item['num'], item['arxiv_article_id'])
        tx.execute(sql, params)

    def mag_update(self, tx, item):
        flag = False
        sql = "INSERT INTO arxiv_article.mag_articles (mag_id, arxiv_id, title, display_title, year_published, date_published, references_, journal_id, journal_name, conference_id, conference_name, conference_instance_id, conference_instance_name, venue_fullname, venue_shortname, venue_info, keywords, doi, cite_count, e_cite_count)"\
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
        params = (item['mag_id'], item['arxiv_article_id'], item['title'], item['display_title'],item['year_published'],item['date_published'],item['references'],item['journal_id'],item['journal_name'],item['conference_id'],item['conference_name'],item['conference_instance_id'],item['conference_instance_name'],item['venue_fullname'],item['venue_shortname'],item['venue_info'],item['keywords'],item['doi'],item['cite_count'],item['e_cite_count'])
        tx.execute(sql, params)
        flag = True
        '''
        try:
            tx.execute(sql, params)
            flag = True
        except:
            pass
        '''

        if flag:
            for author in item['authors']:
                try:
                    a = author['afId']
                except:
                    author['afId'] = ''
                    author['afN'] = ''
                    author['dAfN'] = ''

                sql_author = "INSERT INTO arxiv_article.mag_authors (mag_author_id, name, display_name, affiliation_id, affiliation_name, display_affiliation_name)" \
                             "VALUES(%s, %s, %s, %s, %s, %s );"
                params = (author['auId'], author['auN'], author['dAuN'], author['afId'], author['afN'], author['dAfN'])

                try:
                    tx.execute(sql_author, params)
                except:
                    sql_author = "INSERT INTO arxiv_article.mag_authors_to_update (mag_author_id, name, display_name, affiliation_id, affiliation_name, display_affiliation_name, mark)" \
                                 "VALUES(%s, %s, %s, %s, %s, %s, \'DONE\');"
                    params = (
                    author['auId'], author['auN'], author['dAuN'], author['afId'], author['afN'], author['dAfN'])
                    try:
                        tx.execute(sql_author, params)
                    except:
                        pass

                sql_author_connect = "INSERT INTO arxiv_article.mag2authors (mag_article_id, mag_author_id, author_index)" \
                                     "VALUES(%s, %s, %s );"
                params = (item['mag_id'], author['auId'], author['s'])
                tx.execute(sql_author_connect, params)

            for field in item['fields']:
                sql_field = "INSERT INTO arxiv_article.mag_fields (mag_field_id, mag_field_name)" \
                            "VALUES(%s, %s );"
                params = (field['fId'], field['fn'])
                try:
                    tx.execute(sql_field, params)
                except:
                    pass

                sql_field_connect = "INSERT INTO arxiv_article.mag2fields (mag_article_id, mag_field_id)" \
                                    "VALUES(%s, %s );"
                params = (item['mag_id'], field['fId'])
                tx.execute(sql_field_connect, params)

    def mag_author_update(self, tx, item):

        for coauthor in item['co_authors']:
            try:
                sql_author = "INSERT INTO arxiv_article.mag_authors (mag_author_id, display_name, mark)"\
                "VALUES(%s, %s , 'CO');"
                params = (coauthor['id'], coauthor['lt'])
                tx.execute(sql_author, params)
            except:
                pass
            try:
                sql_author_connect = "INSERT INTO arxiv_article.mag_author2coauthors (mag_author_id, mag_coauthor_id)"\
                "VALUES(%s, %s );"
                params = (item['author_id'], coauthor['id'])
                tx.execute(sql_author_connect, params)
            except:
                pass


        for field in item['fields']:
            sql_field = "INSERT INTO arxiv_article.mag_fields (mag_field_id, mag_field_name)"\
            "VALUES(%s, %s );"
            params = (field['id'], field['lt'])
            try:
                tx.execute(sql_field, params)
            except:
                pass

            sql_field_connect = "INSERT INTO arxiv_article.mag_author2fields (mag_author_id, mag_field_id)"\
            "VALUES(%s, %s );"
            params = (item['author_id'], field['id'])
            tx.execute(sql_field_connect, params)

        for journal in item['journals']:
            sql_journal = "INSERT INTO arxiv_article.mag_journals (mag_journal_id, journal_display_name)"\
            "VALUES(%s, %s );"
            params = (journal['id'], journal['lt'])
            try:
                tx.execute(sql_journal, params)
            except:
                pass

            sql_journal_connect = "INSERT INTO arxiv_article.mag_author2journals (mag_author_id, mag_journal_id)"\
            "VALUES(%s, %s );"
            params = (item['author_id'], journal['id'])
            tx.execute(sql_journal_connect, params)

        for conference in item['conferences']:
            sql_conference = "INSERT INTO arxiv_article.mag_conferences (mag_conference_id, conference_display_name)"\
            "VALUES(%s, %s );"
            params = (conference['id'], conference['lt'])
            try:
                tx.execute(sql_conference, params)
            except:
                pass

            sql_conference_connect = "INSERT INTO arxiv_article.mag_author2conferences (mag_author_id, mag_conference_id)"\
            "VALUES(%s, %s );"
            params = (item['author_id'], conference['id'])
            tx.execute(sql_conference_connect, params)

        sql = "UPDATE arxiv_article.mag_authors SET cite_count = %s, e_cite_count = %s, paper_count = %s , mark = 'DONE' WHERE mag_author_id = %s"
        params = (item['cite_count'], item['e_cite_count'], item['paper_count'], item['author_id'])
        try:
            tx.execute(sql, params)
        except:
            pass

        sql = "UPDATE arxiv_article.mag_authors_copy SET cite_count = %s, e_cite_count = %s, paper_count = %s , mark = 'DONE' WHERE mag_author_id = %s"
        params = (item['cite_count'], item['e_cite_count'], item['paper_count'], item['author_id'])
        try:
            tx.execute(sql, params)
        except:
            pass

    def mag_conference_update(self, tx, item):

        for field in item['fields']:
            sql_field = "INSERT INTO arxiv_article.mag_fields (mag_field_id, mag_field_name)" \
                        "VALUES(%s, %s );"
            params = (field['id'], field['lt'])
            try:
                tx.execute(sql_field, params)
            except:
                pass

            sql_field_connect = "INSERT INTO arxiv_article.mag_conference2fields (mag_conference_id, mag_field_id)" \
                                "VALUES(%s, %s );"
            params = (item['conference_id'], field['id'])
            tx.execute(sql_field_connect, params)


        sql = "UPDATE arxiv_article.mag_conferences SET cite_count = %s, e_cite_count = %s, paper_count = %s , conference_name = %s , conference_shortname = %s WHERE mag_conference_id = %s"
        params = (item['cite_count'], item['e_cite_count'], item['paper_count'], item['whole'], item['short'], item['conference_id'])
        try:
            tx.execute(sql, params)
        except:
            pass

        sql = "UPDATE arxiv_article.mag_conferences_copy SET mark = 'DONE' WHERE mag_conference_id = %s"
        params = (item['conference_id'])
        try:
            tx.execute(sql, params)
        except:
            pass

    def mag_journal_update(self, tx, item):

        for field in item['fields']:
            sql_field = "INSERT INTO arxiv_article.mag_fields (mag_field_id, mag_field_name)" \
                        "VALUES(%s, %s );"
            params = (field['id'], field['lt'])
            try:
                tx.execute(sql_field, params)
            except:
                pass

            sql_field_connect = "INSERT INTO arxiv_article.mag_journal2fields (mag_journal_id, mag_field_id)" \
                                "VALUES(%s, %s );"
            params = (item['journal_id'], field['id'])
            tx.execute(sql_field_connect, params)


        sql = "UPDATE arxiv_article.mag_journals SET cite_count = %s, e_cite_count = %s, paper_count = %s , journal_name = %s WHERE mag_journal_id = %s"
        params = (item['cite_count'], item['e_cite_count'], item['paper_count'], item['name'], item['journal_id'])
        try:
            tx.execute(sql, params)
        except:
            pass

        sql = "UPDATE arxiv_article.mag_journals_copy SET mark = 'DONE' WHERE mag_journal_id = %s"
        params = (item['journal_id'])
        try:
            tx.execute(sql, params)
        except:
            pass

    def mag_new_update(self, tx, item):

        sql = "UPDATE arxiv_article.mag_articles SET references_ = %s, references_count = %s, references_query = %s , abstract = %s WHERE mag_id = %s"
        params = (item['references'], item['references_count'], item['references_query'], item['abstract'], item['mag_id'])
        try:
            tx.execute(sql, params)
        except:
            pass


        sql = "UPDATE arxiv_article.mag_articles_copy SET mark = 'DONE' WHERE mag_id = %s" % (item['mag_id'])
        try:
            tx.execute(sql)
        except:
            pass

    def mag_hindex_update(self, tx, item):

        sql = "INSERT INTO arxiv_article.mag_articles_all (mag_id, title, display_title, year_published, date_published, references_, journal_id, journal_name, conference_id, conference_name, conference_instance_id, conference_instance_name, venue_fullname, venue_shortname, venue_info, keywords, doi, cite_count, e_cite_count, references_count, abstract)" \
              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
        params = (
        item['mag_id'], item['title'], item['display_title'], item['year_published'],
        item['date_published'], item['references'], item['journal_id'], item['journal_name'], item['conference_id'],
        item['conference_name'], item['conference_instance_id'], item['conference_instance_name'],
        item['venue_fullname'], item['venue_shortname'], item['venue_info'], item['keywords'], item['doi'],
        item['cite_count'], item['e_cite_count'], item['references_count'], item['abstract'])
        try:
            tx.execute(sql, params)
        except:
            pass

        sql_author_connect = "INSERT INTO arxiv_article.mag2authors_all (mag_article_id, mag_author_id, author_index)" \
                             "VALUES(%s, %s, %s );"
        params = (item['mag_id'], item['author_id'], item['author_index'])
        tx.execute(sql_author_connect, params)


        for field in item['fields']:
            sql_field = "INSERT INTO arxiv_article.mag_fields (mag_field_id, mag_field_name)" \
                        "VALUES(%s, %s );"
            params = (field['fId'], field['fn'])
            try:
                tx.execute(sql_field, params)
            except:
                pass

            sql_field_connect = "INSERT INTO arxiv_article.mag2fields_all (mag_article_id, mag_field_id)" \
                                "VALUES(%s, %s );"
            params = (item['mag_id'], field['fId'])
            tx.execute(sql_field_connect, params)

    def mag_hindex_author_update(self, tx, item):

        sql = "UPDATE arxiv_article.mag_authors SET h_index = %s, i10_index = %s, CCF_A_count = %s, CCF_B_count = %s, CCF_C_count = %s, paper_count = %s WHERE mag_author_id = %s"
        params = (
        item['hindex'], item['i10index'], item['ccf_a_count'], item['ccf_b_count'], item['ccf_c_count'], item['paper_count'], item['author_id'])
        tx.execute(sql, params)

        sql = "UPDATE arxiv_article.mag_authors_copy2 SET mark = 'DONE' WHERE mag_author_id = %s" %(item['author_id'])
        tx.execute(sql)


    def mag_arxiv_update(self, tx, item):
        sql = "UPDATE arxiv_article.articles SET mag_mark = %s, mag_num = %s WHERE id = %s"
        params = (item['mark'], item['num'], item['arxiv_article_id'])
        tx.execute(sql, params)

    def ccf_update(self, tx, item):
        sql = "INSERT INTO arxiv_article.ccf_2015 (CCF_name, CCF_abbreviation, CCF_pub, CCF_dblplink, CCF_type, CCF_classification, computercategory_computerCategory_id)" \
                         "VALUES(%s, %s, %s, %s, %s, %s, %s );"
        params = (item['name'], item['abbr'], item['pub'], item['dblplink'], item['type'], item['classification'], item['category'])
        tx.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue
