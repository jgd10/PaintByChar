from enum import Enum
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


class FillOptions(Enum):
    CHARS = 1
    BACKGROUND = 2
    BOTH = 3


def get_colormap_dict(colormap_name: str) -> dict[str, tuple[int, ...]]:
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError(
            "matplotlib is required for colormap presets") from error
    cmap = plt.get_cmap(colormap_name)
    colors = [tuple(int(255 * c) for c in cmap(i / 9)[:3]) for i in range(10)]
    return {str(i): colors[i] for i in range(10)}


PRESETS = {'viridis': get_colormap_dict('viridis'),
           'plasma': get_colormap_dict(
               'plasma'), }  # type: dict[str, dict[str, tuple[int, ...]]]


def grid_to_image(grid_str: str,
                  char_color_map: Optional[dict[str, tuple[int, ...]]] = None,
                  preset: Optional[str] = None,
                  bg_color: tuple[int, int, int] = (255, 255, 255),
                  cell_size: int = 32, out_path: Path | str = 'grid.png',
                  show_chars: FillOptions = FillOptions.CHARS,
                  font_path: Path = None,
                  font_size: Optional[int] = None) -> None:
    lines = grid_str.strip().split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)

    char_color_map, font = get_set_mappings(cell_size, char_color_map,
                                            font_path, font_size, preset)

    img = Image.new('RGB', (width * cell_size, height * cell_size), bg_color)
    draw = ImageDraw.Draw(img)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            xy = [x * cell_size, y * cell_size, (x + 1) * cell_size,
                  (y + 1) * cell_size]
            draw.rectangle(xy, fill=bg_color)
            match show_chars:
                case FillOptions.BACKGROUND:
                    color = char_color_map.get(char, (0, 0, 0))
                    draw.rectangle(xy, fill=color)
                    bbox = draw.textbbox((0, 0), char, font=font)
                    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    tx = x * cell_size + (cell_size - w) // 2
                    ty = y * cell_size + (cell_size - h) // 2
                    draw.text((tx, ty), char, fill=bg_color, font=font)
                case FillOptions.BOTH:
                    color = char_color_map.get(char, (0, 0, 0))
                    draw.rectangle(xy, fill=color)
                case FillOptions.CHARS:
                    color = char_color_map.get(char, (0, 0, 0))
                    bbox = draw.textbbox((0, 0), char, font=font)
                    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    tx = x * cell_size + (cell_size - w) // 2
                    ty = y * cell_size + (cell_size - h) // 2
                    draw.text((tx, ty), char, fill=color, font=font)
                case _:
                    raise ValueError(
                        f"Invalid show_chars option: {show_chars}")

    img.save(out_path)
    print(f"Saved image to {out_path}")


def get_set_mappings(cell_size: int,
                     char_color_map: Optional[dict[str, tuple[int, ...]]],
                     font_path: Optional[Path], font_size: int, preset: str)\
        -> \
tuple[
    dict[str, tuple[int, ...]], ImageFont.FreeTypeFont | ImageFont.ImageFont]:
    if preset:
        char_color_map = PRESETS.get(preset, {})
    elif char_color_map is None:
        char_color_map = {}
    # Use bold Consolas if available, else fallback
    if font_path is None:
        font_path = "consolab.ttf"  # Bold Consolas
    if font_size is None:
        font_size = int(cell_size)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        font = ImageFont.load_default()
    return char_color_map, font


# Example usage:
if __name__ == "__main__":
    grid = Path('../tests/example4.txt').read_text()
    grid_to_image(grid, preset='viridis', bg_color=(240, 240, 240),
                  cell_size=40, out_path='viridis_grid_chars.png',
                  show_chars=FillOptions.BACKGROUND, font_size=32)
