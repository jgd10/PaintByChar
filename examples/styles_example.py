"""Demonstrate the three RenderStyle modes and save outputs."""
from pathlib import Path
import paintbychar as pbc


def main():
    grid = """A1
2B
"""
    outdir = Path(__file__).resolve().parent / "generated"
    outdir.mkdir(parents=True, exist_ok=True)

    # Colored cells (fills each cell with the mapped color)
    img1 = pbc.string_to_image(grid, value_colors={"A": (255, 0, 0), "1": (0, 255, 0),
                                                   "2": (0, 0, 255), "B": (255, 200, 0)},
                               cell_size=40, render_style=pbc.RenderStyle.COLORED_CELLS)
    pbc.save_image(img1, outdir / "style_colored_cells.png")

    # Colored text (background stays default, characters are colored)
    img2 = pbc.string_to_image(grid, value_colors={"A": (0, 0, 0), "1": (128, 0, 128),
                                                   "2": (0, 128, 128), "B": (128, 128, 0)},
                               cell_size=40, render_style=pbc.RenderStyle.COLORED_TEXT,
                               background_color=(240, 240, 255))
    pbc.save_image(img2, outdir / "style_colored_text.png")

    # Colored cells with background-text (cell colored, text drawn in background color)
    img3 = pbc.string_to_image(grid, value_colors={"A": (200, 50, 50), "1": (50, 200, 50),
                                                   "2": (50, 50, 200), "B": (200, 180, 50)},
                               cell_size=40, render_style=pbc.RenderStyle.COLORED_CELLS_WITH_BACKGROUND_TEXT,
                               background_color=(255, 255, 255))
    pbc.save_image(img3, outdir / "style_cells_with_bg_text.png")


if __name__ == "__main__":
    main()
