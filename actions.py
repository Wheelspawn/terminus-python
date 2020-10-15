#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 18:34:54 2020

@author: nathaniellesage
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import engine
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
            return # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_n, dest_m]:
            return # destination is blocked by a tile
        
        entity.move(self.dm, self.dn)