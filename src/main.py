from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from pathlib import Path

def get_colormap_dict(colormap_name):
    cmap = plt.get_cmap(colormap_name)
    colors = [tuple(int(255 * c) for c in cmap(i / 9)[:3]) for i in range(10)]
    return {str(i): colors[i] for i in range(10)}

PRESETS = {
    'viridis': get_colormap_dict('viridis'),
    'plasma': get_colormap_dict('plasma'),
}

def grid_to_image(grid_str, char_color_map=None, preset=None, bg_color=(255,255,255), cell_size=32, out_path='grid.png', show_chars=False, font_path=None, font_size=None):
    lines = grid_str.strip().split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)
    img = Image.new('RGB', (width * cell_size, height * cell_size), bg_color)
    draw = ImageDraw.Draw(img)

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

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            xy = [x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size]
            draw.rectangle(xy, fill=bg_color)
            if show_chars:
                color = char_color_map.get(char, (0, 0, 0))
                bbox = draw.textbbox((0, 0), char, font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                tx = x * cell_size + (cell_size - w) // 2
                ty = y * cell_size + (cell_size - h) // 2
                draw.text((tx, ty), char, fill=color, font=font)

    img.save(out_path)
    print(f"Saved image to {out_path}")

# Example usage:
if __name__ == "__main__":
    grid = Path('../tests/example4.txt').read_text()
    grid_to_image(grid, preset='viridis', bg_color=(240,240,240), cell_size=40, out_path='viridis_grid_chars.png', show_chars=True, font_size=32)
