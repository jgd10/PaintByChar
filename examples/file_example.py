"""Read a grid from a file and generate an image."""
from pathlib import Path
import paintbychar as pbc


def main():
    examples_dir = Path(__file__).resolve().parent
    output_dir = examples_dir / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    grid_file = output_dir / "sample_grid.txt"
    # write a sample grid file
    grid_file.write_text("A B C\nD E F\nG H I\n")

    img = pbc.file_to_image(grid_file,
                            value_colors={c: (100 + i * 10, 150, 200)
                                          for i, c in
                                          enumerate("ABCDEF")},
                            cell_size=30,
                            render_style=pbc.RenderStyle.COLORED_TEXT,
                            background_color=(255, 255, 240))
    out = output_dir / "output_from_file.png"
    pbc.save_image(img, out)


if __name__ == "__main__":
    main()
