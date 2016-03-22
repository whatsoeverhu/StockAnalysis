import csv
from functions import stock_ana

data = []
stocks_dict = stock_ana.all_stocks() 
csvfile = open('stocks.csv', 'w',newline='')  # @UndefinedVariable
writer = csv.writer(csvfile,delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#writer.writerow(['股票代码', '股票名称'])
for key, value in stocks_dict.items():
    data_str=key+","+value
    data.append(data_str)  
print (data)
writer.writerows(data)
csvfile.close()
print("股票信息已经更新！")