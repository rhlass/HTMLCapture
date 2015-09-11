#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年9月10日

@author: wangxianyun
'''
from config_default import configs
from LoginIn import Login
import logging,time,datetime,logging.handlers
from urllib2 import URLError, HTTPError
from linkHTMLParser import linkHTMLParser
from HTMLTabCrawer import html2csv

if __name__ == '__main__':
    
    #读取配置文件
    config_info = configs['info']
    logid = config_info['userid'] #用户名
    logpwd = config_info['password'] #密码
    tmodel = config_info['tmodel'] #模式:00/18
    today = datetime.datetime.now()
    sdate = (today - (datetime.timedelta(days=1))).strftime('%Y-%m-%d')
    #time.strftime('%Y-%m-%d',time.localtime())#开始日期 默认为当前日期前一天
    edate = today.strftime('%Y-%m-%d')#结束日期 默认为当前日期
    #print sdate,edate
    domain = config_info['domain']
    #设置日记记录
    log_file = './log/%s.log'%today.strftime('%Y-%m-%d')
    handler = logging.handlers.RotatingFileHandler(log_file,maxBytes=20*1024*1024,backupCount=10)
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)s]'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger = logging.getLogger('kybz')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    #logging.basicConfig(level=logging.DEBUG)
    #登录网站
    try:
        lg = Login()
        lg.setLoginInfo(logid, logpwd, domain)
        lg.login()
    except HTTPError,e:
        logger.info('httperror:登录失败，请检查配置文件!')
    except URLError,e:
        logger.info('urlerror:登录失败，请检查配置文件!')
    except StandardError,e:
        logger.exception(e)
    else:
        logger.info('登录成功')
    finally:
        logger.info('完成登录')
    #提取数据
    #先通过配置文件取得要查询的路局和发站
    config_data_lj = configs['data_lj']
    config_data_fz = configs['data_fz']
    #print config_data_lj['F']
    #print config_data_fz[1]
    #循环发站，取得车次
    for fz in config_data_fz:
        logger.debug(fz)
        #发送请求，取回所有车次
        params = {'type':'','ksrq':sdate,'jsrz':edate,'moshi':tmodel,'lz':config_data_lj,'start_stn':fz}
        logger.info(params)
        trainlistpage = lg.requestPage(domain+'/kybz/jsp/list_train_no.jsp', lg.headers,params)
        #解释返回的网页
        hp = linkHTMLParser()
        hp.feed(trainlistpage.read())
        hp.close()
        print hp.dictLinks
        #循环车次，取得编组数据
        for k,v in hp.dictLinks.iteritems():
            print k,v
            #取得车次编组信息
            params = {'cc':k,'mqfilename':v,'type':'33b'}
            logger.debug(params)
            traincomppage = lg.requestPage(domain+'/kybz/kybz.changeServlet', lg.headers,params)
            #处理编组信息并导出
            parse = html2csv()
            parse.feed(traincomppage.read())
            try:
                csvfile = open('./%s_%s'%(k,edate),'w+b')
            except StandardError,e:
                logger.exception(e.msg)
            else:
                csvfile.write(parse.getCSV())
                csvfile.write(parse.getCSV(True))
            finally:
                csvfile.close()
            
    #循环车次，取得编组
    print 'end'
    