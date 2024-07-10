import streamlit as st
import json
import html_boxes
import yiq
import wcag_auto
import random

header = st.container()
inputs = st.container()


@st.cache()
def fetch_yiq():
    with open("result_yiq.json", "r") as f:
        return json.load(f)


@st.cache()
def fetch_wcag():
    with open("result_wcag.json", "r") as f:
        return json.load(f)


def fetch_wcag_reqs(contrast):
    if contrast >= 7:
        return "Contrast higher than 7, level AAA reached for normal text"
    elif contrast >= 4.5:
        return "Contrast higher than 4.5, level AAA reached for large text, AA for normal text"
    elif contrast >= 3:
        return "Contrast higher than 3, level AA reached for large text and requirements for graphics and user interface components met"


# @st.cache()
def get_random_color(prev_color):
    random_colors = ["#009F75", "#D54799", "#FF0066", "#5D74CB", "#7E8712"]
    return random.choice(random_colors)


with header:
    st.header("Combined color contrast comparator")
    st.write(
        "Compare [WCAG](https://www.w3.org/TR/WCAG20-TECHS/G18.html) (ISO-9241) with [YIQ](https://24ways.org/2010/calculating-color-contrast) color contrast"
    )

    left, right = st.columns(2)
    bg_c = left.color_picker("Choose the background color", "#009F75")
    left.text(bg_c.upper())

    if right.button("Get random conflicting color"):
        bg_c = get_random_color(bg_c)

    r, g, b = str(int(bg_c[1:3], 16)), str(int(bg_c[3:5], 16)), str(int(bg_c[5:], 16))

with inputs:

    fg, bg = st.columns(2)

    ### WCAG ###
    wcag_color, wcag_contrast = wcag_auto.getContrastColor(bg_c)
    # wcag = fetch_wcag()
    # wcag_color, wcag_contrast = wcag[r][g][b]

    fg.subheader("WCAG")
    # fg.text(html_boxes.wcag(bg_c, wcag_color))
    wcag_contrast_box = html_boxes.result(bg_c, wcag_color)
    fg.markdown(wcag_contrast_box, unsafe_allow_html=True)
    fg.write(f"Contrast: {wcag_contrast}:1 - {fetch_wcag_reqs(wcag_contrast)}")

    ### YIQ ###
    yiq_color, yiq_result = yiq.getContrastColor(bg_c)
    # yiq = fetch_yiq()
    # yiq_color, yiq_result = yiq[r][g][b]

    bg.subheader("YIQ")
    yiq_contrast = html_boxes.result(bg_c, yiq_color)
    bg.markdown(yiq_contrast, unsafe_allow_html=True)
    if yiq_color != wcag_color:
        yiq_contrast = wcag_auto.getContrastColor(bg_c, True)
    else:
        yiq_contrast = wcag_contrast
    bg.write(
        f"YIQ result: {round(yiq_result, 2)}. WCAG contrast: {yiq_contrast}:1. {fetch_wcag_reqs(yiq_contrast)}"
    )

    info = st.expander("So what's all this then?")
    info_text = html_boxes.info()
    info.markdown(info_text, unsafe_allow_html=True)
    # info.write(html_formatting.info())
