# PaintByChar documentation

Welcome to the PaintByChar documentation.

This project turns text grids into small, colorful images using character-to-color mapping.

## Getting started

```python
import paintbychar as pbc

grid = """A B
C D
"""

img = pbc.string_to_image(
    grid,
    value_colors={"A": (255, 0, 0), "B": (0, 255, 0), "C": (0, 0, 255), "D": (255, 255, 0)},
    cell_size=30,
    render_style=pbc.RenderStyle.COLORED_CELLS,
)

pbc.save_image(img, "example.png")
```

## Documentation

- [API reference](api.md)
- [Examples directory](https://github.com/jgd10/PaintByChar/tree/main/examples)
- [Project README](https://github.com/jgd10/PaintByChar/blob/main/README.md)
