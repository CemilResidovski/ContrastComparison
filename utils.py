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


def intro():
    return "For a given background color, will white or black foreground text color be more visible?  \n\nThis web app compares [WCAG](https://www.w3.org/TR/WCAG20-TECHS/G18.html) (ISO-9241) with [YIQ](https://24ways.org/2010/calculating-color-contrast) color contrast, and checks which WCAG requirements the foreground text color clears."


def info():
    info = """This app determines whether black or white text will provide the highest contrast against a given background color.

Think of it as asking, "Given this background color, should the text be dark or bright?"

There are different methods to calculate the luminance and contrast of colors for better accessibility. This app uses the WCAG guidelines and the YIQ color space to perform these calculations. The YIQ method is also commonly used for creating greyscale images.

While WCAG guidelines are effective (fun fact: for any solid background color, white or black text will always meet the WCAG-compliant contrast ratio of 4.5:1 for normal text, fulfilling the AA standard), I sometimes prefer the YIQ results, and you might too.

You can keep pressing the button above to get random background colors where WCAG and YIQ recommend different text colors due to their differing calculations."""
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
