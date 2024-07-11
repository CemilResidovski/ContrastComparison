def getContrastColor(bg_color, yiq=False):
    # bg RGB
    bg_color = [int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:], 16)]

    # Normalize
    def normalize(color):
        color_normalized = []
        for ch in color:
            ch = ch / 255
            if ch <= 0.03928:
                ch_n = ch / 12.92
            else:
                ch_n = ((ch + 0.055) / 1.055) ** 2.4
            color_normalized.append(ch_n)
        return color_normalized

    bg_norm = normalize(bg_color)

    # Calc contrast ratio
    def get_luminance(c):
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

    L_b = get_luminance(bg_norm) + 0.05

    if yiq:
        return get_yiq_contrast(L_b)
    else:
        return get_best_color(L_b)


def get_best_color(c):
    lum_black = 0.05
    lum_white = 1.05

    if lum_black > c:
        ratio_black = lum_black / c
    else:
        ratio_black = c / lum_black

    if lum_white > c:
        ratio_white = lum_white / c
    else:
        ratio_white = c / lum_white

    return (
        ["black", round(ratio_black, 1)]
        if (ratio_black > ratio_white)
        else ["white", round(ratio_white, 1)]
    )


def get_yiq_contrast(c):
    lum_black = 0.05
    lum_white = 1.05

    if lum_black > c:
        ratio_black = lum_black / c
    else:
        ratio_black = c / lum_black

    if lum_white > c:
        ratio_white = lum_white / c
    else:
        ratio_white = c / lum_white

    return (
        round(ratio_black, 1) if (ratio_black < ratio_white) else round(ratio_white, 1)
    )
