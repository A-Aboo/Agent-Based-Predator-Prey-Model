# Agent-Based Predator-Prey Model

This repository contains a simple Python simulator for an **agent-based predator-prey model** using a cellular automata grid.

The simulator uses **Pygame** for visualization and **NumPy** for fast grid rendering.

## Description

The simulation follows this loop:

1. Agents move.
2. The cellular automata grid is updated.
3. The future grid becomes the current grid.
4. The simulation continues.
..

This structure can be used to model interactions between agents such as predators and prey inside a 2D environment.

## Requirements

Install the required Python libraries:

```bash
pip install pygame numpy
```

## Features

* 2D grid-based simulation
* Agent movement system
* Support for predator-prey style models
* Cellular automata update step
* Fast rendering with NumPy and Pygame
* Zoom and camera movement
* FPS and simulation speed display

## Controls

| Key                  | Action                           |
| -------------------- | -------------------------------- |
| `ESC`                | Quit simulation                  |
| `Z`                  | Zoom out                         |
| `Shift + Z`          | Zoom in                          |
| Arrow keys           | Move camera                      |
| `Shift + Arrow keys` | Move camera continuously         |
| `D`                  | Change rendering speed           |
| `Shift + D`          | Change rendering speed backwards |
| `R`                  | Reset zoom and camera            |
| `Shift + R`          | Restart simulation               |

## How to Use

To use the simulator, define:

1. An initialization function :

```python
def init_simulation(params):
    grid = ...
    newgrid = ...
    return grid, newgrid
```

2. A cellular automata step function:

```python
def ca_step(grid, newgrid):
    ...
```

3. Colors for the grid states:

```python
colors_ca = {
    0: (0, 0, 0),
    1: (255, 255, 255)
}
```

4. Optional agents:

```python
def make_agents(params):
    return []
```

Then launch the simulation:

```python
run(
    params={},
    init_simulation=init_simulation,
    ca_step=ca_step,
    colors_ca=colors_ca,
    colors_agents=None,
    dx=80,
    dy=80,
    display_dx=800,
    display_dy=800,
    title="Agent-Based Predator-Prey Model"
)
```

## Agent Class

The project includes a base `Agent` class.

You can create your own predator or prey agents by inheriting from this class and rewriting the `move()` method.

Example:

```python
class Prey(Agent):
    def move(self, grid, agents):
        self.x += 1
```

## Notes

* The grid should be a NumPy array.
* Grid states must match the keys used in `colors_ca`.
* Agent types must match the keys used in `colors_agents`.
* The simulation runs until the window is closed or `ESC` is pressed.

## License

This project is for learning and experimentation.
