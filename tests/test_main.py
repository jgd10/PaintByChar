import importlib.util
import sys
from pathlib import Path

import pytest
from PIL import ImageFont


def load_main_module():
    # Load src/main.py by path to avoid package import issues.
    root = Path(__file__).resolve().parents[1]
    src_path = root / "src" / "paintbychar.py"
    spec = importlib.util.spec_from_file_location("project_main", src_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["project_main"] = module
    spec.loader.exec_module(module)
    return module


class TestGridString:
    @pytest.mark.parametrize("grid_str", ["abc\ndef\nghi", "abc\ndef\nghi\n",
        "1234\n5678\n9012", "A\nB\nC", "■\n■", "X Y Z\n1 2 3\n! @ #", "L",
        "NOP"])
    def test_grid_string_valid(self, grid_str):
        m = load_main_module()
        assert m.check_grid_string(grid_str) is True

    @pytest.mark.parametrize("grid_str", ["", "\n", "   "])
    def test_grid_string_invalid(self, grid_str):
        m = load_main_module()
        with pytest.raises(m.InputError):
            m.check_grid_string(grid_str)


def test_get_set_mappings_font_fallback():
    m = load_main_module()
    char_map, font = m.get_set_mappings(12, None, Path("nonexistent-font.ttf"),
                                        None, None)
    assert isinstance(char_map, dict)
    # default font should be returned when truetype fails
    assert (isinstance(font, ImageFont.FreeTypeFont) or isinstance(font,
                                                                   ImageFont.ImageFont))


class TestRenderStyle:
    @pytest.mark.parametrize("style", ["COLORED_CELLS", "COLORED_TEXT",
        "COLORED_CELLS_WITH_BACKGROUND_TEXT"])
    def test_render_style_valid(self, style):
        m = load_main_module()
        assert m.RenderStyle[style] is not None

    @pytest.mark.parametrize("invalid_style",
                             ["INVALID_OPTION", "colored_cells",
                                 "Colored_Text", "", None])
    def test_render_style_invalid(self, invalid_style):
        m = load_main_module()
        with pytest.raises(KeyError):
            _ = m.RenderStyle[invalid_style]

    def test_string_to_image_background_color_is_used_for_empty_character_area(
            self):
        m = load_main_module()
        img = m.string_to_image("A", background_color=(11, 22, 33),
                                cell_size=100,
                                render_style=m.RenderStyle.COLORED_TEXT,
                                value_colors={"A": (200, 201, 202)})
        pixels = list(img.getdata())
        assert (11, 22, 33) in pixels
        assert (200, 201, 202) in pixels

    def test_string_to_image_background_mode_draws_character_in_background_color(
            self):
        m = load_main_module()
        img = m.string_to_image("A", background_color=(11, 22, 33),
                                cell_size=100,
                                render_style=m.RenderStyle.COLORED_CELLS_WITH_BACKGROUND_TEXT,
                                value_colors={"A": (200, 201, 202)})
        pixels = list(img.getdata())
        print(pixels)
        assert (200, 201, 202) in pixels
        assert (11, 22, 33) in pixels

    def test_string_to_image_COLORED_CELLS_mode_fills_every_pixel_in_cell(self):
        m = load_main_module()
        img = m.string_to_image("A", background_color=(11, 22, 33),
                                cell_size=10,
                                render_style=m.RenderStyle.COLORED_CELLS,
                                value_colors={"A": (200, 201, 202)})
        assert set(img.getdata()) == {(200, 201, 202)}

    def test_string_to_image_invalid_render_style(self):
        m = load_main_module()
        grid = "A"
        with pytest.raises(ValueError):
            m.string_to_image(grid, value_colors={"A": (0, 0, 0)},
                              cell_size=10, render_style="INVALID_OPTION")


@pytest.mark.parametrize("grid_str", ["", "\n"])
def test_string_to_image_rejects_invalid_grid(grid_str):
    m = load_main_module()
    with pytest.raises(m.InputError):
        img = m.string_to_image(grid_str)


def test_string_to_image_rectangular_dimensions():
    m = load_main_module()
    img = m.string_to_image("AB\nCD", cell_size=7)
    assert img.size == (14, 14)


def test_string_to_image_irregular_dimensions():
    m = load_main_module()
    img = m.string_to_image("ABCE\nCDE\nAC\n\nDEFGH", cell_size=5)
    assert img.size == (25, 25)


@pytest.mark.parametrize("value",
                         [(1, 2), (1, 2, 3, 4), (1.5, 2, 3), ("1", 2, 3)])
def test_resolve_color_rejects_malformed_rgb_tuples(value):
    m = load_main_module()
    with pytest.raises(ValueError):
        m.resolve_color(value)


@pytest.mark.parametrize("cell_size", [0, -1])
def test_string_to_image_rejects_non_positive_cell_size(cell_size):
    m = load_main_module()
    with pytest.raises(ValueError):
        m.string_to_image("A", cell_size=cell_size)


def test_missing_character_mapping_uses_black():
    m = load_main_module()
    img = m.string_to_image("A", cell_size=10,
                            render_style=m.RenderStyle.COLORED_CELLS)
    assert set(img.getdata()) == {(0, 0, 0)}


@pytest.mark.parametrize("value", [True, False])
def test_bool_rgb(value):
    m = load_main_module()
    img = m.string_to_image("A", cell_size=10,
                            value_colors={'A': (value, value, value)},
                            render_style=m.RenderStyle.COLORED_CELLS,
                            background_color='red')
    assert set(img.getdata()) == {(value, value, value)}


def test_preset_takes_precedence_over_character_mapping():
    m = load_main_module()
    img = m.string_to_image("5", preset="viridis", cell_size=10,
                            render_style=m.RenderStyle.COLORED_CELLS,
                            value_colors={"5": (1, 2, 3)})
    assert img.getpixel((5, 5)) == m.PRESETS["viridis"]["5"]


def test_file_to_image_accepts_path_object(tmp_path):
    m = load_main_module()
    path = tmp_path / "grid.txt"
    path.write_text("AB\nCD")
    img = m.file_to_image(path, cell_size=6,
                          value_colors={char: (1, 2, 3) for char in "ABCD"},
                          render_style=m.RenderStyle.COLORED_CELLS)
    assert img.size == (12, 12)


def test_file_to_image_accepts_trailing_newline(tmp_path):
    m = load_main_module()
    path = tmp_path / "grid.txt"
    path.write_text("A\n")
    img = m.file_to_image(path, cell_size=6, value_colors={"A": (1, 2, 3)},
                          render_style=m.RenderStyle.COLORED_CELLS)
    assert img.size == (6, 6)


@pytest.mark.parametrize("colormap_name",
                         ["viridis", "plasma", "inferno", "magma", "cividis",
                             "terrain", "coolwarm"])
def test_preset_applied_to_value_colors(colormap_name):
    import matplotlib.pyplot as plt
    m = load_main_module()
    cmap = plt.get_cmap(colormap_name)
    grid = "5"
    img = m.string_to_image(grid, preset=colormap_name, cell_size=90,
                            render_style=m.RenderStyle.COLORED_CELLS)
    assert img.size == (90, 90)
    assert img.getpixel((50, 50)) == tuple(
        [int(c * 255) for c in cmap(5 / 9)[:3]])


def test_file_to_image_reads_file(tmp_path):
    m = load_main_module()
    p = tmp_path / "grid.txt"
    p.write_text("X")
    # ensure the mapping for X is provided to get deterministic colors
    img = m.file_to_image(str(p), value_colors={"X": (1, 2, 3)},
                          background_color=(255, 255, 255), cell_size=8,
                          render_style=m.RenderStyle.COLORED_CELLS)
    assert img.size == (8, 8)
    assert img.getpixel((4, 4)) == (1, 2, 3)


def test_file_to_image_invalid_file(tmp_path):
    m = load_main_module()
    p = tmp_path / "invalid_grid.txt"
    p.write_text("\n")  # inconsistent line lengths
    with pytest.raises(m.InputError):
        m.file_to_image(str(p), value_colors={"A": (0, 0, 0), "B": (0, 0, 0),
                                              "C": (0, 0, 0)}, cell_size=10,
                        render_style=m.RenderStyle.COLORED_TEXT)


def test_file_to_image_nonexistent_file():
    m = load_main_module()
    with pytest.raises(FileNotFoundError):
        m.file_to_image("nonexistent_file.txt", value_colors={"A": (0, 0, 0)},
                        cell_size=10, render_style=m.RenderStyle.COLORED_TEXT)


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
    expected_keys = {'viridis', 'plasma', 'inferno', 'magma', 'cividis',
                     'terrain', 'coolwarm'}
    assert set(m.PRESETS.keys()) == expected_keys


def test_save_image_to_path(tmp_path):
    from PIL import Image
    m = load_main_module()
    grid = "A"
    img = m.string_to_image(grid, value_colors={"A": (100, 150, 200)},
                            cell_size=10, render_style=m.RenderStyle.COLORED_CELLS)
    output_path = tmp_path / "output_image.png"
    m.save_image(img, output_path)
    assert output_path.exists()
    loaded_img = Image.open(output_path)
    assert loaded_img.size == img.size
    assert loaded_img.getpixel((5, 5)) == (100, 150, 200)


class TestColorPresets:
    @pytest.mark.parametrize("preset_name",
                             ["white", "black", "light_gray", "dark_gray",
                                 "pastel_blue", "pastel_green", "pastel_pink",
                                 "cream", "beige", "mint", "navy", "charcoal",
                                 "soft_yellow", "gray", "blue", "green",
                                 "pink", "yellow", "teal", "brown", "red"])
    def test_resolve_color_valid(self, preset_name):
        m = load_main_module()
        color = m.resolve_color(preset_name)
        assert isinstance(color, tuple)
        assert len(color) == 3
        for channel in color:
            assert 0 <= channel <= 255

    @pytest.mark.parametrize("invalid_value",
                             ["unknown_color", (256, 0, 0), (-1, 0, 0),
                                 "123,456,789", 12345, None])
    def test_resolve_color_invalid(self, invalid_value):
        m = load_main_module()
        with pytest.raises(ValueError):
            color = m.resolve_color(invalid_value)
            for channel in color:
                assert 0 <= channel <= 255

# TODO: Add a test once the expected behavior for an unknown preset is defined.
# TODO: Add tests for font_size=0, negative font_size, and a valid custom font.
# TODO: Add tests for empty files, CRLF files, and Unicode file contents.
# TODO: Add tests for save_image overwriting files and nonexistent parent 
#  paths.
