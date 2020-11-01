#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:16:24 2020

@author: nathaniellesage
"""

import numpy as np
from typing import Iterator, Tuple

import tcod

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
        
'''
def generate_dungeon(map_width: int, map_height: int) -> GameMap:
    dungeon = GameMap(map_width, map_height)
    
    room_1 = RectangularRoom(m=20, n=15, height=10, width=15)
    room_2 = RectangularRoom(m=35, n=15, height=10, width=15)
    
    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor
    
    for m, n in tunnel_between(room_2.center, room_1.center):
        dungeon.tiles[n, m] = tile_types.floor
    
    return dungeon
'''

# rm = RidgedMulti(frequency=0.005,lacunarity=3.5,octaves=6,seed=np.random.seed)

def cutoff(x, min_val=-0.5, max_val=0.7):
    if x < min_val:
        return min_val
    if x > max_val:
        return max_val
    return x

def generate_multiridge_array(
        start_m: int,
        start_n: int,
        end_m: int,
        end_n: int,
        min_range: int = 0,
        max_range: int = 896,
        freq: float = 0.005,
        lacun: int = 3.5) -> np.ndarray:
    """Return array of Multiridge noise with values constrained from 0 to max_range.
       Frequency is like sigma, decreasing the size of biomes. Lacunarity affects snakiness of mountains, higher meaning snakier. Sigma parameter smooths terrain."""
    z = 0.759823
    rm = RidgedMulti(frequency=freq,lacunarity=lacun,octaves=6,seed=np.random.seed)
    mridgemap = np.array([[rm.get_value(n,m,z) for n in range(start_n,end_n)] for m in range(start_m,end_m)])
    print(np.round(mridgemap,3))
    print(np.round(mridgemap.min(),3),np.round(mridgemap.mean(),3),np.round(mridgemap.max(),3))
    print()
    vec = np.vectorize(cutoff)
    mridgemap=vec(mridgemap)
    mridgemap += 0.5
    mridgemap /= 1.2
    mridgemap *= max_range
    mridgemap = mridgemap.astype('int32').astype(object)
    '''
    mridgemap += abs(mridgemap.min())
    mridgemap /= mridgemap.max()
    mridgemap *= max_range
    mridgemap = mridgemap.astype('int32').astype(object)
    '''
    
    return mridgemap

def generate_perlin_noise_array(
        map_height: int,
        map_width: int,
        offset_m: int,
        offset_n: int,
        sigma: float = 3.5,
        max_range: int = 896) -> np.ndarray:
    """Return array of Perlin noise with values constrained from 0 to max_range.
       Sigma parameter smooths terrain."""
    perlinmap = np.array([[snoise2(n+offset_n*map_width+np.random.seed,m+offset_m*map_height+np.random.seed) for n in range(map_width)] for m in range(map_height)])
    perlinmap = gaussian_filter(perlinmap,sigma=sigma)
    perlinmap += abs(perlinmap.min())
    perlinmap /= perlinmap.max()
    perlinmap *= max_range
    perlinmap = perlinmap.astype('int32').astype(object)
    
    return perlinmap

def generate_overworld(
        map_height: int,
        map_width: int,
        offset_m: int,
        offset_n: int,
        foilage_blur: float = 0.5,
        foilage_range: float = 40,
        elevation_range: int = 896) -> np.ndarray:
    """Generates overworld.
       Returns overworld object."""
    
    import time
    t0 = time.time()
    
    m0 = map_height * offset_m
    n0 = map_width * offset_n
    m1 = map_height * offset_m + map_height
    n1 = map_width * offset_n + map_width
    
    overworld = np.full((map_height, map_width), fill_value=tile_types.wall, order="F")
    elevation = generate_multiridge_array(m0, n0, m1, n1, min_range = 0, max_range = elevation_range)
    foilage = generate_perlin_noise_array(map_height, map_width, offset_m, offset_n, foilage_blur, foilage_range)
    
    t1 = time.time()
    
    ocean_gradient = [tile_types.new_tile(walkable=True, transparent=True, dark=(ord(" "), (10, 95, 250,), (10, 95, 250))) for i in range(0,75)]
    coast_gradient = [tile_types.new_tile(walkable=True, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient( (20,105,250), (131,242,246), 30 )]
    shore_gradient = [tile_types.new_tile(walkable=True, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient( (225,225,200), (205,205,180), 6 )]
    lowgrass_gradient = [tile_types.new_tile(walkable=True, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient( (190,190,154), (110,120,0), 6 )]
    highgrass_gradient = [tile_types.new_tile(walkable=True, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient((110, 120, 0,), (110, 100, 0,), 12)]
    mountain_gradient = [tile_types.new_tile(walkable=False, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient( (110,90,30), (125,115,60), 8)]
    ice_cap_gradient = [tile_types.new_tile(walkable=False, transparent=True, dark=(ord(" "), g, g)) for g in rgb_gradient( (225,220,210), (235,230,220), 2 )]
    
    gradients = ocean_gradient + coast_gradient + shore_gradient + lowgrass_gradient + highgrass_gradient + mountain_gradient + ice_cap_gradient
    
    t2 = time.time()
    
    for m in range(map_height):
        for n in range(map_width):
            
            overworld[m][n] = gradients[int((elevation[m][n]/elevation_range)*(len(gradients)-1))]
            
            if (overworld[m][n] in lowgrass_gradient) or (overworld[m][n] in highgrass_gradient):
                if foilage[m][n] < 20:
                    overworld[m][n]['dark'][1] = (0,200+np.random.choice([-20,-10,0,10,20]),0)
                    if 3 > foilage[m][n]:
                        overworld[m-1][n]['dark'][1] = (0,200+np.random.choice([-20,-10,0,10,20]),0)
                        overworld[m-1][n]['walkable'] = False
                        overworld[m-1][n]['dark'][0] = ord("▓")
                        overworld[m][n]['dark'][1] = (100,80,0)
                        overworld[m][n]['walkable'] = False
                        overworld[m][n]['dark'][0] = ord("|")
                    elif 2 <= foilage[m][n] < 15:
                        overworld[m][n]['dark'][0] = ord("v")
                    elif 15 <= foilage[m][n]:
                        overworld[m][n]['dark'][0] = ord("W")
            
            if overworld[m][n] in shore_gradient:
                if foilage[m][n] < 6:
                    overworld[m][n]['dark'][1] = (0,200+np.random.choice([-20,-10,0,10,20]),0)
                    overworld[m][n]['dark'][0] = ord("|")
            
            if overworld[m][n] in mountain_gradient:
                if foilage[m][n] < 4:
                    overworld[m][n]['dark'][1] = (100,80,0)
                    overworld[m][n]['dark'][0] = ord("|")
    
    t3 = time.time()
    
    print(t1-t0)
    print(t3-t2)
    return overworld

def rgb_gradient(rgb1: Tuple[float,float,float], rgb2: Tuple[float,float,float], step: float):
    """
    Returns rgb gradient from rgb1 to rgb2, with step+1 specifying the number of values to return.
    
    Examples:
        >>> rgb_gradient((200,200,200),(215,215,215),3)
        >>> [(200, 200, 200), (205, 205, 205), (210, 210, 210), (215, 215, 215)]
        
        >>> rgb_gradient((200,200,200),(215,215,215),5)
        >>> [(200, 200, 200),
             (203, 203, 203),
             (206, 206, 206),
             (209, 209, 209),
             (212, 212, 212),
             (215, 215, 215)]
    """
    l = []
    for i in range(step+1):
        l.append(( int(rgb1[0] + (rgb2[0]-rgb1[0])*i/step), int(rgb1[1] + (rgb2[1]-rgb1[1])*i/step), int(rgb1[2] + (rgb2[2]-rgb1[2])*i/step) ))
    
    return l






            