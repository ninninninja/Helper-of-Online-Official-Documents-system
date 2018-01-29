# encoding: utf-8
import requests
from bs4 import BeautifulSoup


executiveUrl = 'http://docweb.sfaa.gov.tw/iftdc/DC11T01.php'
ajaxRPCURL = 'http://docweb.sfaa.gov.tw/iftdc/ajax/ajax_rpc_server.php'
#個人待處理
needExecuteURL = 'http://docweb.sfaa.gov.tw/iftdc/DC11T01.php?f_type=B&f_menuname=%E7%B0%BD%E6%A0%B8%E5%BE%85%E8%99%95%E7%90%86%E5%A4%BE'

cBrowser = requests.Session()
cBrowser.headers['Host'] = 'docweb.sfaa.gov.tw'
#firefox
cBrowser.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0'
#IE
#cBrowser.headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)'
#cBrowser.headers['Referer'] = 'http://docweb.sfaa.gov.tw/iftdc/DC11T01.php?f_type=B&f_menuname=%E7%B0%BD%E6%A0%B8%E5%BE%85%E8%99%95%E7%90%86%E5%A4%BE'
cBrowser.headers['Upgrade-Insecure-Requests'] = '1'
cBrowser.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

cBrowser.get('http://docweb.sfaa.gov.tw/')
payload = {'mode': 'IdLogin', 'f_id': '***', 'f_pw': '*******', 'f_vertify': 'undefined'}

reponseLogin = cBrowser.post('http://docweb.sfaa.gov.tw/ajax_server/ajax_out.server.php',data=payload)
testLogin = reponseLogin.json()
if testLogin[u'flag'] == True:
    print('login success\n')
else:
    print('login fail')

cBrowser.get('http://docweb.sfaa.gov.tw/menu.php')
cBrowser.get('http://docweb.sfaa.gov.tw/iftdc/default.php?f_id=d01&f_pw=d00001')



print('Send to Chief Secretary')
f = open('ToChiefSecretary.txt','r',encoding = 'utf8')
for line in f.readlines():
    documentNo = line.strip()

    #單位收文登錄作業
    cBrowser.get('http://docweb.sfaa.gov.tw/iftdc/DC01T01.php?&f_menuname=%E5%96%AE%E4%BD%8D%E6%94%B6%E6%96%87%E7%99%BB%E9%8C%84%E4%BD%9C%E6%A5%AD')

    cBrowser.get(needExecuteURL + '&q_inno=' + documentNo)
    rawHtml = cBrowser.get(needExecuteURL + '&q_inno=' + documentNo)
    
    rawHtml.encoding= 'utf8'
    textHtml = rawHtml.text
    soup = BeautifulSoup(textHtml, 'html.parser')



    searchTmp = textHtml.find('$("form:first").append("')
    searchStart = textHtml.find("'",searchTmp) + 1
    searchEnd = textHtml.find("'",searchStart + 1)
    fAuthName = textHtml[searchStart:searchEnd]

    searchStart = textHtml.find("'",searchEnd + 1) + 1
    searchEnd = textHtml.find("'",searchStart + 1)
    fAuthValue = textHtml[searchStart:searchEnd]


    searchTmp = textHtml.find('_csrf_protect_token')
    searchTmp = textHtml.find('value',searchTmp)
    searchStart = textHtml.find('"',searchTmp) + 1
    searchEnd = textHtml.find('"',searchStart)
    fCsrfValue = textHtml[searchStart:searchEnd]


   
    searchTmp = textHtml.find('name="f_radio')
    searchTmp = textHtml.find('value', searchTmp)
    searchStart = textHtml.find('"',searchTmp) + 1
    if searchStart == 0:
        print(documentNo + 'fail')
        continue
    searchEnd = textHtml.find('"',searchStart)
    f_radio = textHtml[searchStart:searchEnd]
    trseqno = f_radio.split('_',2)[1]


    payload = {
        'act': 'rpc_chk_dc11t01b_2',
        'inno': documentNo,
        'trseqno': trseqno,
        'trdpno': '04',
        'epname': '%E6%B4%AA%E4%B8%8A%E7%A5%90', 
        'tdno': 'F6',
        'qagent': '',
        'useapvsw': 'false',
        'modedata:': '"{"chk_sfidxdata":"Y","sfidx_fileyy":"","sfidx_fileno":"","sfidx_fcaseno":"","sfidx_pages":"","apvno":"","apvdate":"","isspup":""}"'
        }

    responseExecute1 = cBrowser.post(ajaxRPCURL,data=payload)



    payload = {
        'act': 'get_indcrel',
        'main_inno': documentNo,
        'main_trseqno': trseqno
        }


    responseExecute2 = cBrowser.post(ajaxRPCURL,data=payload)


    payload = {
        'act': 'is_ds',
        'main_inno': documentNo
        }

    responseExecute3 = cBrowser.post(ajaxRPCURL,data=payload)


    payload = {
        'act': 'rpc_dc11t01b_2',
        'inno': documentNo,
        'trseqno': trseqno,
        'trdpno': '04',
        'trdpname': '%E4%B8%BB%E4%BB%BB%E7%A7%98%E6%9B%B8%E5%AE%A4',
        'epname': '%E6%B4%AA%E4%B8%8A%E7%A5%90',
        'procdesc': '',
        'tdno': 'F6',
        'qagent': '',
        'reasontype': '2',
        'useapvsw': 'false',
        'moredata': '{"chk_sfidxdata":"Y","sfidx_fileyy":"","sfidx_fileno":"","sfidx_fcaseno":"","sfidx_pages":"","apvno":"","apvdate":"","isspup":""}'
        }


    responseExecute4 = cBrowser.post(ajaxRPCURL,data=payload)
    responseExecute4.encoding = 'utf8'
    
    executeResult = responseExecute4.text
    executeResult = executeResult.replace("true","True")
    executeResult = eval(executeResult)
    print(documentNo + "\t" + executeResult['msgtxt'])

f.close()
