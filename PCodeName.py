import requests
from html.parser import HTMLParser
import codecs
import json

class MyHtmlParser(HTMLParser):
    def __init__(self):
        self.shouldParse = False
        self.code_name_dict = {}
        self.linklist = []
        self.ccode = ''
        self.chref = ''
        HTMLParser.__init__(self)   


    def handle_starttag(self, tag, attrs):
        if self.shouldParse == False:
            return
        for kv in attrs:
            if kv[0] == 'href':
                self.chref = kv[1]
        
    def handle_endtag(self, tag):
        if tag == 'table':
            self.shouldParse = False
        if self.shouldParse == False:
            return
        return

    def handle_data(self, data):
        if data == '名称':
            self.shouldParse = True
            return
        if self.shouldParse == False:
            return
        #print(type(data))
        data = data.strip()
        if len(data) == 0:
            return
        if data.isdigit():
            self.ccode = data
            self.linklist.append((self.chref, data))
        else:
            self.code_name_dict[self.ccode] = data
            
        #print(data)
        return


host = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/65/'
page = '6532.html'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
           'Referer':'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/65.html'}

code2name = {}

codeT = {}

def walk(code, page):
    res = requests.get(host+'/'+page, headers = headers)
    res.encoding = 'gb2312'
    parser = MyHtmlParser()
    parser.feed(res.text)
    #print('-'*10+'code: name'+'-'*10)
    #print(parser.code_name_dict)
    #print('-'*10+'links'+'-'*10)
    #print(parser.linklist)
    codelist = list(parser.code_name_dict.keys())
    if len(codelist) == 0:
        return
    codeT[code] = codelist
    for k in codelist:
        code2name[k] = parser.code_name_dict[k]
    for ll in parser.linklist:
        walk(ll[1], ll[0])
        
walk('653200000000', page)
#print(codeT)
#print(code2name)

fin = codecs.open('code.txt','w',encoding='utf-8')
fin.write(json.dumps(codeT, ensure_ascii=False))
fin.write(json.dumps(code2name, ensure_ascii=False));
fin.close()

