"""Example taken from Advent of Code 2022, Day 12: Hill Climbing Algorithm.
Problems like this are the reason this library was created, 
to facilitate creation of simple visualizations from the 2D ASCII data common
to Advent of Code problems.

This example uses the sample input from the problem description, 
and visualizes the path found to the top through a Breadth-First-Search 
implementation."""

from pathlib import Path

import matplotlib.pyplot as plt
import paintbychar as pbc


TERRAIN = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

HEIGHT_MAP = {k: i + 1 for i, k in enumerate('abcdefghijklmnopqrstuvwxyz')}
HEIGHT_MAP = {**HEIGHT_MAP, 'E': 27, 'S': 0}


def draw_path_on_terrain(terrain: str,
                         path: list[tuple[int, int, int]]) -> str:
    terrain_lines = terrain.splitlines()
    terrain_list = [list(line) for line in terrain_lines]
    for i, j, _ in path:
        if terrain_list[j][i] not in ['S', 'E']:
            terrain_list[j][i] = '*'
    return '\n'.join(''.join(line) for line in terrain_list)


def parse_terrain(terrain: str):
    cells = set()
    start = None
    for j, line in enumerate(terrain.splitlines()):
        for i, char in enumerate(line):
            cells.add((i, j, HEIGHT_MAP[char]))
            if char == 'S':
                start = (i, j, 0)
    if start is None:
        raise ValueError("No starting point 'S' found in terrain.")
    return cells, start


def fetch_neighbors(cell, cells):
    i, j, height = cell
    neighbors = []
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        ni, nj = i + di, j + dj
        if (ni, nj, height + 1) in cells:
            neighbors.append((ni, nj, height + 1))
        elif (ni, nj, height) in cells:
            neighbors.append((ni, nj, height))
        elif (ni, nj, height - 1) in cells:
            neighbors.append((ni, nj, height - 1))
    return neighbors


def breadth_first_search(cells: set[tuple[int, int, int]],
                         start: tuple[int, int, int]) -> dict[
    tuple[int, int, int], tuple[int, int, int]]:
    explored = {start}
    queue = [start]
    parents = {}
    while queue:
        v = queue.pop(0)
        if v[2] == 27:  # Max height - target position 'E'
            break
        neighbors = fetch_neighbors(v, cells)
        for neighbor in neighbors:
            if neighbor not in explored:
                explored.add(neighbor)
                queue.append(neighbor)
                parents[neighbor] = v
    return parents


def visualize_steps(path: list[tuple[int, int, int]]):
    output_dir = Path(__file__).resolve().parent / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    path_by_step = []
    cmap = plt.get_cmap("terrain")
    value_colors = {k: tuple([int(255 * c) for c in cmap(i / 28)[0:3]]) for
                    i, k in enumerate('abcdefghijklmnopqrstuvwxyz')}
    value_colors = {**value_colors, 'S': 'black', 'E': 'white', '*': 'red'}
    for i, cell in enumerate(path):
        path_by_step.append(cell)
        string = draw_path_on_terrain(TERRAIN, path_by_step)

        img = pbc.string_to_image(string, value_colors=value_colors,
                                  cell_size=24,
                                  render_style=pbc.RenderStyle.COLORED_CELLS)
        out = Path(__file__).resolve().parent / "generated"
        pbc.save_image(img, out / f"path_step_{i:03d}.png")


def create_gif():
    import imageio.v2 as imageio
    output_dir = Path(__file__).resolve().parent / "generated"
    images = []
    for i in range(len(list(output_dir.glob("path_step_*.png")))):
        filename = output_dir / f"path_step_{i:03d}.png"
        images.append(imageio.imread(filename))
    imageio.mimsave(output_dir / "path_animation.gif", images, duration=0.5)
    print('GIF saved to', output_dir / "path_animation.gif")


def find_path(parents: dict[tuple[int, int, int], tuple[int, int, int]],
              start: tuple[int, int, int], end: tuple[int, int, int]) -> list[
    tuple[int, int, int]]:
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parents[current]
    path.append(start)
    path.reverse()
    return path


def main():
    cells, start = parse_terrain(TERRAIN)
    parents = breadth_first_search(cells, start)
    end = [c for c in cells if c[2] == 27][
        0]  # Find the cell with height 27 (E)
    path = find_path(parents, start, end)
    visualize_steps(path)
    try:
        create_gif()
    except ImportError:
        print("imageio not installed, skipping GIF creation.")
    return len(path) - 1


if __name__ == "__main__":
    print(f'Steps required to reach summit = {main()}')
