#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:16:24 2020

@author: nathaniellesage
"""

import numpy as np
from typing import Iterator, Tuple

import tcod

from game_map import GameMap
import tile_types

from noise import snoise2
from pynoise.noisemodule import RidgedMulti
from scipy.ndimage.filters import gaussian_filter

class RectangularRoom:
    def __init__(self, m: int, n: int, height: int, width: int):
        self.m1 = m
        self.n1 = n
        self.m2 = m + height
        self.n2 = n + width
    
    @property
    def center(self) -> Tuple[int, int]:
        center_m = int((self.m1 + self.m2) / 2)
        center_n = int((self.n1 + self.n2) / 2)
        
        return center_m, center_n
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.m1 + 1, self.m2), slice(self.n1 + 1, self.n2)

def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    m1, n1 = start
    m2, n2 = end
    if np.random.random() < 0.5:
        # Move horizontally, then vertically.
        corner_m, corner_n = m2, n1
    else:
        # Move vertically, then horizontally.
        corner_m, corner_n = m1, n2
    
    # Generate the coordinates for this tunnel.
    for n, m in tcod.los.bresenham((n1, m1), (corner_n, corner_m)).tolist():
        yield n, m
    for n, m in tcod.los.bresenham((corner_n, corner_m), (n2, m2)).tolist():
        yield n, m
        
def generate_dungeon(map_width: int, map_height: int) -> GameMap:
    dungeon = GameMap(map_width, map_height)
    
    room_1 = RectangularRoom(m=20, n=15, height=10, width=15)
    room_2 = RectangularRoom(m=35, n=15, height=10, width=15)
    
    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor
    
    for m, n in tunnel_between(room_2.center, room_1.center):
        dungeon.tiles[n, m] = tile_types.floor
    
    return dungeon

def generate_multiridge_array(map_width: int, map_height: int, freq: float = 0.007, lacun: int = 2.5, sigma: float = 3.5, max_int: int = 896) -> np.ndarray:
    """Return array of Multiridge noise with values constrained from 0 to max_int.
       Frequency is like sigma, decreasing the size of biomes. Lacunarity affects snakiness of mountains, higher meaning snakier. Sigma parameter smooths terrain."""
    rm = RidgedMulti(frequency=freq,lacunarity=lacun)
    seed1 = np.random.randint(-(10**5),(10**5))
    seed2 = np.random.randint(-(10**5),(10**5))
    mridgemap = np.array([[rm.get_value(i+seed1,j+seed2,0.759823) for i in range(map_width)] for j in range(map_height)])
    mridgemap = gaussian_filter(mridgemap,sigma=sigma)
    mridgemap += abs(mridgemap.min())
    mridgemap /= mridgemap.max()
    mridgemap *= max_int
    mridgemap = mridgemap.astype('int32').astype(object)
    
    return mridgemap

def generate_perlin_noise_array(map_width: int, map_height: int, sigma: float = 3.5, max_int: int = 896) -> np.ndarray:
    """Return array of Perlin noise with values constrained from 0 to max_int.
       Sigma parameter smooths terrain."""
    seed1 = np.random.randint(-(10**5),(10**5))
    seed2 = np.random.randint(-(10**5),(10**5))
    perlinmap = np.array([[snoise2(i+seed1,j+seed2) for i in range(map_width)] for j in range(map_height)])
    perlinmap = gaussian_filter(perlinmap,sigma=sigma)
    perlinmap += abs(perlinmap.min())
    perlinmap /= perlinmap.max()
    perlinmap *= max_int
    perlinmap = perlinmap.astype('int32').astype(object)
    
    return perlinmap

def generate_overworld(map_width: int, map_height: int, sigma: float = 10, max_int: int = 896) -> GameMap:
    overworld = GameMap(map_width, map_height)
    elevation = generate_multiridge_array(map_width, map_height, sigma = 1.5, max_int = max_int)
    foilage = generate_perlin_noise_array(map_width, map_height,0.5,40)
    
    ocean_gradient = [tile_types.new_tile(walkable=False, transparent=True, dark=(ord(" "), (10, 95, 250,), (10, 95, 250))) for i in range(0,10)]
    
    ocean_gradient.extend([tile_types.new_tile(walkable=True, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient( (51,116,255), (131,242,246), 9 )])
    
    shore_gradient = [tile_types.new_tile(walkable=True, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient( (225,225,200), (205,205,180), 4 )]
    
    dirt_gradient = [tile_types.new_tile(walkable=True, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient( (175,180,154), (120,103,0), 10 )]
    
    dirt_gradient.extend([tile_types.new_tile(walkable=True, transparent=True, dark=(ord(" "), (120, 100, 0,), (120, 100, 0,))) for i in range(0,8)])
    
    mountain_gradient = [tile_types.new_tile(walkable=False, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient( (110,90,30), (125,115,60), 6)]
    
    ice_cap = [tile_types.new_tile(walkable=False, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient( (225,220,210), (235,230,220), 2 )]
    
    gradients = ocean_gradient + shore_gradient + dirt_gradient + mountain_gradient + ice_cap
    
    for m in range(map_height):
        for n in range(map_width):
            
            overworld.tiles[n][m] = gradients[int((elevation[m][n]/max_int)*(len(gradients)-1))]
            
            if overworld.tiles[n][m] in dirt_gradient:
                if foilage[m][n] < 20:
                    overworld.tiles[n][m]['dark'][1] = (0,200+np.random.choice([-20,-10,0,10,20]),0)
                    if 3 > foilage[m][n]:
                        overworld.tiles[n][m-1]['dark'][1] = (0,200+np.random.choice([-20,-10,0,10,20]),0)
                        overworld.tiles[n][m-1]['walkable'] = False
                        overworld.tiles[n][m-1]['dark'][0] = ord("▓")
                        overworld.tiles[n][m]['dark'][1] = (100,80,0)
                        overworld.tiles[n][m]['walkable'] = False
                        overworld.tiles[n][m]['dark'][0] = ord("|")
                    elif 2 <= foilage[m][n] < 15:
                        overworld.tiles[n][m]['dark'][0] = ord("v")
                    elif 15 <= foilage[m][n]:
                        overworld.tiles[n][m]['dark'][0] = ord("W")
            
            if overworld.tiles[n][m] in shore_gradient:
                if foilage[m][n] < 6:
                    overworld.tiles[n][m]['dark'][1] = (0,200+np.random.choice([-20,-10,0,10,20]),0)
                    overworld.tiles[n][m]['dark'][0] = ord("|")
            
            if overworld.tiles[n][m] in mountain_gradient:
                if foilage[m][n] < 4:
                    overworld.tiles[n][m]['dark'][1] = (100,80,0)
                    overworld.tiles[n][m]['dark'][0] = ord("|")
            
    return overworld

def rgb_gradient(rgb1: Tuple[float,float,float], rgb2: Tuple[float,float,float], step: float):
    l = []
    for i in range(step+1):
        l.append(( int(rgb1[0] + (rgb2[0]-rgb1[0])*i/step), int(rgb1[1] + (rgb2[1]-rgb1[1])*i/step), int(rgb1[2] + (rgb2[2]-rgb1[2])*i/step) ))
    
    return l






            