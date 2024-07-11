def format_color(color):
    return [int(color[1:3], 16), int(color[3:5], 16), int(color[5:], 16)]


def get_contrast_color(bg_color):
    bg_color = format_color(bg_color)

    yiq = (bg_color[0] * 299 + bg_color[1] * 587 + bg_color[2] * 114) / 1000

    return ["black", yiq] if (yiq >= 128) else ["white", yiq]

    # return round(ratio, 2)
