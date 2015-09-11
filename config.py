#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年9月10日

@author: wangxianyun
'''
import config_default

class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict,self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def toDict(d):
    D = Dict()
    for k,v in d.iteritems():
        D[k] = toDict(v) if isinstance(v,dict) else v
    return D
    
configs = config_default.configs

configs = toDict(configs)

if __name__ == '__main__':
    config = configs.info
    print configs