'''
Created on 2015

@author: wangxianyun
'''
from HTMLParser import HTMLParser
import re,sys,time

class html2csv(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.CSV = ''
        self.CSVRow = ''
        self.inTR = 0
        self.inTD = 0
        self.rowCount = 0
        self.re_multiplespaces = re.compile('\s+')
        
        
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':self.start_tr()
        elif tag == 'td':self.start_td()
        
    def handle_endtag(self, tag):
        if tag == 'tr': self.end_tr()
        elif tag == 'td': self.end_td()
        
    def start_tr(self):
        #print 'tr start...'
        if self.inTR: self.end_tr()
        self.inTR = 1
        
    def end_tr(self):
        #print 'tr end..'
        if self.inTD:self.end_td()
        self.inTR = 0
        if len(self.CSVRow) > 0:
            self.CSV += self.CSVRow[:-1]
            self.CSVRow = ''
        self.CSV += '\n'
        self.rowCount += 1
        
    def start_td(self):
        #print 'td start...'
        if not self.inTR:self.start_tr()
        self.CSVRow += '"'
        self.inTD = 1
    
    def end_td(self):
        #print 'td end...'
        if self.inTD:
            self.CSVRow += '",'
            self.inTD = 0
            
    def handle_data(self, data):
        if self.inTD:
            self.CSVRow += self.re_multiplespaces.sub(' ',data.replace('\t','').replace('\n','').replace('\r','').replace('"','""'))
    
    def getCSV(self,purge=False):
        if purge and self.inTR:
            self.end_tr()
        dataout = self.CSV[:]
        self.CSV = ''
        return dataout
        

if __name__ == '__main__':
    parser = html2csv()
    try:
        htmlfile = open('./kybz.html')
        data = htmlfile.read()
        print htmlfile
        csvfile = open('./demo%s.csv'%(time.strftime('%Y-%m-%d',time.localtime())),'w+b')
        parser.feed(data)
        print parser.CSV
        csvfile.write(parser.getCSV())
        csvfile.write(parser.getCSV(True))
        csvfile.close()
        htmlfile.close()
        print 'convert success'
    except:
        print 'Error convert'
        