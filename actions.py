#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 18:34:54 2020

@author: nathaniellesage
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.
        
        `engine` is the scope this action is being performed in.
        
        `entity` is the object performing the action.
        
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class MovementAction(Action):
    def __init__(self, dm: int, dn: int):
        super().__init__()
        
        self.dm = dm
        self.dn = dn
    
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_m = entity.m + self.dm
        dest_n = entity.n + self.dn
        
        if not engine.game_map.in_bounds(dest_m, dest_n):
            if dest_m == -1:
                engine.game_map.transfer_region((-1,0))
            if dest_m == engine.game_map.height:
                engine.game_map.transfer_region((1,0))
            if dest_n == -1:
                engine.game_map.transfer_region((0,-1))
            if dest_n == engine.game_map.width:
                engine.game_map.transfer_region((0,1))
            
            entity.move(self.dm, self.dn)
            
            entity.m %= engine.game_map.current_region.height
            entity.n %= engine.game_map.current_region.width
            
            return # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_m][dest_n]:
            return # destination is blocked by a tile
        
        entity.move(self.dm, self.dn)

class ClimbAction(Action):
    def __init__(self, direction: int):
        super().__init__()
        
        self.direction = direction
    
    def perform(self, engine: Engine, entity: Entity) -> None:
        engine.game_map.climb(self.direction)
            