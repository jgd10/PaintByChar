# PaintByChar

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![PyPI version](https://img.shields.io/pypi/v/PaintByChar.svg)](https://pypi.org/project/PaintByChar/)
[![Tests](https://github.com/jgd10/PaintByChar/actions/workflows/python-tests.yml/badge.svg)](https://github.com/jgd10/PaintByChar/actions/workflows/python-tests.yml)

A tiny Python library for turning ASCII grids into colorful images. It is designed for quick visualizations of mazes, maps, game boards, and Advent of Code-style 2D text puzzles.

## Why PaintByChar?

- Turn a rectangular text grid into a rendered image in a few lines
- Map each character to a color automatically or via your own palette
- Support multiple rendering styles for cells, text, and background-label combinations
- Works well for generative art, puzzle visualizations, and debugging text-based layouts

## Features

- `string_to_image()` for direct text-to-image conversion
- `file_to_image()` for processing a text file as a grid
- Preset colormaps such as `viridis`, `plasma`, and `terrain`
- Custom `value_colors` dictionaries for full control over mapping
- Render modes: filled cells, colored text, and colored cells with background text

## Install

```bash
pip install paintbychar
```

## Quick example

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

## Example output

![](https://github.com/jgd10/PaintByChar/blob/main/output_basic.png)

## More examples

The repository includes several runnable examples in the [`examples/`](examples/) folder, including:

- `basic_example.py`
- `file_example.py`
- `styles_example.py`
- `preset_example.py`
- `advent_of_code_example.py`

## API reference

See the [documentation](docs/api.md) for a quick overview of the public functions and options.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions, testing guidance, and the pull request process.

## Code of conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Project status

PaintByChar is currently a small, focused library aimed at grid-based text rendering and visualization. It is suitable for personal, educational, and open-source use, and is prepared for broader community contributions as it matures.

## Social preview

A repository preview image is included in [`assets/social-preview.svg`](assets/social-preview.svg) and can be used as a GitHub social preview or banner asset.
