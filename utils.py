import random


def fetch_wcag_reqs(contrast):
    if contrast >= 7:
        return "  \nContrast higher than 7.  \nLevel AAA reached for normal text."
    elif contrast >= 4.5:
        return "  \nContrast higher than 4.5, lower than 7.  \nLevel AAA reached for large text, AA for normal text."
    elif contrast >= 3:
        return "  \nContrast higher than 3, lower than 4.5.  \nLevel AA reached for large text and requirements for graphics and user interface components met."
    else:
        return "  \nContrast lower than 3.  \nNo WCAG requirements met."


def format_hex(color):
    if isinstance(color, tuple) and len(color) == 3:
        return color
    color = color.lstrip("#")
    return [color[i : i + 2] for i in range(0, len(color), 2)]


def hex_to_rgb(color):
    if isinstance(color, tuple) and len(color) == 3:
        return color
    color = format_hex(color)
    return tuple(int(c, 16) for c in color)


def result(background_color, color, contrast):
    if contrast >= 7:
        res = ["(AAA ✅)", "(AAA ✅)"]
    elif contrast >= 4.5:
        res = ["(AAA ✅)", "(AA ✅)"]
    elif contrast >= 3:
        res = ["(AA ✅)", "(AA ❌)"]
    else:
        res = ["(AA ❌)", "(AA ❌)"]
    result = f"""<div style='background-color:{background_color};color:{color};
    margin-left:auto;margin-right:auto;text-align:center;vertical-align:middle;'>
    <p style='font-size:18pt;'>Large text {res[0]}</p>
    <p style='font-size:14pt; font-weight:bold;'>Large text {res[0]}</p>
    <p style="font-size:14pt;">Normal text {res[1]}</p></div>"""
    return result


def info():
    info = """This app sets the text color between black and white for the highest contrast between foreground and background color.<br><br>
    You can see it as essentially "According to the background color, should this text have dark or bright color?"<br><br>
    There's a couple of different ways to calculate the luminance of colors, and thereof the contrast between them for better accessibility. This app calculates it according to WCAG's guidelines and YIQ's color space.<br><br>
    There's nothing really bad about WCAG guidelines (fun fact, for any solid background color, white or black text will always offer a WCAG-compliant contrast higher than 4.5:1! AA standard for normal text will always be fulfilled), I just sometimes prefer the YIQ result, and you might too.<br><br>
    You can keep pressing the button above to get random colors where WCAG and YIQ returns different "best text color" due to their results."""
    return info


def get_random_color(prev_color):
    random_colors = [
        "#009F75",
        "#D54799",
        "#FF0066",
        "#5D74CB",
        "#7E8712",
        "#FF00FF",
        "#EF0000",
        "#239E9E",
        "#00A8FF",
        "#00DA00",
        "#FF26FF",
    ]
    if prev_color in random_colors:
        random_colors.remove(prev_color)
    return random.choice(random_colors)
