#! /usr/bin/env python
#coding:utf-8
'''
Created on 2015��9��6��

@author: wangxy
'''

import sys
import re
import urllib
import urllib2
import cookielib
from wsgiref.headers import Headers
from HTMLParser import HTMLParser
import logging
from wsgiref import headers
from urllib2 import URLError
from HTMLTabCrawer import html2csv

reload(sys)
#sys.setdefaultencoding("utf-8")

#loginurl = 'http://172.16.205.1:9000/api/authenticate'
loginurl = 'http://10.1.3.54:7001/kybz/kybz.login.loginServlet'
logindomain = 'http://10.1.3.54:7001'

class Login(object):
    def __init__(self):
        self.name = ''
        self.password = ''
        self.domain = ''
        self.page = ''
        self.req = ''
        self.res = ''
        self.headers = ''
        
        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)
        
    def setLoginInfo(self,username,password,domain):
        self.name = username
        self.pwd = password
        self.domain = domain
        logging.info('set login info as domain:%s,username:%s,pass:=****'%(self.domain,self.name))
        
    def login(self):
        loginparams = {'uid':self.name,'password':self.pwd,'imageield.x':50,'imageField.y':21}
        #self.headers = {'Host':logindomain,'User-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        self.headers = {'Host':logindomain,'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        self.req = urllib2.Request(loginurl,urllib.urlencode(loginparams),headers=self.headers)
        
            
        self.res = urllib2.urlopen(self.req)
        self.operate = self.opener.open(self.req)
        #thePage = self.res.read()
        logging.info('login in success')
        logging.info(self.headers)
        logging.info(thePage)
        
        
        #print thePage
        #print self.cj
    def requestPage(self,postURL,headers,params=None):
        try:
            self.req = urllib2.Request(url=postURL,headers=headers,data=params)
            self.res = urllib2.urlopen(self.req)
            self.operate = self.opener.open(self.req)
            self.page = self.res.read()
            logging.info('get data from URL success')
            #print self.page
            return self.page
        except Exception,e:
            logging.exception('open request page error')
        
        
class linkHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.datas = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if len(attrs) == 0:pass
            else:
                for (variable,value) in attrs:
                    if variable == "href":
                        self.links.append(value)
     
    def handle_data(self, data):
        pass

if __name__ == '__main__':
    '''
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('crawlogger')
    logger.setLevel(logging.DEBUG)
    
    fh = logging.FileHandler('./craw.log')
    fh.setLevel(logging.DEBUG)
    
    logger.addHandler(fh)
    #logger.info('sdds')'''
    
    userlogin = Login()
    username = 'fddkybz'
    password = 'fddkybz'
    domain = logindomain
    userlogin.setLoginInfo(username, password, domain)
    userlogin.login()
    
    #links 
    print userlogin.page
    #all dict content 
    thePage = userlogin.requestPage(domain+'/kybz/jsp/top.jsp',userlogin.headers)
    #print thePage
    #hp = linkHTMLParser()
    #hp.feed(userlogin.page)
    #read html from file
    #hp.feed(open("d:\\hello.html").read())
    #hp.close()
    #print hp.links
    #train list
    #thePage = userlogin.requestPage(domain+'/kybz/jsp/list_train_no.jsp', userlogin.headers)
    
    #thePage = userlogin.requestPage(domain+'/kybz/kybz.changeServlet', userlogin.headers)
    #parser = html2csv()
    '''
    try:
        #htmlfile = open('./kybz.html')
        htmlfile = thePage
        data = htmlfile.read()
        print htmlfile
        csvfile = open('./trainlist%s.csv'%(time.strftime('%Y-%m-%d',time.localtime())),'w+b')
        parser.feed(data)
        print parser.CSV
        csvfile.write(parser.getCSV())
        csvfile.write(parser.getCSV(True))
        csvfile.close()
        htmlfile.close()
        print 'convert success'
    except:
        print 'Error convert'
    '''
    