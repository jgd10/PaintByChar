from enum import Enum
from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


class FillOption(Enum):
    """Enumeration for fill options in the image generation."""
    CHARS = 1
    BACKGROUND = 2
    BOTH = 3


def get_colormap_dict(colormap_name: str) -> dict[str, tuple[int, ...]]:
    """Generate a color mapping dictionary from a matplotlib colormap.

    Uses the characters '0'-'9' as keys and maps them to colors sampled from the
    specified colormap. Supported colormaps include 'viridis', 'plasma',
    'inferno', 'magma', 'cividis', 'terrain', and 'coolwarm'.

    Args:
        colormap_name (str): Name of the matplotlib colormap to use.
    Returns:
        dict[str, tuple[int, ...]]: A dictionary mapping string digits '0'-'9' to RGB color tuples.
    """
    cmap = plt.get_cmap(colormap_name)
    colors = [tuple(int(255 * c) for c in cmap(i / 9)[:3]) for i in range(10)]
    return {str(i): colors[i] for i in range(10)}


PRESETS = {'viridis': get_colormap_dict('viridis'),
           'plasma': get_colormap_dict('plasma'),
           'inferno': get_colormap_dict('inferno'),
           'magma': get_colormap_dict('magma'),
           'cividis': get_colormap_dict('cividis'),  #
           'terrain': get_colormap_dict('terrain'),
           'coolwarm': get_colormap_dict(
               'coolwarm')}  # type: dict[str, dict[str, tuple[int, ...]]]


class InputError(Exception):
    """Custom exception for invalid input data."""
    pass


def check_grid_string(grid_str: str) -> bool:
    """Check if all lines in the string block have the same length.

    Input can only be a rectangular grid of single characters

    Args:
        grid_str (str): The string block representing the grid.
    Raises:
        InputError: If the lines have inconsistent lengths.
    Returns:
        bool: True if all lines have the same length.
    """
    lines = grid_str.strip().split('\n')
    width = len(lines[0])
    if width == 0:
        raise InputError("The string block must not be empty.")
    for line in lines:
        if len(line) != width:
            raise InputError("All lines in the string block must have the "
                             "same length.")
    return True


def file_to_image(file_path: Path | str,
                  char_color_map: Optional[dict[str, tuple[int, ...]]] = None,
                  preset: Optional[str] = None,
                  bg_color: tuple[int, int, int] = (255, 255, 255),
                  cell_size: int = 32,
                  fill_option: FillOption = FillOption.CHARS,
                  font_path: Path = None,
                  font_size: Optional[int] = None) -> Image:
    """Read a string block from a file and convert it to an image.

    Args:
        file_path (Path | str): Path to the file containing the string block.
        char_color_map (Optional[dict[str, tuple[int, ...]]]): Mapping of characters to RGB colors.
        preset (Optional[str]): Name of a preset colormap to use.
        bg_color (tuple[int, int, int]): Background color as an RGB tuple.
        cell_size (int): Size of each cell in pixels.
        fill_option (FillOption): Option for filling characters and/or background.
        font_path (Path): Path to the font file to use for rendering text.
        font_size (Optional[int]): Size of the font to use for rendering text.
    Returns:
        Image: The generated image.
    """
    grid_str = Path(file_path).read_text()
    check_grid_string(grid_str)
    img = string_to_image(grid_str, char_color_map, preset, bg_color, cell_size,
                          fill_option, font_path, font_size)
    return img


def string_to_image(grid_str: str,
                    char_color_map: Optional[dict[str, tuple[int, ...]]] = None,
                    preset: Optional[str] = None,
                    bg_color: tuple[int, int, int] = (255, 255, 255),
                    cell_size: int = 32,
                    fill_option: FillOption = FillOption.CHARS,
                    font_path: Path = None,
                    font_size: Optional[int] = None) -> Image:
    """Convert a string block to an image.

    Args:
        grid_str (str): The string block representing the grid.
        char_color_map (Optional[dict[str, tuple[int, ...]]]): Mapping of characters to RGB colors.
        preset (Optional[str]): Name of a preset colormap to use.
        bg_color (tuple[int, int, int]): Background color as an RGB tuple.
        cell_size (int): Size of each cell in pixels.
        fill_option (FillOption): Option for filling characters and/or background.
        font_path (Path): Path to the font file to use for rendering text.
        font_size (Optional[int]): Size of the font to use for rendering text.
    Returns:
        Image: The generated image.
    """
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
            match fill_option:
                case FillOption.BACKGROUND:
                    color = char_color_map.get(char, (0, 0, 0))
                    draw.rectangle(xy, fill=color)
                    bbox = draw.textbbox((0, 0), char, font=font)
                    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    tx = x * cell_size + (cell_size - w) // 2
                    ty = y * cell_size + (cell_size - h) // 2
                    draw.text((tx, ty), char, fill=bg_color, font=font)
                case FillOption.BOTH:
                    color = char_color_map.get(char, (0, 0, 0))
                    draw.rectangle(xy, fill=color)
                case FillOption.CHARS:
                    color = char_color_map.get(char, (0, 0, 0))
                    bbox = draw.textbbox((0, 0), char, font=font)
                    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    tx = x * cell_size + (cell_size - w) // 2
                    ty = y * cell_size + (cell_size - h) // 2
                    draw.text((tx, ty), char, fill=color, font=font)
                case _:
                    raise ValueError(
                        f"Invalid show_chars option: {fill_option}")
    return img


def get_set_mappings(cell_size: int,
                     char_color_map: Optional[dict[str, tuple[int, ...]]],
                     font_path: Optional[Path], font_size: int, preset: str)\
        -> \
tuple[
    dict[str, tuple[int, ...]], ImageFont.FreeTypeFont | ImageFont.ImageFont]:
    """Get character color mapping and font.

    Args:
        cell_size (int): Size of each cell in pixels.
        char_color_map (Optional[dict[str, tuple[int, ...]]]): Mapping of characters to RGB colors.
        font_path (Optional[Path]): Path to the font file to use for rendering text.
        font_size (int): Size of the font to use for rendering text.
        preset (str): Name of a preset colormap to use.
    Returns:
        tuple[dict[str, tuple[int, ...]], ImageFont.FreeTypeFont | ImageFont.ImageFont]:
        The character color mapping and the font object.
    """
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


def save_image(img: Image, out_path: Path | str) -> None:
    """Save the image to the specified path.

    Args:
        img (Image): The image to save.
        out_path (Path | str): The path to save the image to.
    Returns:
        None
    """
    img.save(out_path)
    print(f"Saved image to {out_path}")

