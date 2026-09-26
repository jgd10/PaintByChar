from enum import Enum
from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Union

from PIL.ImageFont import FreeTypeFont


COLOR_PRESETS: dict[str, tuple[int, int, int]] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "light_gray": (245, 245, 245),
    "dark_gray": (50, 50, 50),
    "pastel_blue": (174, 198, 207),
    "pastel_green": (152, 251, 152),
    "pastel_pink": (255, 182, 193),
    "cream": (255, 253, 208),
    "beige": (245, 245, 220),
    "mint": (189, 252, 201),
    "navy": (10, 25, 47),
    "charcoal": (34, 40, 49),
    "soft_yellow": (255, 250, 205),
    "gray": (128, 128, 128),
    "blue": (70, 130, 180),
    "green": (60, 179, 113),
    "pink": (255, 182, 193),
    "yellow": (255, 223, 0),
    "teal": (0, 128, 128),
    "brown": (139, 69, 19),
    "red": (220, 20, 60),
}


def resolve_color(value: Union[str, Tuple[int, int, int]]) -> tuple[int, int, int]:
    """
    Resolve a color value which can be:
    - a preset name from BG_PRESETS (e.g., 'cream')
    - an RGB tuple already (e.g., (255, 255, 255))
    Returns an (R, G, B) tuple.
    """
    if isinstance(value, tuple):
        if len(value) != 3:
            raise ValueError(f"RGB tuple must have 3 elements, got {len(value)}")
        for channel in value:
            if not isinstance(channel, int):
                raise ValueError(f"RGB channel value {channel} is not an integer")
            if not (0 <= channel <= 255):
                raise ValueError(f"RGB channel value {channel} out of range 0-255")
        return value
    if isinstance(value, str):
        if value.lower() in COLOR_PRESETS:
            return COLOR_PRESETS[value]
    raise ValueError(f"Unsupported bg color: {value}")



class RenderStyle(Enum):
    """Enumeration for fill options in the image generation."""
    COLORED_CELLS = "colored_cells"
    COLORED_TEXT = "colored_text"
    COLORED_CELLS_WITH_BACKGROUND_TEXT = (
        "colored_cells_with_background_text"
    )


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
    max_width = 0
    for line in lines:
        max_width = max(max_width, len(line))
    if max_width == 0:
        raise InputError("The string block must not be empty.")
    return True


def file_to_image(file_path: Path | str,
                  value_colors: Optional[dict[str, tuple[int, ...]]] = None,
                  preset: Optional[str] = None,
                  background_color: tuple[int, int, int] = (255, 255, 255),
                  cell_size: int = 32,
                  render_style: RenderStyle = RenderStyle.COLORED_CELLS,
                  font_path: Path = None,
                  font_size: Optional[int] = None) -> Image:
    """Read a string block from a file and convert it to an image.

    Args:
        file_path (Path | str): Path to the file containing the string block.
        value_colors (Optional[dict[str, tuple[int, ...]]]): Mapping of values to RGB colors.
        preset (Optional[str]): Name of a preset colormap to use.
        background_color (tuple[int, int, int]): Background color as an RGB tuple.
        cell_size (int): Size of each cell in pixels.
        render_style (RenderStyle): Style for rendering the image.
        font_path (Path): Path to the font file to use for rendering text.
        font_size (Optional[int]): Size of the font to use for rendering text.
    Returns:
        Image: The generated image.
    """
    grid_str = Path(file_path).read_text()
    img = string_to_image(grid_str, value_colors, preset, background_color, cell_size,
                          render_style, font_path, font_size)
    return img


def string_to_image(grid_str: str,
                    value_colors: Optional[dict[str, tuple[int, ...]]] = None,
                    preset: Optional[str] = None,
                    background_color: tuple[int, int, int] | str = (255, 255, 255),
                    cell_size: int = 32,
                    render_style: RenderStyle = RenderStyle.COLORED_CELLS,
                    font_path: Path = None,
                    font_size: Optional[int] = None) -> Image:
    """Convert a string block to an image.

    Args:
        grid_str (str): The string block representing the grid.
        value_colors (Optional[dict[str, tuple[int, ...]]]): Mapping of values to RGB colors.
        preset (Optional[str]): Name of a preset colormap to use.
        background_color (tuple[int, int, int] | str): Background color as an RGB tuple
        or one of the preset strings.
        cell_size (int): Size of each cell in pixels.
        render_style (RenderStyle): Style for rendering the image.
        font_path (Path): Path to the font file to use for rendering text.
        font_size (Optional[int]): Size of the font to use for rendering text.
    Returns:
        Image: The generated image.
    """
    check_grid_string(grid_str)
    lines = grid_str.strip().split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)

    value_colors, font = get_set_mappings(cell_size, value_colors,
                                            font_path, font_size, preset)
    background_color = resolve_color(background_color)

    img = Image.new('RGB', (width * cell_size, height * cell_size), background_color)
    draw = ImageDraw.Draw(img)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            xy = [x * cell_size, y * cell_size, (x + 1) * cell_size,
                  (y + 1) * cell_size]
            draw.rectangle(xy, fill=background_color)
            match render_style:
                case RenderStyle.COLORED_CELLS_WITH_BACKGROUND_TEXT:
                    color = resolve_color(value_colors.get(char, (0, 0, 0)))
                    draw.rectangle(xy, fill=color)
                    draw_character(background_color, cell_size, char, draw,
                                   font, x, y)
                case RenderStyle.COLORED_CELLS:
                    color = resolve_color(value_colors.get(char, (0, 0, 0)))
                    draw.rectangle(xy, fill=color)
                case RenderStyle.COLORED_TEXT: 
                    color = resolve_color(value_colors.get(char, (0, 0, 0)))
                    draw_character(color, cell_size, char, draw,
                                   font, x, y)
                case _:
                    raise ValueError(
                        f"Invalid show_chars option: {render_style}")
    return img


def draw_character(background_color: tuple[int, int, int], cell_size: int,
                   char: str, draw: ImageDraw, font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                   x: int, y: int):
    bbox = draw.textbbox((0, 0), char, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = x * cell_size + (cell_size - w) // 2
    ty = y * cell_size + (cell_size - h) // 2
    draw.text((tx, ty), char, fill=background_color, font=font)


def get_set_mappings(cell_size: int,
                     value_colors: Optional[dict[str, tuple[int, ...]]],
                     font_path: Optional[Path], font_size: int, preset: str)\
        -> \
tuple[
    dict[str, tuple[int, ...]], ImageFont.FreeTypeFont | ImageFont.ImageFont]:
    """Get value color mapping and font.

    Args:
        cell_size (int): Size of each cell in pixels.
        value_colors (Optional[dict[str, tuple[int, ...]]]): Mapping of values to RGB colors.
        font_path (Optional[Path]): Path to the font file to use for rendering text.
        font_size (int): Size of the font to use for rendering text.
        preset (str): Name of a preset colormap to use.
    Returns:
        tuple[dict[str, tuple[int, ...]], ImageFont.FreeTypeFont | ImageFont.ImageFont]:
        The value color mapping and the font object.
    """
    if preset:
        value_colors = PRESETS.get(preset, {})
    elif value_colors is None:
        value_colors = {}
    # Use bold Consolas if available, else fallback
    if font_path is None:
        font_path = "consolab.ttf"  # Bold Consolas
    if font_size is None:
        font_size = int(cell_size)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        font = ImageFont.load_default()
    return value_colors, font


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

