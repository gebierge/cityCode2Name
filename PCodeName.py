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

        data = data.strip()
        if len(data) == 0:
            return
        if data.isdigit():
            if len(data) < 5:
                return
            self.ccode = data
            if (len(self.chref)) > 0:
                self.linklist.append((self.chref, data))
                self.chref = ''
        else:
            self.code_name_dict[self.ccode] = data
            
        return

from urllib.parse import urljoin
# you can change these values according to your requrements
fcurl = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/65.html'
ftourl = '65/6532.html'
saveLog = True
code_blacklist = {'653201000000': True};
# ---------------------------------------------------------
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'}
code2name = {}
codeT = {}
logF = None
if saveLog:
    logF = codecs.open('log.txt', 'w', encoding = 'utf-8')
    
def walk(code, curl, tocurl):
    url = urljoin(curl, tocurl)
    headers['Referer'] = curl
    res = requests.get(url, headers = headers)
    res.encoding = 'gb2312'
    parser = MyHtmlParser()
    parser.feed(res.text)
    
    codelist = list(parser.code_name_dict.keys())
    # about log
    if saveLog:
        logF.write('walk params: [%s, %s, %s]\n'%(code ,curl, tocurl))
        logF.write('go: %s\n'%(url))
    # handle blacklist
    codelist = [elem for elem in codelist if elem not in code_blacklist]
    if len(codelist) == 0:
        return
    codeT[code] = codelist
    for k in codelist:
        code2name[k] = parser.code_name_dict[k]

    #about log
    if saveLog:
        logF.write('-'*10+'code: name'+'-'*10+'\n')
        logF.write(json.dumps(parser.code_name_dict, ensure_ascii=False)+'\n')
        logF.write('-'*10+'links'+'-'*10+'\n')
        logF.write(json.dumps(parser.linklist, ensure_ascii=False)+'\n')
        
    for ll in parser.linklist:
        # skip blacklist
        if ll[1] in code_blacklist:
            continue
        walk(ll[1],url, ll[0])
        
walk('653200000000', fcurl, ftourl)
#print(codeT)
#print(code2name)
if saveLog:
    logF.close()

fin = codecs.open('code.txt','w',encoding='utf-8')
fin.write(json.dumps(codeT, ensure_ascii=False))
fin.write(json.dumps(code2name, ensure_ascii=False));
fin.close()



