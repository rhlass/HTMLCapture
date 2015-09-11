'''
Created on 2015年9月10日

@author: wangxianyun
'''
import chardet

if __name__ == '__main__':
    topPage = open('./top.html').read()
    #htmlEncode = chardet.detect(topPage).get('encoding','utf-8')
    #print htmlEncode
    #encodeTopPage = topPage.decode(htmlEncode,'ignore').encode(sysEncode)
    #print chardet.detect(encodeTopPage).get('encoding','utf-8')