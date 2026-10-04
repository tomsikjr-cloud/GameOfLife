# Conway's Game of Life

An interactive browser simulation of Conway's Game of Life. Draw a starting pattern, generate a random board, or explore a glider, blinker, or pulsar.

**The primary version is now [`index.html`](index.html) at the repository root.** The original Python/Tkinter application is preserved unchanged in [`archive/python-v1/`](archive/python-v1/), together with its original documentation. This follows the root HTML / archived Python layout of SpaceDefense.

## Run locally

Download or clone this repository and open `index.html` in a modern browser. No build step, Python installation, package installation, or internet connection is required. HTML, CSS, JavaScript, and Canvas graphics are contained in that file, with no external assets or requests.

Optionally, serve the repository folder if you have Python 3 installed:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Then open <http://localhost:8000/>. On systems where Python is named `python3`, use that command instead.

## GitHub Pages / static hosting

In this repository's **Settings → Pages**, select **Deploy from a branch**, choose **main** and **/(root)**, then save. After a successful deployment, the default project URL is <https://tomsikjr-cloud.github.io/GameOfLife/>. Adding the HTML file alone does not enable Pages; use the deployment status in Settings to confirm publication.

See [GitHub's publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). The `.nojekyll` file bypasses Jekyll processing. For another static host, upload `index.html` as the site's entry point; no server-side runtime is needed.

## Controls

The board starts empty. Draw a pattern, select **Random**, or choose a sample pattern, then press **Start**.

| Control | Action |
| --- | --- |
| Click / tap | Toggle a cell while paused. |
| Drag | Paint live cells while paused. |
| Keyboard on the focused grid | Arrow keys move the highlighted cell; Space or Enter toggles it while paused. |
| Start / Stop | Run or pause playback. |
| Forward | Advance one generation while paused. |
| Back | Restore the previous generation once, including after pausing playback. |
| Clear | Empty the board and reset the generation count. |
| Random | Reset with approximately 28% living cells. |
| Try a pattern | Replace the board with a centered glider, blinker, or pulsar; reset the generation count. |
| Speed slider / − / + | Set the target speed from 1 to 25 generations per second, including during playback. |

Editing clears the saved Back step without resetting the generation count. Back is a single-step undo, not a full history. Editing, Back, Forward, Clear, Random, and patterns are disabled during playback. Playback stops when no living cells remain; still lifes and repeating patterns continue until stopped. Browser scheduling can reduce the actual speed, especially in background tabs. Refreshing the page starts a new empty board.

## Rules and defaults

Each cell has eight neighbors, including diagonals. All cells update simultaneously:

- A living cell survives with two or three living neighbors.
- A dead cell becomes alive with exactly three living neighbors.
- All other cells are dead in the next generation.

The 60 × 40 grid wraps at every edge, matching the Python version. The initial speed is 8 generations per second. The browser version adds touch input, keyboard grid editing, sample patterns, and a live population count.

## Repository layout

```text
index.html                       Primary browser application
.nojekyll                        Static GitHub Pages marker
tests/life.test.cjs               Rule and playback regression tests
archive/python-v1/GameOfLife.py   Original Python/Tkinter application
archive/python-v1/README.md       Original Python documentation
```

The constants, `nextGeneration` function, patterns, drawing code, and controls are in `index.html`. Developers with Node.js installed can run `node --test tests/life.test.cjs`; Node.js is not needed to play.

## Archived Python version

The Python source and original README are preserved byte-for-byte. To run the desktop version, use Python 3.6 or newer with Tkinter and a graphical desktop session:

```sh
cd archive/python-v1
python GameOfLife.py
```

See the [archived README](archive/python-v1/README.md) for its requirements and controls; its paths are relative to the archive folder. Existing Git history, including the original source at commit `f711dd5b4e91a818b7dc239bbe32463dafca0068`, is retained.
