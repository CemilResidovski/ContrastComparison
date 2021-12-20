def getContrastColor(fg_color, bg_color):
    # fg RGB
    fg_color = [int(fg_color[1:3], 16), int(fg_color[3:5], 16), int(fg_color[5:], 16)]

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

    fg_norm = normalize(fg_color)
    bg_norm = normalize(bg_color)

    # Calc contrast ratio
    def get_luminance(c):
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

    L_f = get_luminance(fg_norm) + 0.05
    L_b = get_luminance(bg_norm) + 0.05

    if L_f > L_b:
        ratio = L_f / L_b
    else:
        ratio = L_b / L_f

    print(f"L blac: {L_f}")
    print(f"L white: {L_b}")
    # return round(ratio, 2)
    # alternatively, if contrast is strictly more than 5, return black color, else white
    # this seems very suspicious, is there always a contrast higher than 5? what about perfect grey?
    # calculate luminance for black and white (once) then compare background color with bolthf


getContrastColor("#000000", "#FFFFFF")
black = 0.05
white = 1.05