def result(background_color, color):
    result = f"""<div style='background-color:{background_color};color:{color};
    margin-left:auto;margin-right:auto;text-align:center;vertical-align:middle;'>
    <p style='font-size:24px;'>Large text</p>
    <p style='font-size:18.5px;font-weight:bold;'>Large text</p>
    <p style="font-size:18.5px;">Normal text</p></div>"""
    return result


def info():
    info = """This app sets the text color between black and white for the highest contrast between foreground and background color.</br>
    You can see it as essentially "According to the background color, should this text have dark or bright color?"</br>
    There's a couple of different ways to calculate the luminance of colors, and thereof the contrast between them for better accessibility, here there's according to WCAG's guidelines and YIQ's color space.</br>
    There's nothing really bad about WCAG guidelines (fun fact, for any solid background color, white or black text will always offer a WCAG-compliant contrast higher than 4.5:1! AA standard for normal text will always be fulfilled),</br>
    I just sometimes prefer the YIQ result, and you might too.</br>
    You can keep refreshing this page to get random colors where WCAG and YIQ returns different "best color" depending on their results."""
    return info
