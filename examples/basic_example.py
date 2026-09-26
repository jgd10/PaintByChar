"""Simple example: convert a small string grid to an image and save it."""
from pathlib import Path
import paintbychar as pbc


def main():
    output_dir = Path(__file__).resolve().parent / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    grid = """0123
4567
89AB
"""
    img = pbc.string_to_image(grid, preset="viridis", cell_size=24,
                              render_style=pbc.RenderStyle.COLORED_CELLS)
    out = output_dir / "output_basic.png"
    pbc.save_image(img, out)


if __name__ == "__main__":
    main()
