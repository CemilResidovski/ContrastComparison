def hex_to_rgb(color):
    return [int(color[1:3], 16), int(color[3:5], 16), int(color[5:], 16)]


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


# Observe that the result in index 2 is the reverse of the WCAG contrast.
# Make sure this is only used when YIQ returns the opposite color of WCAG.
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


def get_wcag_result(bg_color, yiq=False):
    # bg RGB
    bg_color = hex_to_rgb(bg_color)

    # Normalize
    bg_norm = normalize(bg_color)

    # Get luminance
    L_b = get_luminance(bg_norm) + 0.05

    return get_contrast(L_b)
