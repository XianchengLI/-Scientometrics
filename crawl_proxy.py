#coding:utf-8
from lxml import html
import urllib
import requests

#of = open('proxy.txt' , 'w')
https = True

url = 'http://www.freeproxylists.net/zh/?pr=HTTPS&a[]=1&a[]=2&u=60&s=rs&page=1'
test_url = 'https://academic.microsoft.com/'

headers = {
	'Cookie': 'hl=zh; pv=12; userno=20170909-014778; from=direct; visited=2017%2F09%2F28+17%3A18%3A09; __utmt=1; __utma=251962462.1123204536.1504962629.1505025462.1506586691.4; __utmb=251962462.1.10.1506586691; __utmc=251962462; __utmz=251962462.1504962629.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=251962462.United%20States; __atuvc=5%7C36%2C6%7C37%2C0%7C38%2C1%7C39; __atuvs=59ccb0420654ac03000',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
}

def test_proxy(proxy, protocol):
	p = {}
	if protocol == 'HTTPS':
		p = {
			"https": 'http://' + proxy
		}
	else:
		p = {
			"http": 'http://' + proxy
		}
	try:
		r = requests.get(test_url, proxies=p, timeout=3)
	
	except:
		return False

	if r.status_code == 200:
		return True
	return False

page = requests.get(url, headers = headers)
tree = html.fromstring(page.text)
proxies = tree.xpath('//table[@class="DataGrid"]/tr[@class="Odd"]|//table[@class="DataGrid"]/tr[@class="Even"]')
for proxy in proxies:
	protocol = proxy.xpath('.//td[3]/text()')
	if len(protocol) == 0:
		continue
	protocol = protocol[0]
	if https and protocol != 'HTTPS':
		continue
	ip = proxy.xpath('.//td[1]/script/text()')
	tree = html.fromstring(urllib.unquote(urllib.unquote(ip[0][10:-2])))
	ip = tree.xpath('//a/text()')[0]
	port = proxy.xpath('.//td[2]/text()')[0]
	p = ip + ':' + port
	if test_proxy(p, protocol):
		print '{\'ip_port\': \'' + p + '\'},'



