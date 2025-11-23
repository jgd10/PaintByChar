import sys
import importlib.util
from pathlib import Path
import pytest
from PIL import ImageFont
import glob


def load_main_module():
    # Load src/main.py by path to avoid package import issues.
    root = Path(__file__).resolve().parents[1]
    src_path = root / "src" / "main.py"
    spec = importlib.util.spec_from_file_location("project_main", src_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["project_main"] = module
    spec.loader.exec_module(module)
    return module


class TestGridString:
    @pytest.mark.parametrize("grid_str", [
        "abc\ndef\nghi",
        "abc\ndef\nghi\n",
        "1234\n5678\n9012",
        "A\nB\nC",
        "■\n■",
        "X Y Z\n1 2 3\n! @ #",
        "L",
        "NOP"
    ])
    def test_grid_string_valid(self, grid_str):
        m = load_main_module()
        assert m.check_grid_string(grid_str) is True

    @pytest.mark.parametrize("grid_str", [
        "",
        "\n",
        "   ",
        "abc\nde\nfgh",
        "12\n345\n6789",
        "A B\nC D E",
        "X Y Z\n1 2\n! @ #"
        "XYZ\n12 3\n!@#"
    ])
    def test_grid_string_invalid(self, grid_str):
        m = load_main_module()
        with pytest.raises(m.InputError):
            m.check_grid_string(grid_str)


def test_get_set_mappings_font_fallback():
    m = load_main_module()
    char_map, font = m.get_set_mappings(12, None, Path("nonexistent-font.ttf"), None, None)
    assert isinstance(char_map, dict)
    # default font should be returned when truetype fails
    assert (isinstance(font, ImageFont.FreeTypeFont)
            or isinstance(font, ImageFont.ImageFont))


def test_block_to_image_fill_both_pixel_color():
    m = load_main_module()
    # single-cell grid; use a deterministic color
    grid = "A"
    char_color_map = {"A": (10, 20, 30)}
    img = m.block_to_image(grid,
                           char_color_map=char_color_map,
                           cell_size=10,
                           fill_option=m.FillOption.BOTH)
    assert img.size == (10, 10)
    # center pixel should be filled with the mapping color
    assert img.getpixel((5, 5)) == (10, 20, 30)


def test_block_to_image_fill_background_pixel_color():
    m = load_main_module()
    # single-cell grid; use a deterministic color
    grid = "`"
    char_color_map = {"`": (40, 50, 60)}
    img = m.block_to_image(grid,
                           char_color_map=char_color_map,
                           cell_size=100,
                           fill_option=m.FillOption.BACKGROUND)
    # inspection
    assert img.size == (100, 100)
    # center pixel should be filled with the mapping color
    assert img.getpixel((5, 5)) == (40, 50, 60)


def test_block_to_image_fill_chars_pixel_color():
    m = load_main_module()
    # single-cell grid; use a deterministic color
    grid = "■"
    char_color_map = {"■": (70, 80, 90)}
    img = m.block_to_image(grid,
                           char_color_map=char_color_map,
                           cell_size=10,
                           fill_option=m.FillOption.CHARS)
    assert img.size == (10, 10)
    # center pixel should be filled with the mapping color
    assert img.getpixel((5, 5)) == (70, 80, 90)


def test_block_to_image_invalid_fill_option():
    m = load_main_module()
    grid = "A"
    with pytest.raises(ValueError):
        m.block_to_image(grid,
                         char_color_map={"A": (0, 0, 0)},
                         cell_size=10,
                         fill_option="INVALID_OPTION")


@pytest.mark.parametrize("colormap_name", [
    "viridis",
    "plasma",
    "inferno",
    "magma",
    "cividis",
    "terrain",
    "coolwarm"])
def test_preset_applied_to_char_color_map(colormap_name):
    import matplotlib.pyplot as plt
    m = load_main_module()
    cmap = plt.get_cmap(colormap_name)
    grid = "5"
    img = m.block_to_image(grid,
                           preset=colormap_name,
                           cell_size=90,
                           fill_option=m.FillOption.BOTH)
    assert img.size == (90, 90)
    assert img.getpixel((50, 50)) == tuple([int(c*255) for c in cmap(5 / 9)[
        :3]])


def test_file_to_image_reads_file(tmp_path):
    m = load_main_module()
    p = tmp_path / "grid.txt"
    p.write_text("X")
    # ensure the mapping for X is provided to get deterministic colors
    img = m.file_to_image(str(p),
                          char_color_map={"X": (1, 2, 3)},
                          bg_color=(255, 255, 255),
                          cell_size=8,
                          fill_option=m.FillOption.BOTH)
    assert img.size == (8, 8)
    assert img.getpixel((4, 4)) == (1, 2, 3)


def test_file_to_image_invalid_file(tmp_path):
    m = load_main_module()
    p = tmp_path / "invalid_grid.txt"
    p.write_text("AB\nC")  # inconsistent line lengths
    with pytest.raises(m.InputError):
        m.file_to_image(str(p),
                        char_color_map={"A": (0, 0, 0),
                                        "B": (0, 0, 0),
                                        "C": (0, 0, 0)},
                        cell_size=10,
                        fill_option=m.FillOption.CHARS)

def test_file_to_image_nonexistent_file():
    m = load_main_module()
    with pytest.raises(FileNotFoundError):
        m.file_to_image("nonexistent_file.txt",
                        char_color_map={"A": (0, 0, 0)},
                        cell_size=10,
                        fill_option=m.FillOption.CHARS)


def test_get_colormap_dict_length_and_values():
    m = load_main_module()
    colormap_name = "viridis"
    colormap_dict = m.get_colormap_dict(colormap_name)
    assert len(colormap_dict) == 10
    for i in range(10):
        color = colormap_dict[str(i)]
        assert isinstance(color, tuple)
        assert len(color) == 3
        for channel in color:
            assert 0 <= channel <= 255

def test_get_colormap_dict_invalid_name():
    m = load_main_module()
    with pytest.raises(ValueError):
        m.get_colormap_dict("invalid_colormap_name")


def test_presets_contain_expected_keys():
    m = load_main_module()
    expected_keys = {'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'terrain', 'coolwarm'}
    assert set(m.PRESETS.keys()) == expected_keys


def test_save_image_to_path(tmp_path):
    from PIL import Image
    m = load_main_module()
    grid = "A"
    img = m.block_to_image(grid,
                           char_color_map={"A": (100, 150, 200)},
                           cell_size=10,
                           fill_option=m.FillOption.BOTH)
    output_path = tmp_path / "output_image.png"
    m.save_image(img, output_path)
    assert output_path.exists()
    loaded_img = Image.open(output_path)
    assert loaded_img.size == img.size
    assert loaded_img.getpixel((5, 5)) == (100, 150, 200)
