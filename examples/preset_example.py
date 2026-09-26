"""Show how to use presets and get_colormap_dict to build a mapping."""
from pathlib import Path
import paintbychar as pbc


def main():
    output_dir = Path(__file__).resolve().parent / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Print available presets
    print("Available presets:", sorted(pbc.PRESETS.keys()))

    # Use a preset to render digits 0-9 in a single-row image
    grid = "0123456789"
    img = pbc.string_to_image(grid, preset="plasma", cell_size=32,
                              render_style=pbc.RenderStyle.COLORED_CELLS)
    out = output_dir / "output_preset_plasma.png"
    pbc.save_image(img, out)

    # Demonstrate get_colormap_dict directly
    cmap = pbc.get_colormap_dict("viridis")
    print("viridis[5] =", cmap["5"])  # rgb tuple for digit '5'


if __name__ == "__main__":
    main()
