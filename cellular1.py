import random
import tkinter as tk

CELL_SIZE = 12
GRID_WIDTH = 60
GRID_HEIGHT = 40
ALIVE_COLOR = "#1f77b4"
DEAD_COLOR = "#f0f0f0"
# Speed configuration (generations per second)
MIN_SPEED = 1
MAX_SPEED = 25
DEFAULT_SPEED = 8


class GameOfLifeApp:
    def __init__(self, width=GRID_WIDTH, height=GRID_HEIGHT, cell_size=CELL_SIZE):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.animation_running = False
        self.grid = self._make_grid()
        # speed controls (generations per second)
        self.speed = DEFAULT_SPEED
        self.update_delay = None

        self.root = tk.Tk()
        self.root.title("Conway's Game of Life")

        self.canvas = tk.Canvas(
            self.root,
            width=self.width * self.cell_size,
            height=self.height * self.cell_size,
            bg=DEAD_COLOR,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)

        # create canvas items for each cell (optimize redraw)
        self.cell_items = [[None] * self.width for _ in range(self.height)]

        controls = tk.Frame(self.root)
        controls.pack(pady=6)

        button_defs = [
            ("Start", self.start, tk.NORMAL),
            ("Stop", self.stop, tk.DISABLED),
            ("Back", self.step_back, tk.DISABLED),
            ("Forward", self.step_forward, tk.NORMAL),
            ("Clear", self.clear, tk.NORMAL),
            ("Random", self.randomize, tk.NORMAL),
        ]
        self.buttons = {}
        for label, cmd, state in button_defs:
            btn = tk.Button(controls, text=label, command=cmd, state=state)
            btn.pack(side=tk.LEFT, padx=4)
            self.buttons[label] = btn

        # Speed controls: slower, slider, faster
        speed_frame = tk.Frame(self.root)
        speed_frame.pack(pady=4)

        self.slower_btn = tk.Button(speed_frame, text="<", width=3, command=lambda: self._change_speed(-1))
        self.slower_btn.pack(side=tk.LEFT, padx=(4, 2))

        self.speed_scale = tk.Scale(
            speed_frame,
            from_=MIN_SPEED,
            to=MAX_SPEED,
            orient=tk.HORIZONTAL,
            showvalue=False,
            command=self._on_speed_change,
            length=140,
        )
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(side=tk.LEFT)

        self.faster_btn = tk.Button(speed_frame, text=">", width=3, command=lambda: self._change_speed(1))
        self.faster_btn.pack(side=tk.LEFT, padx=(2, 4))

        self.speed_label = tk.Label(self.root, text=f"Speed: {self.speed} gen/s", font=("Arial", 10))
        self.speed_label.pack()

        self.instructions = tk.Label(
            self.root,
            text="Draw the starting pattern with the mouse, then press Start.",
            font=("Arial", 10),
            pady=4,
        )
        self.instructions.pack()

        self.generation = 0
        self.previous_grid = None
        self.generation_label = tk.Label(
            self.root,
            text=f"Generation: {self.generation}",
            font=("Arial", 10),
            pady=2,
        )
        self.generation_label.pack()

        # initialize drawing items and compute initial delay
        self._create_cell_items()
        self._on_speed_change(self.speed)
        self.draw_grid()

    def _make_grid(self, fill=0):
        return [[fill] * self.width for _ in range(self.height)]

    def _clone_grid(self):
        return [row[:] for row in self.grid]

    def _make_random_grid(self, alive_prob=0.28):
        return [
            [1 if random.random() < alive_prob else 0 for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def _count_live_neighbors(self, row, col):
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                count += self.grid[(row + dr) % self.height][(col + dc) % self.width]
        return count

    def _step_grid(self):
        new_grid = self._make_grid()
        for r in range(self.height):
            row = self.grid[r]
            next_row = new_grid[r]
            for c in range(self.width):
                neighbors = self._count_live_neighbors(r, c)
                if row[c] == 1:
                    next_row[c] = 1 if neighbors in (2, 3) else 0
                else:
                    next_row[c] = 1 if neighbors == 3 else 0
        self.grid = new_grid

    def draw_grid(self):
        # Update only changed cells when possible
        prev = self.previous_grid
        for r, row in enumerate(self.grid):
            for c, value in enumerate(row):
                if prev is not None and prev[r][c] == value:
                    continue
                rect_id = self.cell_items[r][c]
                color = ALIVE_COLOR if value else DEAD_COLOR
                self.canvas.itemconfig(rect_id, fill=color)

    def _on_canvas_click(self, event):
        if self.animation_running:
            return
        row, col = event.y // self.cell_size, event.x // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            self.previous_grid = None
            self.buttons["Back"].config(state=tk.DISABLED)
            self.grid[row][col] ^= 1
            self.draw_grid()

    def _on_canvas_drag(self, event):
        if self.animation_running:
            return
        row, col = event.y // self.cell_size, event.x // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = 1
            self.draw_grid()

    def _set_button_state(self, running):
        self.buttons["Start"].config(state=tk.DISABLED if running else tk.NORMAL)
        self.buttons["Stop"].config(state=tk.NORMAL if running else tk.DISABLED)
        self.buttons["Forward"].config(state=tk.DISABLED if running else tk.NORMAL)
        self.buttons["Clear"].config(state=tk.DISABLED if running else tk.NORMAL)
        self.buttons["Random"].config(state=tk.DISABLED if running else tk.NORMAL)

    def step_forward(self):
        if self.animation_running:
            return
        self.previous_grid = self._clone_grid()
        self._step_grid()
        self.generation += 1
        self._update_generation_label()
        self.buttons["Back"].config(state=tk.NORMAL)
        self.draw_grid()

    def step_back(self):
        if self.animation_running or not self.previous_grid:
            return
        self.grid = self.previous_grid
        self.previous_grid = None
        self.generation = max(0, self.generation - 1)
        self._update_generation_label()
        self.buttons["Back"].config(state=tk.DISABLED)
        self.draw_grid()

    def start(self):
        if self.animation_running:
            return
        self.animation_running = True
        self._set_button_state(True)
        self.buttons["Back"].config(state=tk.DISABLED)
        self._animate()

    def stop(self):
        if not self.animation_running:
            return
        self.animation_running = False
        self._set_button_state(False)

    def _reset_state(self, grid):
        if self.animation_running:
            return
        self.grid = grid
        self.previous_grid = None
        self.generation = 0
        self.buttons["Back"].config(state=tk.DISABLED)
        self._update_generation_label()
        self.draw_grid()

    def clear(self):
        self._reset_state(self._make_grid())

    def randomize(self):
        self._reset_state(self._make_random_grid())

    def _update_generation_label(self):
        self.generation_label.config(text=f"Generation: {self.generation}")

    def _count_live_cells(self):
        """Count the number of live cells in the grid."""
        return sum(sum(row) for row in self.grid)

    # consolidated speed change helper
    def _change_speed(self, delta):
        new = max(MIN_SPEED, min(MAX_SPEED, self.speed + delta))
        if new == self.speed:
            return
        self.speed = new
        self.speed_scale.set(self.speed)
        self._on_speed_change(self.speed)

    def _create_cell_items(self):
        for r in range(self.height):
            for c in range(self.width):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=DEAD_COLOR, outline="#d9d9d9"
                )
                self.cell_items[r][c] = rect

    def _on_speed_change(self, val):
        try:
            # Scale may pass float-like strings; accept them but keep integer speed
            self.speed = int(float(val))
        except Exception:
            return
        # Compute integer milliseconds per generation from speed (gen/s)
        # Ensure at least 1 ms delay to satisfy tkinter.after
        self.update_delay = max(1, int(1000 / float(self.speed)))
        self.speed_label.config(text=f"Speed: {self.speed} gen/s")

    # removed separate increase/decrease methods in favor of _change_speed

    def _animate(self):
        if not self.animation_running:
            return
        self.previous_grid = self._clone_grid()
        self._step_grid()
        self.generation += 1
        self._update_generation_label()
        self.draw_grid()
        
        # Stop if all cells are dead
        if self._count_live_cells() == 0:
            self.stop()
            return
        
        # schedule next frame using current delay
        self.root.after(self.update_delay, self._animate)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    GameOfLifeApp().run()
