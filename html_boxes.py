def result(background_color, color):
    result = f"""<div style='background-color:{background_color};color:{color};
    margin-left:auto;margin-right:auto;text-align:center;vertical-align:middle;'>
    <p style='font-size:24px;'>Large text</p>
    <p style='font-size:18.5px;font-weight:bold;'>Large text</p>
    <p style="font-size:18.5px;">Normal text</p></div>"""
    return result
