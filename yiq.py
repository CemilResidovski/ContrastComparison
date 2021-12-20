# def getContrastColor(fg_color, bg_color):
def getContrastColor(bg_color):
    # fg RGB
    # fg_color = [int(fg_color[1:3], 16), int(fg_color[3:5], 16), int(fg_color[5:], 16)]

    # bg RGB
    bg_color = [int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:], 16)]

    yiq = (bg_color[0] * 299 + bg_color[1] * 587 + bg_color[2] * 114) / 1000

    return ["black", yiq] if (yiq >= 128) else ["white", yiq]

    # return round(ratio, 2)