import http
import http.client
import urllib
import urllib.parse
import re
import httpx
import ptvsd

def getHanziZigen( strHanzi ):
    if type(strHanzi) != type(""):        
        return None
    if ord(strHanzi) < 0x4e00 or ord(strHanzi) > 0x9FA5:
        return None
    try:
        params = urllib.parse.urlencode({'hzname' : strHanzi.encode('utf-8')})
        headers = {'content-type':'application/x-www-form-urlencoded','accept':'text/html', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
        #httpClient = http.client.HTTPSConnection('52wubi.com', 443)
        httpClient = httpx.Client(http2=True)        
        #httpClient.request("POST", '/wbbmcx/search.php', params, headers)
        r = httpClient.post('https://www.52wubi.com/wbbmcx/search.php', params = params, headers=headers)
        print(type(r))
        #response = httpClient.getresponse()
        if r.status_code == 200:#response.status == 200:            
            #resHtml = response.read().decode('gbk')
            resHtml = r.text
            pttnHanzi = r'<td><a href="\w+.html" title="[\u4e00-\u9fa5]+">([\u4e00-\u9fa5])+</a></td>'
            pttnZigen = r'<td class="wbbm">(\w+)</td>'
            pttnZigenImgUrl = r'<td><img src="(\w+/[\d\w]+.gif)" alt="[\u4e00-\u9fa5]+"'
            lstHanzi = re.findall(pttnHanzi, resHtml)
            #print(strHanzi)
            lstZigen = re.findall(pttnZigen, resHtml)
            #print(strZigen)
            lstZigenImgUrl = re.findall(pttnZigenImgUrl, resHtml)
            #print(strZigenImgUrl)
        else:
            return [None, None]
    except Exception as e:
        print(e)
        return None
    else:
        if len(lstZigen) != 0:
            if len(lstZigenImgUrl) != 0:                
                return [lstZigen[0], lstZigenImgUrl[0]]
            else:
                return [lstZigen[0], None]
        else:
            return [None, None]
        #return strHanzi + strZigen + strZigenImgUrl

def getZigenGif(strGifUrl):
    if type(strGifUrl) != type(""):
        return None
    if strGifUrl == "":
        return None
    
    try:
        headers = {'Accept-Encoding':'gzip, deflate, br','accept':'image/avif,image/webp,*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
        #httpClient = http.client.HTTPSConnection('52wubi.com', 443)        
        url = 'https://www.52wubi.com/wbbmcx/' + urllib.parse.quote(strGifUrl)
        #httpClient.request("GET", url, "", headers)
        response = httpx.get(url, headers = headers)
        #response = httpClient.getresponse()
        if response.status_code == 200:
            binGif = response.read()
        else:
            return None
    except Exception as e:
        print(e)
        return None
    else:
        return binGif