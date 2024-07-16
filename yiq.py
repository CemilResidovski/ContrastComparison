from utils import hex_to_rgb


def get_contrast_color(bg_color):
    bg_color = hex_to_rgb(bg_color)

    yiq = (bg_color[0] * 299.0 + bg_color[1] * 587.0 + bg_color[2] * 114.0) / 1000.0

    return ["black", yiq] if (yiq >= 128) else ["white", yiq]
