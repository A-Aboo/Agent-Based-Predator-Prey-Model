#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Calipsomulator - a simple CA and Agent-based simulator
# 2026, nb@su
# 
# GUI: curseur, z, shift+z, d, shift+d, reset, shift-reset
#

import random
import numpy as np

try:
    from numba import njit
except ImportError:
    print ("[WARNING] Numba not available.")
    def njit(*args, **kwargs):
        def wrapper(f):
            return f
        return wrapper

import calipsolib
from calipsolib import Agent

# =-=-= simulation parameters

params = {
    "p_reproduction_p":0.01,
}

# =-=-= Defining cell types

EMPTY = 0
TREE = 1
FIRE = 2
PREY_TRAIL = 3
PREDATOR_TRAIL = 4

colors_ca = {
    EMPTY: (255, 255, 255),
    TREE:  (40, 200, 40),
    FIRE:  (255, 40, 40),
    PREY_TRAIL: (224, 224, 255),
    PREDATOR_TRAIL:  (255, 224, 224),
}

# =-=-= Defining agent types

PREY = 0
PREDATOR = 1

colors_agents = {
    PREY: (0, 0, 128),
    PREDATOR:  (128, 0, 0),
}

# =-=-= user-defined agents

class Predator(Agent):
    def __init__(self, x: float, y: float, params):
        super().__init__(x, y,"Predator",params)
        self.type = PREDATOR
        self.running = True
        self.vie = 1000
        self.params = params




    def move(self, grid, agents):
        delta_x, delta_y = random.choice(( (-1, -1), (-1, 0), (-1, 1), ( 0, -1), ( 0, 1), ( 1, -1), ( 1, 0), ( 1, 1) ))
        self.vie -= 10
        for agent in agents:
            if agent is not self and agent.type == PREY and agent.running == True and agent.x == self.x and agent.y == self.y :
                agent.running = False
                self.vie += 100
                agents.remove(agent)
                return 
        self.x = (self.x + delta_x) % self.dx
        self.y = (self.y + delta_y) % self.dy

        if self.vie <= 0:
            self.running = False
            return

        if random.random() < self.params["p_reproduction_p"]:
            agents.append(Predator(x=self.x,y=self.y,params=self.params))
        

class Prey(Agent):
    def __init__(self, x: float, y: float, params):
        super().__init__(x, y,"Prey",params)
        self.type = PREY
        self.running = True
        self.vie = 1000
        self.params = params
    def move(self, grid, agents):
        self.vie -= 10
        delta_x, delta_y = random.choice(( (-1, -1), (-1, 0), (-1, 1), ( 0, -1), ( 0, 1), ( 1, -1), ( 1, 0), ( 1, 1) ))
        self.x = (self.x + delta_x) % self.dx
        self.y = (self.y + delta_y) % self.dy
        if self.vie < 0:
            self.running = False
            return
        if random.random() < self.params["p_reproduction_p"]:
            agents.append(Prey(x=self.x,y=self.y,params=self.params))

def make_agents(params):
    dx = params["dx"]
    dy = params["dy"]
    return [
        Prey(x=random.randint(0,dx-1), y=random.randint(0,dy-1), params=params),
        Predator(x=random.randint(0,dx-1), y=random.randint(0,dy-1), params=params),
        Prey(x=random.randint(0,dx-1), y=random.randint(0,dy-1), params=params),
        Predator(x=random.randint(0,dx-1), y=random.randint(0,dy-1), params=params),
        Prey(x=random.randint(0,dx-1), y=random.randint(0,dy-1), params=params),
        Predator(x=random.randint(0,dx-1), y=random.randint(0,dy-1), params=params)
    ]

# =-=-= user-defined cellular automata

def init_simulation(params):
    dx = params["dx"]
    dy = params["dy"]

    grid = np.zeros((dx, dy), dtype=np.uint8)
    newgrid = np.empty((dx, dy), dtype=np.uint8)

    for x in range (dx):
        for y in range(dy):
            if random.random() < 0.5:
                grid[x,y] = TREE


    return grid, newgrid

@njit(cache=True)
def ca_step(grid, newgrid):
    dx, dy = grid.shape
    for x in range(dx):
        for y in range(dy):
            newgrid[x,y] = grid[x, y]

# =-=-= run

if __name__ == "__main__":
    calipsolib.run(
        params=params, # user-defined
        init_simulation=init_simulation, # user-defined
        ca_step=ca_step, # user-defined
        make_agents=make_agents, # user-defined
        colors_ca=colors_ca,
        colors_agents=colors_agents,
        dx=8, # CA width
        dy=8, # CA height
        display_dx=800,
        display_dy=800,
        title="Predator-Prey (template)", 
        verbose=False, # display stuff (can be used by user)
        fps=2 # steps per seconds (default: 60)
    )
