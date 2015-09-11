#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on

@author: wangxianyun
'''
from HTMLParser import HTMLParser
import re,sys
#import chardet

class LinkList(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.link = []
        self.name = []
        
    
class linkHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.datas = []
        self.dictLinks = {}
        self.dictLJ = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if len(attrs) == 0:pass
            else:
                for (variable,value) in attrs:
                    if variable == "href":
                        self.links.append(value)
        elif tag == 'option':
            if len(attrs) == 0:pass
            else:
                #print attrs
                for (variable,value) in attrs:
                    if variable == 'value':
                        self.dictLJ.append(value)
        #print self.dictLJ
        
        for link in self.links:
            
            data = re.match("^(java\w+):(\w+)\('(\w+)','(\w+.\w+)",link)
            #print link
            #print data.group(0)
            #print data.group(1),data.group(2),data.group(3),data.group(4)
            self.dictLinks[data.group(3)] = data.group(4)
            
    def handle_data(self, data):
        pass

if __name__ == '__main__':
    hp = linkHTMLParser()
    hp.feed(open('./list_train_no.html').read())
    hp.close()
    
    print hp.dictLinks
    
    topPage = open('./top.html').read().decode('utf16')
    sysEncode = sys.getfilesystemencoding()
    print topPage
    print sysEncode
    print type(topPage)
    
    #pattern = re.compile("\w#\w+[\u4e00-\u9fa5]+")
    pattern = re.compile(ur"(\w+#\w*[\u4e00-\u9fa5]+|$)")
    #m1 = re.match(ur"(\w+#\w*[\u4e00-\u9fa5]+|)",topPage)
    #m2 = re.match(ur"(\w+#\w*[\u4e00-\u9fa5]+|$)",topPage)
    result = pattern.findall(topPage)
    #print pattern
    print result
    #htmlEncode = chardet.detect(topPage).get('encoding','utf-8')
    #print htmlEncode
    #encodeTopPage = topPage.decode(htmlEncode,'ignore').encode(sysEncode)
    #print chardet.detect(encodeTopPage).get('encoding','utf-8')
    #hp.feed(encodeTopPage)
    #hp.close()
    #print hp.dictLJ
    #print encodeTopPage

    #encodeTopPage = encodeTopPage.decode(htmlEncode,'ignore').encode('utf-8')
    #print type(encodeTopPage)
    #re_array1 = re.compile(r'^(w+)(\.#\w+|)')
    
    #dictFZ = re.findall(ur'(\w#\w+|)',encodeTopPage)
    #dictFZ = re.findall(u'\w#\w3[\u4e00-\u9fa5]+|$',encodeTopPage)
    #encodeTopPage = encodeTopPage.decode(sysEncode,'ignore').encode('utf8')
    #pattern = re.compile("\w#\w+[\u4e00-\u9fa5]+")
    #pattern = re.match(ur"(\w+#\w+[\u4e00-\u9fa5]+|)+",encodeTopPage).group(0)
    
    #dictFZ = pattern.findall(encodeTopPage)
    #print pattern
    '''for fz in dictFZ:
        if len(fz) > 1:
            print fz'''
    #print dictFZ
    '''
    for line in encodeTopPage.readlines():
        print line
        print 'a new line'
        if re_array2.match(line):
            listFZ = line
        elif re_array1.match(line):
            listLJ = line
            '''
    #print topPage
    
    #print listLJ,listFZ
    