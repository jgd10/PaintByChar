# Examples

These example scripts live in the repository under the [`examples/` directory](https://github.com/jgd10/PaintByChar/tree/main/examples).

## Basic example

```python
import paintbychar as pbc

grid = """0123
4567
89AB
"""

img = pbc.string_to_image(
    grid,
    preset="viridis",
    cell_size=24,
    render_style=pbc.RenderStyle.COLORED_CELLS,
)

pbc.save_image(img, "output_basic.png")
```

![Basic example output](assets/output_basic.png)

See the full script in [examples/basic_example.py](https://github.com/jgd10/PaintByChar/blob/main/examples/basic_example.py).

## Reading from a file

```python
from pathlib import Path
import paintbychar as pbc

path = Path("sample_grid.txt")
path.write_text("A B C\nD E F\nG H I\n")

img = pbc.file_to_image(
    path,
    value_colors={c: (100, 150, 200) for c in "ABCDEF"},
    cell_size=30,
    render_style=pbc.RenderStyle.COLORED_TEXT,
)

pbc.save_image(img, "output_from_file.png")
```

See [examples/file_example.py](https://github.com/jgd10/PaintByChar/blob/main/examples/file_example.py).

## Render styles

```python
import paintbychar as pbc

grid = """A1
2B
"""

img = pbc.string_to_image(
    grid,
    value_colors={"A": (255, 0, 0), "1": (0, 255, 0), "2": (0, 0, 255), "B": (255, 200, 0)},
    cell_size=40,
    render_style=pbc.RenderStyle.COLORED_TEXT,
)

pbc.save_image(img, "style_colored_text.png")
```

![Render style output](assets/style_colored_text.png)

See [examples/styles_example.py](https://github.com/jgd10/PaintByChar/blob/main/examples/styles_example.py).

## Preset based mapping

```python
import paintbychar as pbc

grid = "0123456789"
img = pbc.string_to_image(
    grid,
    preset="plasma",
    cell_size=32,
    render_style=pbc.RenderStyle.COLORED_CELLS,
)
pbc.save_image(img, "output_preset_plasma.png")
```

![Preset example output](assets/output_preset_plasma.png)

See [examples/preset_example.py](https://github.com/jgd10/PaintByChar/blob/main/examples/preset_example.py).
