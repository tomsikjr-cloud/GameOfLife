# Conway's Game of Life

An interactive Python desktop simulation of Conway's Game of Life, built with Tkinter. Draw a starting pattern, generate a random board, or step through generations to explore how simple rules produce evolving patterns.

## Requirements

- Python 3.6 or newer (the script uses f-strings).
- Tkinter and a graphical desktop session.

The program uses only Python's standard library; no pip packages are required. To check that Tkinter is available, run:

```sh
python -m tkinter
```

This should open a small test window. If Tkinter is missing, install the Tcl/Tk support provided by your Python distribution or operating system.

## Run

Download or clone this repository, open a terminal in its directory, and run:

```sh
python GameOfLife.py
```

On Windows, you can also use `py GameOfLife.py`. On systems where Python 3 is named `python3`, use `python3 GameOfLife.py`.

## Controls

The board starts empty. Draw a pattern or select **Random**, then press **Start**.

| Control | Action |
| --- | --- |
| Left click | Toggle a cell between alive and dead while stopped. |
| Left click and drag | Paint live cells while stopped. |
| Start | Run the simulation continuously. |
| Stop | Pause the simulation. |
| Forward | Advance one generation while stopped. |
| Back | Undo the most recent manual Forward step, once. |
| Clear | Empty the board and reset the generation counter. |
| Random | Generate a new board with approximately 28% live cells and reset the generation counter. |
| Speed slider / < / > | Adjust the target speed from 1 to 25 generations per second, including while running. |

The generation counter tracks simulation steps. Clear and Random reset it to zero; drawing on the board does not. Clicking to edit the board clears the saved Back step. Back is a single-step undo, not a full history, and is disabled during automatic playback.

The simulation stops automatically when no live cells remain. Still lifes and repeating patterns continue running until you press Stop.

## Rules

Each cell has eight neighbors, including diagonals. At every generation, all cells update together:

- A live cell survives with two or three live neighbors.
- A dead cell becomes alive with exactly three live neighbors.
- All other cells are dead in the next generation.

The grid wraps at every edge: cells on opposite sides are neighbors.

Try placing three live cells in a horizontal row away from the edges, then press **Forward**. This pattern, called a blinker, alternates between horizontal and vertical rows.

## Defaults and customization

The constants at the top of [GameOfLife.py](GameOfLife.py) control the board size, colors, and speed limits:

| Setting | Default |
| --- | --- |
| Grid width | 60 cells |
| Grid height | 40 cells |
| Cell size | 12 pixels |
| Live cell color | Blue (`#1f77b4`) |
| Dead cell color | Light gray (`#f0f0f0`) |
| Initial speed | 8 generations per second |
| Speed range | 1–25 generations per second |

Actual animation speed depends on the time needed to calculate and draw each generation.

## Code layout

All application code lives in `GameOfLife.py`. The `GameOfLifeApp` class manages the grid, neighbor counting, generation updates, Tkinter interface, and animation loop. Running the script creates the application and opens its window.
