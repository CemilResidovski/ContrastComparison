import json
from collections import defaultdict

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


def get_luminance(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2] + 0.05


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
        ("black", round(ratio_black, 2))
        if (ratio_black > ratio_white)
        else ("white", round(ratio_white, 2))
    )


lums = defaultdict(lambda: defaultdict(dict))

for r in range(256):
    for g in range(256):
        for b in range(256):
            color = [r, g, b]
            color_norm = normalize(color)
            color_lum = get_luminance(color_norm)
            best_color = get_best_color(color_lum)
            lums[r][g][b] = best_color

with open("result_wcag.json", "w") as f:
    json.dump(lums, f)
