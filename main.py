# -*- coding: utf-8 -*-

import tcod
import random

from actions import EscapeAction, MovementAction
from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_overworld
from game_map import GameMap

import numpy as np

np.random.seed = np.random.randint(-10000,10000) # -122, 294, -335, 4578
# np.random.seed = 4578

l = [(random.randint(0,80),
      random.randint(0,50),
      (random.randint(50,100),
       random.randint(200,255),
       random.randint(50,100))) for i in range(750)]

def main():
    screen_height = 50
    screen_width = 80

    map_height = 50
    map_width = 50
    
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    event_handler = EventHandler()
    
    player = Entity(int(screen_height / 2), int(screen_width / 2), "@", (255,255,255))
    # npc = Entity(int(screen_height / 2), int(screen_width / 2 - 5), "M", (255,0,0))
    # npc2 = Entity(int(screen_height / 2 - 12), int(screen_width / 2 - 10), "M", (255,0,0))
    # npc3 = Entity(int(screen_height / 2), int(screen_width / 2 + 6), "M", (255,0,0))
    entities={player}
    
    game_map = GameMap(map_height,map_width)
    
    engine = Engine(entities=entities,
                    event_handler=event_handler,
                    game_map=game_map,
                    player=player)
    
    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Terminus ({})".format(np.random.seed),
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height)
        while True:
            engine.render(console=root_console,context=context)
            
            events = tcod.event.wait()
            
            engine.handle_events(events)

if __name__ == "__main__":
    main()

