#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 16:34:22 2020

@author: nathaniellesage
"""

from __future__ import annotations

import json

def init_class_from_params(faddr: str, param_class: object):
        f = open(faddr)
        js = json.load(f)
        f.close()
        return param_class(**js)

def save_class_params(faddr: str, param_class: object):
        f = open(faddr,"w")
        js = param_class.__dict__
        f.write(str(js))
        f.close()
        
class Loaded(object):
    def __init__(self, a: int, b: int, c:int):
        self.a = a
        self.b = b
        self.c = c

if __name__ == "__main__":
    pm = init_class_from_params("data//param_test",Loaded)
    print(pm.a)
    print(pm.b)
    print(pm.c)
    pm.b = -7000
    save_class_params("data//param_test_modified",pm)
    