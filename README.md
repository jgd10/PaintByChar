# PaintByChar

Python package providing simple functions that will take a rectangular grid of ASCII
characters and "paint" the cell/square containing said character 
a pre-assigned color, to form a final image.

This library was originally built to facilitate Advent of Code visualizations since many of the
problems presented there involve 2D ASCII grids, like the original inspiration from 2022 Day 12.

There are three methods of painting the cell.

1. Fill the square cell with a single color depending on the character
2. Write the character in the cell in the color depending on the character with a uniform background color of your choice
3. Write the characters in all cells with a uniform background color whilst coloring the rest of the cell with a single color depending on the character.
   
## Install

PaintByChar can be pip installed from PyPI.

```
C:\> pip install paintbychar
```

<!-- BEGIN EXAMPLES -->
## Examples

```python
import paintbychar as pbc

grid = """0123
4567
89AB
"""
img = pbc.string_to_image(grid, preset="viridis", cell_size=24,  render_style=pbc.RenderStyle.COLORED_CELLS)
out = "output_basic.png"
pbc.save_image(img, out)
```

### Example Output

![](https://github.com/jgd10/PaintByChar/blob/main/output_basic.png)