import csv
 
csvfile = open('csv_test.csv', 'w',newline='')  # @UndefinedVariable

writer = csv.writer(csvfile,delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)

writer.writerow(['姓名', '年龄', '电话'])
  
data = [

     ('小河',25,2343454),

     ('小芳',18,235365)

] 

writer.writerows(data)
 

csvfile.close()