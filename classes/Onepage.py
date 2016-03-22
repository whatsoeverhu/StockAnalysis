'''
Created on Jun 16, 2015

@author: HuJA
'''

class Onepage:
    pageCount = 0
    
    def __init__(self, tips, read,reply,first_date,last_date,read_list,reply_list,date_list,dictionary_read,dictionary_reply,dictionary_tips,date_list_unique):
        self.tips = tips
        self.read = read
        self.reply = reply
        self.first_date = first_date
        self.last_date = last_date
        self.read_list = read_list
        self.reply_list = reply_list
        self.date_list = date_list
        self.dictionary_read = dictionary_read
        self.dictionary_reply = dictionary_reply
        self.dictionary_tips = dictionary_tips        
        self.date_list_unique = date_list_unique
        Onepage.pageCount += 1
        
    def displayCount(self):
        print ("Total Stock Number %d" % Onepage.pageCount)

    def displayOnePage(self):
        print ("First date : ", str(self.first_date),"Last date : ", str(self.last_date))  # @UndefinedVariable
        print ("Read Dict:", self.dictionary_read)  # @UndefinedVariable
        print ("Reply Dict:", self.dictionary_reply)  # @UndefinedVariable
        print ("Tips Dict:", self.dictionary_tips)  # @UndefinedVariable
        print ("Unique Date:",self.date_list_unique)