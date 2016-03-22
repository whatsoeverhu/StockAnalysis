import csv

 

with open('../jobs/stocks.csv',newline='') as csvfile:  # @UndefinedVariable

    reader = csv.reader(csvfile,delimiter=',',quotechar='|')

    for row in reader:
        print(row[0].replace(' ','')) 

csvfile.close()