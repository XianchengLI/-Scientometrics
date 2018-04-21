# -*- coding: utf-8 -*-

# Scrapy settings for arxivspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'arxivspider'

SPIDER_MODULES = ['arxivspider.spiders']
NEWSPIDER_MODULE = 'arxivspider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'arxivspider (+http://www.yourdomain.com)'

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 256

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.2
DOWNLOAD_TIMEOUT = 60
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 64

# Retry many times since proxies often fail
RETRY_TIMES = 20
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408, 429, 302]
REDIRECTS_ENABLED = False

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
COOKIES_DEBUG = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'arxivspider.middlewares.ArxivspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'arxivspider.middlewares.MyCustomDownloaderMiddleware': 543,
	'arxivspider.middlewares.RandomUserAgent': 1, #随机user agent
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'arxivspider.middlewares.ProxyMiddleware': 100,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'arxivspider.pipelines.ArxivspiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]

PROXIES = [
    
{'ip_port': '76.69.194.71:3128'},
{'ip_port': '116.11.254.37:80'},
{'ip_port': '46.150.174.192:65103'},
{'ip_port': '50.201.51.216:8080'},
{'ip_port': '145.239.137.83:3128'},
{'ip_port': '186.46.156.202:65309'},
{'ip_port': '187.95.125.87:3128'},
{'ip_port': '195.154.42.249:3128'},
{'ip_port': '69.30.212.186:3128'},
{'ip_port': '146.185.151.66:8080'},
{'ip_port': '192.228.250.98:8080'},
{'ip_port': '180.246.59.101:8080'},
{'ip_port': '177.38.13.16:53281'},
{'ip_port': '14.207.133.97:8080'},
{'ip_port': '190.214.56.138:53281'},
{'ip_port': '52.178.197.34:3128'},
{'ip_port': '202.53.174.162:8080'},
{'ip_port': '180.250.213.130:8080'},
{'ip_port': '186.227.8.21:3128'},
{'ip_port': '182.253.78.18:3128'},
{'ip_port': '13.82.97.73:3128'},
{'ip_port': '177.89.214.214:53281'},
{'ip_port': '198.168.140.84:3128'},
{'ip_port': '128.199.126.183:3128'},
{'ip_port': '116.71.137.162:53281'},
{'ip_port': '87.229.76.9:53281'},
{'ip_port': '112.216.16.250:3128'},
{'ip_port': '42.112.209.164:8080'},
{'ip_port': '216.100.88.229:8080'},
{'ip_port': '186.226.162.237:3128'},
{'ip_port': '198.168.140.84:3128'},
{'ip_port': '80.211.232.225:3128'},
{'ip_port': '113.160.55.242:52335'},
{'ip_port': '31.135.64.76:3128'},
{'ip_port': '180.250.74.210:8080'},
{'ip_port': '213.154.3.103:3128'},
{'ip_port': '188.166.232.174:8080'},
{'ip_port': '50.201.51.216:8080'},
{'ip_port': '200.138.196.34:8088'},
{'ip_port': '182.16.178.194:8080'},
{'ip_port': '213.174.123.194:3128'},
{'ip_port': '181.30.101.242:3128'},
{'ip_port': '195.154.42.249:3128'},
{'ip_port': '163.172.93.129:3128'},
{'ip_port': '161.132.104.51:3130'},
{'ip_port': '146.185.151.66:8080'},
{'ip_port': '186.103.169.164:8080'},
{'ip_port': '50.59.162.78:8088'},
{'ip_port': '77.65.13.26:8080'},
{'ip_port': '216.100.88.229:8080'},
{'ip_port': '186.226.162.237:3128'},
{'ip_port': '198.168.140.84:3128'},
{'ip_port': '117.52.91.121:80'},
{'ip_port': '201.164.47.210:3128'},
{'ip_port': '109.203.124.226:80'},
{'ip_port': '80.211.232.225:3128'},
{'ip_port': '31.135.64.76:3128'},
{'ip_port': '213.154.3.103:3128'},
{'ip_port': '121.172.54.218:3128'},
{'ip_port': '202.29.20.124:80'},
{'ip_port': '188.166.232.174:8080'},
{'ip_port': '50.201.51.216:8080'},
{'ip_port': '182.16.178.194:8080'},
{'ip_port': '213.174.123.194:3128'},
{'ip_port': '195.154.42.249:3128'},
{'ip_port': '163.172.93.129:3128'},
{'ip_port': '161.132.104.51:3130'},
{'ip_port': '146.185.151.66:8080'},
{'ip_port': '50.59.162.78:8088'},
{'ip_port': '36.74.83.28:3128'},
{'ip_port': '161.132.104.51:3130'},
{'ip_port': '51.15.41.168:3128'},
{'ip_port': '128.199.203.105:8080'},
{'ip_port': '31.182.52.156:3129'},
{'ip_port': '186.226.162.237:3128'},
{'ip_port': '109.203.124.226:80'},
{'ip_port': '212.47.252.49:3128'},
{'ip_port': '213.174.123.194:3128'},
{'ip_port': '173.212.246.178:3128'},
{'ip_port': '177.37.164.228:3128'},
{'ip_port': '83.69.245.150:53281'},
{'ip_port': '90.150.87.130:3128'},
{'ip_port': '137.74.163.137:3128'},
{'ip_port': '31.145.111.12:65103'},
{'ip_port': '46.253.12.46:53281'},
{'ip_port': '198.168.140.84:3128'},
{'ip_port': '40.71.93.5:3128'},
{'ip_port': '188.165.194.110:8888'},
{'ip_port': '222.124.146.81:3128'},
{'ip_port': '31.135.64.76:3128'},
{'ip_port': '78.142.142.102:8080'},
{'ip_port': '185.42.223.194:3128'},
{'ip_port': '47.52.5.8:3128'},
{'ip_port': '213.235.171.118:53281'},
{'ip_port': '164.52.9.242:808'},
{'ip_port': '89.236.17.106:3128'},
{'ip_port': '14.207.133.97:8080'},
{'ip_port': '117.54.223.34:8080'},
{'ip_port': '35.198.2.63:8080'},
{'ip_port': '89.238.65.9:3128'},
{'ip_port': '203.142.85.132:3128'},
{'ip_port': '173.212.245.54:3128'},
{'ip_port': '164.52.9.242:808'},
{'ip_port': '163.172.217.103:3128'},
{'ip_port': '79.137.86.157:3128'},
{'ip_port': '216.100.88.229:8080'},
{'ip_port': '138.197.171.153:8080'},
{'ip_port': '101.108.208.75:8888'},
{'ip_port': '202.53.174.162:8080'},
{'ip_port': '137.74.163.137:3128'},
{'ip_port': '50.201.51.216:8080'},
{'ip_port': '89.238.65.9:3128'},
{'ip_port': '123.30.236.222:6969'},
{'ip_port': '190.186.58.144:53281'},
{'ip_port': '149.56.226.31:80'},
{'ip_port': '14.207.133.97:8080'},
{'ip_port': '185.42.223.194:3128'},
{'ip_port': '47.52.5.8:3128'},
{'ip_port': '202.190.165.68:8080'},
{'ip_port': '111.68.99.51:8080'},
{'ip_port': '101.37.79.125:3128'},
{'ip_port': '190.93.179.6:8080'},
{'ip_port': '69.27.184.131:53281'},
{'ip_port': '177.8.169.254:3128'},
{'ip_port': '187.95.11.239:3128'},
{'ip_port': '138.197.12.6:3128'},
{'ip_port': '50.59.162.78:8088'},
{'ip_port': '182.16.178.194:8080'},
{'ip_port': '47.254.17.64:3128'},
{'ip_port': '40.71.93.5:3128'},
{'ip_port': '118.97.205.138:8080'},
{'ip_port': '101.37.79.125:3128'},
{'ip_port': '87.229.76.9:53281'},
{'ip_port': '138.197.171.153:8080'},
{'ip_port': '202.138.248.105:8080'},
{'ip_port': '96.9.69.167:53281'},
{'ip_port': '200.138.196.34:8088'},
{'ip_port': '36.81.95.41:3128'},
{'ip_port': '117.52.91.121:80'},
{'ip_port': '186.225.39.251:8080'},
{'ip_port': '177.8.169.254:3128'},
{'ip_port': '36.69.84.219:8080'},
{'ip_port': '88.99.149.188:31288'},
{'ip_port': '202.53.174.162:8080'},
{'ip_port': '61.97.130.196:52335'},
{'ip_port': '90.150.87.130:3128'},
{'ip_port': '118.69.140.108:53281'},
{'ip_port': '180.234.207.225:8080'},
{'ip_port': '202.138.226.157:8080'},
{'ip_port': '203.207.57.222:8080'},
{'ip_port': '180.252.122.117:8080'},
{'ip_port': '213.154.3.102:3128'},
{'ip_port': '194.106.219.34:3128'},
{'ip_port': '186.227.8.21:3128'},
{'ip_port': '47.91.240.96:3128'},
{'ip_port': '138.197.171.153:8080'},
{'ip_port': '35.198.2.63:8080'},
{'ip_port': '1.179.189.217:8080'},
{'ip_port': '112.216.16.250:3128'},
{'ip_port': '121.172.54.218:3128'},
{'ip_port': '36.67.45.95:80'},
{'ip_port': '90.150.87.130:3128'},
{'ip_port': '202.152.58.146:8080'},
{'ip_port': '113.160.55.242:52335'},
{'ip_port': '163.172.93.129:3128'},
{'ip_port': '36.66.56.130:65301'},
{'ip_port': '200.55.219.178:52335'},
{'ip_port': '51.15.41.168:3128'},
{'ip_port': '50.59.162.78:8088'},
{'ip_port': '173.212.245.54:3128'},
{'ip_port': '202.62.12.174:53281'},
{'ip_port': '47.91.240.96:3128'},
{'ip_port': '35.198.2.63:8080'},
{'ip_port': '177.125.144.186:8080'},
{'ip_port': '1.179.189.217:8080'},
{'ip_port': '118.97.205.138:8080'},
{'ip_port': '121.172.54.218:3128'},
{'ip_port': '195.182.193.198:52335'},
{'ip_port': '202.152.58.146:8080'},
{'ip_port': '113.160.55.242:52335'},
{'ip_port': '138.197.12.6:3128'},
{'ip_port': '163.172.93.129:3128'},
{'ip_port': '200.55.219.178:52335'},
{'ip_port': '51.15.41.168:3128'},
{'ip_port': '50.59.162.78:8088'},
{'ip_port': '61.6.147.126:53281'},
{'ip_port': '173.212.245.54:3128'},
{'ip_port': '202.62.12.174:53281'},
{'ip_port': '121.172.54.218:3128'},
{'ip_port': '111.68.99.51:8080'},
{'ip_port': '90.150.87.130:3128'},
{'ip_port': '95.161.228.186:8080'},
{'ip_port': '117.52.74.172:80'},
{'ip_port': '186.225.39.251:8080'},
{'ip_port': '180.234.223.93:8080'},
{'ip_port': '202.190.165.68:8080'},
{'ip_port': '186.0.195.195:3128'},
{'ip_port': '180.183.237.105:9999'},
{'ip_port': '173.212.246.178:3128'},
{'ip_port': '188.165.194.110:8888'},
{'ip_port': '195.154.163.181:3128'},
{'ip_port': '121.58.205.116:3128'},
{'ip_port': '190.248.136.229:53281'},
{'ip_port': '113.160.55.242:52335'},
{'ip_port': '109.203.124.226:80'},
{'ip_port': '139.59.2.223:8888'},


    
]

#Mysql数据库的配置信息
MYSQL_HOST = '2400:dd01:1034:1c00:569f:35ff:fe22:1bd8'
MYSQL_DBNAME = 'arxiv_article'         #数据库名字，请修改
MYSQL_USER = 'root'             #数据库账号，请修改
MYSQL_PASSWD = 'xxxx'         #数据库密码，请修改

MYSQL_PORT = 3306               #数据库端口，在dbhelper中使用
