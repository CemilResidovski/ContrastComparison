from utils import hex_to_rgb


def normalize(color):
    color_normalized = []
    for ch in color:
        ch = ch / 255.0
        if ch <= 0.03928:
            ch_n = ch / 12.92
        else:
            ch_n = ((ch + 0.055) / 1.055) ** 2.4
        color_normalized.append(ch_n)
    return color_normalized


# Using the luminocity method here from ATSC standards (HDTV)
def get_luminance(color):
    return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]


# Returns [best_color, best_contrast, other_contrast].
# best_contrast is the WCAG ratio for the winning color.
# other_contrast is the WCAG ratio for the opposite color (used when YIQ disagrees).
def get_contrast(lum):
    lum_black = 0.05
    lum_white = 1.05

    ratio_black = round(max(lum_black / lum, lum / lum_black), 2)
    ratio_white = round(max(lum_white / lum, lum / lum_white), 2)
    return (
        ["black", ratio_black, ratio_white]
        if ratio_black > ratio_white
        else ["white", ratio_white, ratio_black]
    )


def get_wcag_result(bg_color):
    # bg RGB
    bg_color = hex_to_rgb(bg_color)

    # Normalize
    bg_norm = normalize(bg_color)

    # Get luminance
    bg_luminance = get_luminance(bg_norm) + 0.05

    return get_contrast(bg_luminance)
