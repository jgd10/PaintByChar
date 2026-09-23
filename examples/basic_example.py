"""Simple example: convert a small string grid to an image and save it."""
from pathlib import Path
import paintbychar as pbc


def main():
    grid = """0123
4567
89AB
"""
    img = pbc.string_to_image(grid, preset="viridis", cell_size=24,
                              render_style=pbc.RenderStyle.COLORED_CELLS)
    out = Path(__file__).resolve().parent / "output_basic.png"
    pbc.save_image(img, out)


if __name__ == "__main__":
    main()
