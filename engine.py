#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 13:17:51 2020

@author: nathaniellesage
"""

from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

class Engine:
    def __init__(self, entities: Set[Entity], game_map: GameMap, event_handler: EventHandler, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            
            if action is None:
                continue
            
            action.perform(self, self.player)
    
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        
        for entity in self.entities:
            console.print(entity.n, entity.m, entity.char, fg=entity.color)
            
        context.present(console)
        
        console.clear()