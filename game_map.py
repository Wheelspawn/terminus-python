#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:02:48 2020

@author: nathaniellesage
"""

import numpy as np
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        
    def in_bounds(self, m: int, n: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= n < self.width and 0 <= m < self.height
    
    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
        # console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
        