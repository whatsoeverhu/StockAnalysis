'''
Created on Jun 16, 2015

@author: HuJA
'''

class Stock:
    stockCount = 0
    def __init__(self, code,name,date,tips,read,reply,increase):
        self.code = code
        self.name = name
        self.date = date
        self.tips = tips
        self.read = read
        self.reply = reply
        self.increase = increase
        Stock.stockCount += 1
        
    def displayCount(self):
        print ("Total Stock Number %d" % Stock.stockCount)

    def displayStock(self):
        print ("Code : ", self.code,  ", Name: ", self.name)
        print ("Date:",self.date)
        print ("Tips:",self.tips)
        print ("Reads:",self.read)
        print ("Replies:",self.reply)
        print ("Increase:",'{percent:.2%}'.format(percent=self.increase))
