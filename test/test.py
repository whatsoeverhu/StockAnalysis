import urllib.request

link = "http://www.abcfund.cn/data/realdata.php"
req = urllib.request.Request(link)    
response = urllib.request.urlopen(req)    
the_page = response.read()  
the_page = the_page.decode('GBK')
print(the_page)