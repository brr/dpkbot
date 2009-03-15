# -*- coding: utf8 -*-
import sys
import codecs

def is_mat(s):
    Param=s.lower()
    mat_list=[tmp.strip() for tmp in codecs.open('mat_list','r', 'utf-8').readlines()]
    if Param in mat_list: return 1
    else: return 0

