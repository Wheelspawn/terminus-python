#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 18:34:47 2020

@author: nathaniellesage
"""

from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction

class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
        
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        
        key = event.sym
        
        if key == tcod.event.K_UP:
            action = MovementAction(dm=-1, dn=0)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dm=1, dn=0)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dm=0, dn=-1)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dm=0, dn=1)
            
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()
            
        # no valid key was pressed
        return action

