from functions import stock_ana
from classes import stock_cls
import urllib
import csv
import sys
sys.setrecursionlimit(2000)  # @UndefinedVariable

stocks_dict= {}
in_stock = "601766"
in_date = "07-03"
year = "2015"
stock_increase = []

'''
read stocks CSV file to get all the stocks code and desc
'''
with open('../jobs/stocks.csv',newline='') as csvfile:  # @UndefinedVariable
    reader = csv.reader(csvfile,delimiter=',',quotechar='|')
    for row in reader:
        stocks_dict[row[0].replace(' ','')] = row[1].replace(' ','')
csvfile.close()

#print ("Got the stocks dictonary form CSV file:")
#print (stocks_dict)

'''
for all this stocks, get one month historical increase data
'''   
if in_stock in stocks_dict.keys():
    print ("Name:",stocks_dict[in_stock])
    try:        
        print ("Get increase data for stock :",in_stock )
        stock_increase = stock_ana.list_stock_increase(in_stock , in_date, year)
        if (len(stock_increase)<=0):            # @UndefinedVariable
            print ("not increase data found for this stock")
        else:    
            print ("increase data:",stock_increase) 
            date_list = []
            for item in stock_increase:
                item_list = item.split(",")
                stock_date = item_list[1]
                date_list.append(stock_date)
                date_list.sort()
                f_date = date_list[0]
                e_date = date_list[len(date_list)-1]  # @UndefinedVariable
            print ("date list:",date_list)
            print ("start to get tips data...")    
            tips_dict = stock_ana.get_info_oneperiod(in_stock,f_date,e_date) 
            print (tips_dict) 
            print ("Got tips data")
            print ("Show stock data by date:")
            csv_data = []
            for item in stock_increase:
                item_list = item.split(",")
                #print ("************************************")
                stock_code = item_list[0]
                stock_date = item_list[1]
                increase_p = item_list[2]
                increase_f = float(item_list[3])  # @UndefinedVariable
                if not stock_date in tips_dict.keys():
                    print("No tips get on date:",stock_date)
                    continue
                tips_list =  tips_dict[stock_date].split(",")
                reads = tips_list[0]
                tips = tips_list[1]
                replies = tips_list[2]
                stock = stock_cls.Stock(stock_code, stocks_dict[in_stock], stock_date, tips, reads, replies, increase_f)
                #stock.displayStock()
                data_str=stock_code+","+stocks_dict[in_stock]+","+stock_date+","+str(tips)+","+str(reads)+","+str(replies)+","+str(increase_f)  # @UndefinedVariable
                csv_data.append(data_str)  
            file_name = "../csv_files/"+in_stock+".csv"
            print ("start to write to csv file...")
            csvfile = open(file_name, 'w',newline='')  # @UndefinedVariable
            writer = csv.writer(csvfile,delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(csv_data)
            csvfile.close()   
            print ("data are stored in csv file:",file_name)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print ("Data not found for code : ",in_stock)
        else:
            raise
 
print ("Done!")
print ("Output:")
file_name = "../csv_files/"+in_stock+".csv"
try:
    with open(file_name,newline='') as csvfile:  # @UndefinedVariable

        reader = csv.reader(csvfile,delimiter=',',quotechar='|')
        data_list = []
        for row in reader:
            data_str = row[0].replace(' ','')+","+row[1].replace(' ','')+","+row[2].replace(' ','')+","+row[3].replace(' ','')+","+row[4].replace(' ','')+","+row[5].replace(' ','')+","+row[6].replace(' ','')     
            data_list.append(data_str)
        print (data_list)    
    csvfile.close()
except FileNotFoundError as e:  # @UndefinedVariable
    print (e)
