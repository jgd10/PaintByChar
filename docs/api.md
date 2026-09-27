# API reference

## Import

```python
import paintbychar as pbc
```

## Core functions

### `string_to_image(grid_str, value_colors=None, preset=None, background_color=(255, 255, 255), cell_size=32, render_style=RenderStyle.COLORED_CELLS, font_path=None, font_size=None)`

Convert a multiline string into an RGB image.

Parameters:
- `grid_str`: multiline string describing the character grid
- `value_colors`: optional mapping of character to RGB tuple
- `preset`: optional colormap preset name like `viridis`
- `background_color`: default background color for each cell
- `cell_size`: pixel size of each grid cell
- `render_style`: one of `RenderStyle.COLORED_CELLS`, `RenderStyle.COLORED_TEXT`, or `RenderStyle.COLORED_CELLS_WITH_BACKGROUND_TEXT`
- `font_path`: optional font file path
- `font_size`: font size override

### `file_to_image(file_path, value_colors=None, preset=None, background_color=(255, 255, 255), cell_size=32, render_style=RenderStyle.COLORED_CELLS, font_path=None, font_size=None)`

Read a text file containing a grid and render it as an image.

### `save_image(img, out_path)`

Save a Pillow image to disk.

### `resolve_color(value)`

Accepts either a color preset name or a 3-tuple of RGB values.

### `get_colormap_dict(colormap_name)`

Generate a dictionary of digit keys to RGB values from a Matplotlib colormap.

## Render styles

```python
from paintbychar import RenderStyle

RenderStyle.COLORED_CELLS
RenderStyle.COLORED_TEXT
RenderStyle.COLORED_CELLS_WITH_BACKGROUND_TEXT
```

## Presets

```python
import paintbychar as pbc

print(sorted(pbc.PRESETS.keys()))
```

## Version

```python
import paintbychar as pbc
print(pbc.__version__)
```
