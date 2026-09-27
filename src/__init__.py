from .paintbychar import (
    RenderStyle,
    InputError,
    string_to_image,
    file_to_image,
    check_grid_string,
    get_set_mappings,
    PRESETS,
    get_colormap_dict,
    save_image,
    resolve_color,
    COLOR_PRESETS,
    __version__,
)

__package_name__ = "paintbychar"
__all__ = [
    "RenderStyle",
    "InputError",
    "string_to_image",
    "file_to_image",
    "check_grid_string",
    "get_set_mappings",
    "PRESETS",
    "get_colormap_dict",
    "save_image",
    "resolve_color",
    "COLOR_PRESETS",
    "__version__",
]
