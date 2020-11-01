#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 13:44:32 2020

@author: nathaniellesage
"""

from typing import Tuple

import numpy as np
from color import *

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
     ("ch", np.int32), # Unicode codepoint.
     ("fg", "3B"), # 3 unsigned bytes, for RGB colors.
     ("bg", "3B"),
    ])

tile_dt = np.dtype(
    [
     ("walkable", np.bool), # True if this tile can be walked over.
     ("transparent", np.bool), # True if this tile doesn't block FOV.
     ("dark", graphic_dt), # Graphics for when this tile is not in FOV.
    ])

def new_tile(
        *, # Enforce the use of keywords, so that parameter order doesn't matter.
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        ) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark), dtype=tile_dt)

floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255,), (50, 50, 150)))

wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100)))

grass = new_tile(
    walkable=True, transparent=True, dark=(ord("'"), green, green))

tree_leaves = new_tile(
    walkable=False, transparent=True, dark=(ord(" "), green, green))

tree_trunk = new_tile(
    walkable=False, transparent=True, dark=(ord(" "), brown, brown))

'''
class Tile:
    def __init__(self, graphic: graphic_dt, dark: graphic_dt, walkable: bool, blocked: bool, transparent: bool, vegetation: str = None):
        self.graphic = graphic
        self.dark = dark
        self.walkable = walkable
        self.blocked = blocked
        self.transparent = transparent
        self.vegetation = vegetation
        
def new_tile(
        *, # Enforce the use of keywords, so that parameter order doesn't matter.
        graphic: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        walkable: bool,
        blocked: bool,
        transparent: bool
        ) -> np.ndarray:
    return Tile(graphic,dark,walkable,blocked,transparent)
'''

