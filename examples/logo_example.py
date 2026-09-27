"""Simple example: convert a small string grid to an image and save it."""
from pathlib import Path
import paintbychar as pbc
import matplotlib.pyplot as plt


def main():
    output_dir = Path(__file__).resolve().parent / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmap = plt.get_cmap("plasma")
    value_colors = {k: tuple([int(255 * c) for c in cmap(i / 10)[0:3]]) for
                    i, k in enumerate('PAINTBYCHR')}
    value_colors[' '] = (235, 240, 245)
    value_colors['*'] = (235, 240, 245)
    img = pbc.file_to_image("./logo.txt", cell_size=24, value_colors=value_colors,
                              render_style=pbc.RenderStyle.COLORED_CELLS)
    out = output_dir / "output_logo.png"
    pbc.save_image(img, out)


if __name__ == "__main__":
    main()
