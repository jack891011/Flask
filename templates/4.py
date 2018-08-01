#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi,datetime,time,re
t='2017-04-07T22:22'
t1=t.replace('T',' ')
tt=datetime.datetime.strptime(t1,"%Y-%m-%d %H:%M")
print(tt)
