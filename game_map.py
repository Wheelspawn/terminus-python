#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:02:48 2020

@author: nathaniellesage
"""

from __future__ import annotations

import numpy as np
from tcod.console import Console

import tile_types

from typing import Tuple

from procgen import *

class GameMap:
    def __init__(self, region_height: int, region_width: int, regions: dict = {}, current_region: Region = None):
        self.height = region_height
        self.width = region_width
        self.regions = regions
        self.current_region = current_region
        
        if current_region == None:
            self.current_region = Region(self.height, self.width, 0, 0)
            self.current_region.generate()
    
    @property
    def entities(self):
        return self.current_region.entities[self.current_region.current_level]
        
    def in_bounds(self, m: int, n: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= n < self.current_region.width and 0 <= m < self.current_region.height
    
    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.current_region.height, 0:self.current_region.width] = self.tiles["dark"]

    @property
    def tiles(self):
        return self.current_region.levels[self.current_region.current_level]
    
    def transfer_region(self, direction: Tuple[int, int]):
        
        new_coords = (self.current_region.offset_m + direction[0], self.current_region.offset_n + direction[1])
        # print("Old: ",(self.current_region.offset_m,self.current_region.offset_n))
        # print("New: ", new_coords)
        # print()
        
        if new_coords in self.regions:
            self.current_region = self.regions[new_coords]
        else:
            new_region = Region(
                self.height,
                self.width,
                self.current_region.offset_m + direction[0],
                self.current_region.offset_n + direction[1])
            new_region.generate()
            self.regions[new_coords] = new_region
            
            self.current_region = new_region
        
    def climb(direction: int):
        if direction == 1:
            self.current_region.current_level = max(0, self.current_region.current_level+1)
        elif direction == -1:
            self.current_region.current_level = min(len(self.levels)-1, self.current_region.current_level+1)
        
class Region:
    def __init__(
            self,
            height: int,
            width: int,
            offset_m: int,
            offset_n: int,
            levels: list = [],
            entities: list = [[]],
            current_level: int = 0
            ):
        
        self.height = height
        self.width = width
        
        self.offset_m = offset_m
        self.offset_n = offset_n
        
        self.levels = levels
        self.entities = entities
        self.current_level = current_level
        
    def generate(self):
        overworld = generate_overworld(self.height,self.width,self.offset_m,self.offset_n)
        # cave_level_1 = generate_cave(self.map_height,self.map_width,self.offset_m,self.offset_n)
        self.levels = [overworld] # ,cave_level_1]
        self.current_level = 0
        # self.entities = [[]]
        # self.map_tiles = [np.full((width, height), fill_value=tile_types.wall, order="F")]
        self.bridge_overworld_and_caves()
    
    def bridge_overworld_and_caves(self):
        pass
        
        
        
    