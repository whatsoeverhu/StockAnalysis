'''
Created on Jun 16, 2015

@author: HuJA
'''

import urllib.request
from classes import Onepage
import csv
import io

'''
函数功能 :股票代码转股吧链接
输入:股票代码
输出:股吧 URL
备注:默认转换为该股票股吧按发帖日期排序的首页
'''
def stock_to_link(stock_code):
    base_link_beg = "http://guba.eastmoney.com/list,"
    base_link_end = ",f.html"
    link = base_link_beg+stock_code+base_link_end
    return link

'''
函数功能:股票代码 转股票历史数据获取的URL
输入:股票代码，日期，年份
输出:获取一个月股票历史数据的URL
'''    
def stock_to_url(stock_code,in_date,year):
    base_url = "http://table.finance.yahoo.com/table.csv?"
    month = int(in_date[0:2])  # @UndefinedVariable
    day = int(in_date[3:5])  # @UndefinedVariable
    last_day = 0
    from_month = 0
    from_year = int(year)  # @UndefinedVariable
    if month != 1:
        from_month = month - 1
    else:
        from_month = 12
        from_year = from_year - 1    
    if month == 3:
        last_day = 1
    else:
        last_day = day            
    if stock_code[0] == '0' or stock_code[0] == '2' or stock_code[0] == '3':
        append_str = ".sz"
    else:
        append_str = ".ss"
    c = str(from_year)  # @UndefinedVariable
    f = year
    b= last_day
    e = day
    a = from_month - 1 # @UndefinedVariable
    d = month - 1
    url = base_url + "a=" + str(a) +"&b=" + str(b) +"&c="+str(c)+"&d="+str(d)+"&e="+str(e)+"&f="+str(f)+"&s="+stock_code+append_str  # @UndefinedVariable
    return url    

'''
函数功能:获取给定日期的股票涨幅
输入:股票代码，日期，年份
输出:股票的涨幅
'''
def get_stock_increase(stock_code,in_date,year):
    url = stock_to_url(stock_code,in_date,year)
    webpage = urllib.request.urlopen(url)
    datareader = csv.reader(io.TextIOWrapper(webpage))
    data = list(datareader)  # @UndefinedVariable  
    if data[1][0][5:] != in_date:       
        return 99
    elif int(data[1][5]) == 0:  # @UndefinedVariable
        return 98
    else:  
        o_close_1 = data[1][4]
        o_close_2 = data[2][4]    
        increase = (float(o_close_1) - float(o_close_2))/float(o_close_2)  # @UndefinedVariable
        return increase
 
'''
 函数功能:获取一个月内每天的股票涨幅
 输入:股票代码，日期，年份
 输出:包含年一个月每天涨幅的数组
 '''
def list_stock_increase(stock_code,in_date,year):
    url = stock_to_url(stock_code,in_date,year)
    result = []
    webpage = urllib.request.urlopen(url)
    #print (url)
    if webpage.getcode() == 200:        
        datareader = csv.reader(io.TextIOWrapper(webpage))
        data = list(datareader)  # @UndefinedVariable  
        data.reverse()        
        for index,s in enumerate(data):  # @UndefinedVariable
            if index == 0 or index == 1 or index == len(data) - 1:  # @UndefinedVariable
                last_s = s
                continue
            else:
                if int(s[5]) != 0:  # @UndefinedVariable
                    o_close_1 = s[4]
                    o_close_2 = last_s[4]
                    #print (s)
                    #print (o_close_1)
                    #print (o_close_2)
                    increase = (float(o_close_1) - float(o_close_2))/float(o_close_2)  # @UndefinedVariable
                    increase_str = '{percent:.2%}'.format(percent=increase)
                    res_str = stock_code+","+data[index][0][5:]+","+increase_str+","+str(increase)   # @UndefinedVariable
                    result.append(res_str)  
                    last_s = s
    
    return result
 
'''
函数功能:翻页处理
输入:前一页的链接 
输出:后一页的链接
备注:中间特别处理了页数进位的问题
'''
def next_page(link):
    nPos_e = link.index(".html")    #页码结束位置
    nPos_b = link.index(",f") + 3   #页码开始位置
    page_str = link[nPos_b:nPos_e]  #获取页码     
    base_link = ""
    page = 0    
    if page_str.isdigit():  #判断是否为首页，首页没有页码，因而截取到的不是数字类型
        page = int(page_str)  # @UndefinedVariable 转换字符型为数字型
        page = page + 1 #页码+1
        base_link = link[:nPos_b]   #保存准备拼接的链接前段
    else:
        page = 2    #如果是首页，则直接拼接第2页作为下一页            
        base_link = link[:nPos_e]+"_"   #保存准备拼接的链接前段
    
    new_link = base_link+str(page)+".html"  # @UndefinedVariable这完成最终下一页的拼接
    return new_link

'''
函数功能:获得沪深两市的所有股票
输入：无
输出:所有股票的字典集
'''
def all_stocks():
    link = "http://quote.eastmoney.com/stocklist.html"
    req = urllib.request.Request(link)    
    response = urllib.request.urlopen(req)    
    the_page = response.read()  
    the_page = the_page.decode('GBK')
    sh_page = the_page[the_page.index('<div class=\"sltit\"><a name=\"sh\"/>上海股票</div>'):the_page.index('<div class=\"sltit\"><a name=\"sz\"/>深圳股票</div>')]
    sz_page = the_page[the_page.index('<div class=\"sltit\"><a name=\"sz\"/>深圳股票</div>'):the_page.index('<div class=\"shengming\">')]   
    split_page_sh = sh_page.split("<li><a target=\"_blank\" href=\"") 
    split_page_sz = sz_page.split("<li><a target=\"_blank\" href=\"") 
    code = ''
    desc = ''
    dictionary = {}
 
    for index,s in enumerate(split_page_sh):  # @UndefinedVariable
        if index == 0:
            continue
        else:
            code =s[s.index('</a></li>')-7:s.index('</a></li>')-1]
            desc = s[s.index('.html\">')+7:s.index('</a></li>')-8]
            if code[0] == '6':
                dictionary[code] = desc   
          
    for index,s in enumerate(split_page_sz):  # @UndefinedVariable
        if index == 0:
            continue
        else:
            code =s[s.index('</a></li>')-7:s.index('</a></li>')-1]
            desc = s[s.index('.html\">')+7:s.index('</a></li>')-8]
            if code[0] == '0' or code[0] == '2' or code[0] == '3':
                dictionary[code] = desc                     
    return dictionary
    
'''
函数功能:返回某一页的对象
输入:股吧链接
输出:包含帖子数，阅读数，回复数的页面对象
备注:对象属性有帖子数，阅读数，回复数，起始日期，每个帖子的阅读数，回复数和发帖日期的数组
'''
def get_info_onepage(link):
    req = urllib.request.Request(link)    
    response = urllib.request.urlopen(req)    
    the_page = response.read()    
    the_page = the_page.decode('utf-8')  
    split_page = the_page.split("<div class=\"articleh\">")  
    tips =  len(split_page)-2    # @UndefinedVariable
    date_list = []
    reply_list = []
    read_list = []
    ttl_reply = 0
    ttl_read = 0
    first_date = ""
    last_date = ""
    dictionary_read = {}
    dictionary_reply = {}
    dictionary_tips = {}
    first_flag = 1
    for index,s in enumerate(split_page):  # @UndefinedVariable
        if index == 0:
            continue 
        elif s.count("<em class=\"settop\">") > 0: 
            continue
        elif s.count("<em class=\"hinfo\">") > 0:
            continue
        else:            
            get_date = s[s.index('<span class=\"l6\">')+17:s.index('<span class=\"l6\">')+22]
            date_list.append(get_date)
            get_reply = int(s[s.index('<span class=\"l2\">')+17:s.index('</span><span class=\"l3\">')]) # @UndefinedVariable
            reply_list.append(get_reply)  
            get_read = int(s[s.index('<span class=\"l1\">')+17:s.index('</span><span class=\"l2\">')]) # @UndefinedVariable
            read_list.append(get_read)          
            ttl_reply = ttl_reply + get_reply
            ttl_read = ttl_read + get_read 
            if first_flag == 1: #当读取到第一条帖子时，初始化字典对象
                #print ("first tip")
                dictionary_read =  {get_date:get_read} # @UndefinedVariable
                dictionary_reply = {get_date:get_reply} # @UndefinedVariable
                dictionary_tips =   {get_date:1} # @UndefinedVariable  
                #print (dictionary_read) 
            else:
                if get_date in dictionary_tips:  #如果已经有对应日期的字典数据，则做累加
                    #print ("add numbers")     
                    #print (dictionary_read)        
                    dictionary_read[get_date] =  dictionary_read[get_date] + get_read # @UndefinedVariable
                    dictionary_reply[get_date] =  dictionary_reply[get_date] + get_reply # @UndefinedVariable
                    dictionary_tips[get_date] =  dictionary_tips[get_date] + 1 # @UndefinedVariable                  
                else:    #如无日期数据则加入字典
                    #print ("Get tip posted in new date")                      
                    dictionary_read[get_date] =   get_read # @UndefinedVariable
                    dictionary_reply[get_date] = get_reply # @UndefinedVariable
                    dictionary_tips[get_date] =   1 # @UndefinedVariable  
                    #print (dictionary_read)         
            date_list.sort(reverse = True)  # @UndefinedVariable
            last_date = date_list[len(date_list)-1]  # @UndefinedVariable
            first_date = date_list[0]
            first_flag = 0
    date_list_unique = sorted(dictionary_read,reverse = True)  # @UndefinedVariable #用一个数组记录下字典中涉及到 的日期
    onepage = Onepage.Onepage(tips,ttl_read,ttl_reply,first_date,last_date,read_list,reply_list,date_list,dictionary_read,dictionary_reply,dictionary_tips,date_list_unique)
    return onepage

'''
函数功能:递归函数，获取给定日期下的最终发帖数，阅读数及回复数
输入:特定日期,当页开始日期，当页结束日期，发帖日期数组，阅读数数组，回复数数组，链接，返回结果数组
输出:包含[发帖数，阅读数，回复数]的数组 
'''
def cut_by_date(in_date,first_date,last_date,date_list,read_list,reply_list,link,result):
    date_list.sort(reverse = True)  # @UndefinedVariable    
    n = len(date_list) - 1    # @UndefinedVariable
    print (link)
    print (result)
    if (in_date > last_date):
        temp_date = last_date
        while (in_date > temp_date):
            n = n - 1
            temp_date = date_list[n]
        n = n + 1
        ttl_n = result[0] + n  # @UndefinedVariable
        ttl_read = result[1] + sum(read_list[:n])  # @UndefinedVariable
        ttl_reply = result[2] + sum(reply_list[:n])  # @UndefinedVariable  
#        print (date_list[:n])  
        result = [ttl_n,ttl_read,ttl_reply]  
        print ("last record")
        print (result)
        return result    
    elif (in_date == last_date):
        new_link = next_page(link)
        onepage = get_info_onepage(new_link)
        onepage.date_list.sort(reverse = True)  # @UndefinedVariable
        temp_date = first_date  
        c = 0
        while (in_date < temp_date):
            c = c + 1
            temp_date = date_list[c]
           
        ttl_n = result[0] + len(date_list) - c    # @UndefinedVariable
        ttl_read = result[1] + sum(read_list[c:])  # @UndefinedVariable
        ttl_reply = result[2] + sum(reply_list[c:])  # @UndefinedVariable
        result = [ttl_n,ttl_read,ttl_reply]
        return cut_by_date(in_date,onepage.first_date,onepage.last_date,onepage.date_list,onepage.read_list,onepage.reply_list,new_link,result)        
    else:
        new_link = next_page(link)
        onepage = get_info_onepage(new_link)        
        return cut_by_date(in_date,onepage.first_date,onepage.last_date,onepage.date_list,onepage.read_list,onepage.reply_list,new_link,result)                  

'''
函数功能:递归函数，获取给定日期下的最终发帖数，阅读数及回复数
输入:特定日期,当页开始日期，当页结束日期，发帖日期数组，阅读数字典，回复数字典，帖子数字典，链接，返回结果数组
输出:包含[发帖数，阅读数，回复数]的数组 
'''
def get_info_oneday(in_date,first_date,last_date,date_list_unique,dictionary_read,dictionary_reply,dictionary_tips,link,result):
    #print (link)
    #print (result)
    date_list_unique.sort()
    if(not in_date in dictionary_read.keys() or in_date < last_date): #当某页帖子的最后创建日期大于比对日期时，直接翻页，进入下一页
        new_link = next_page(link)
        onepage = get_info_onepage(new_link)  
        return get_info_oneday(in_date,onepage.first_date,onepage.last_date,onepage.date_list_unique,onepage.dictionary_read,onepage.dictionary_reply,onepage.dictionary_tips,new_link,result)
    elif (date_list_unique[0] < in_date):#当某页的最后创建日期小于比对日期时，停子翻页
        ttl_read = result[1]+dictionary_read[in_date]
        ttl_reply = result[2] + dictionary_reply[in_date]
        ttl_tips = result[0]+dictionary_tips[in_date]        
        result = [ttl_tips,ttl_read,ttl_reply]  
        #print ("last record")
        #print (result)
        return result    
    else: #当某页帖子的最后创建小于等于比对日期时，如果当页只取到一个日期，记录下当页所有数据后翻页，如果有多个日期，但是最后创建日期等于
        new_link = next_page(link)
        onepage = get_info_onepage(new_link)         
        ttl_read = result[1]+dictionary_read[in_date]
        ttl_reply = result[2] + dictionary_reply[in_date]
        ttl_tips = result[0]+dictionary_tips[in_date]        
        result = [ttl_tips,ttl_read,ttl_reply]
        return get_info_oneday(in_date,onepage.first_date,onepage.last_date,onepage.date_list_unique,onepage.dictionary_read,onepage.dictionary_reply,onepage.dictionary_tips,new_link,result)   



'''
函数功能:获取一个时期每天的帖吧数据
输入:股票代码，开始日期，结束日期
输出:包含[日期，发帖数，阅读数，回复数]的字典
'''
def get_info_oneperiod(stock_code,f_date,e_date):
    link = stock_to_link(stock_code)
    onepage = get_info_onepage(link)
    re_dict = {}   
    while onepage.first_date >= f_date: #只有当某页的最早日期都小于开始日期时，才停止翻页
        #print (link)
        if onepage.last_date <= e_date:        #只要某页的最晚日期是小于等于结束日期的就需要进行计算           
            for key, value in onepage.dictionary_read.items():
                if key <= e_date and key >= f_date: #只记录日期在起止日期之间的数据
                    #print (onepage.dictionary_read.keys())
                    if (key in re_dict.keys()):
                        v_list = re_dict[key].split(",")
                        read = int(v_list[0])  # @UndefinedVariable
                        tips = int(v_list[1])  # @UndefinedVariable
                        reply = int(v_list[2])  # @UndefinedVariable
                        re_dict[key] = str(value+read)+","+str(onepage.dictionary_tips[key]+tips)+","+str(onepage.dictionary_reply[key]+reply)  # @UndefinedVariable
                    else:    
                        re_dict[key] = str(value)+","+str(onepage.dictionary_tips[key])+","+str(onepage.dictionary_reply[key])            # @UndefinedVariable
        new_link = next_page(link)
        link = new_link
        onepage = get_info_onepage(new_link) 
    return re_dict    


