#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 13:07:43 2020

@author: nathaniellesage
"""

from typing import Tuple

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, m: int, n: int, char: str, color: Tuple[int,int,int]):
        self.m =  m
        self.n = n
        self.char = char
        self.color = color
        
    def move(self, dm: int, dn: int) -> None:
        self.m += dm
        self.n += dn