import streamlit as st
import numpy as np
from collections import defaultdict
import json

# import wcag_auto
# import yiq
import html_boxes

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


with header:
    st.header("Combined color contrast comparator")
    st.write(
        "Compare [WCAG](https://www.w3.org/TR/WCAG20-TECHS/G18.html) (ISO-9241) with [YIQ](https://24ways.org/2010/calculating-color-contrast) color contrast"
    )
    bg_c = st.color_picker("Choose the background color", "#FFFFFF")
    st.text(bg_c.upper())

    r, g, b = str(int(bg_c[1:3], 16)), str(int(bg_c[3:5], 16)), str(int(bg_c[5:], 16))

with inputs:

    fg, bg = st.columns(2)

    ### WCAG ###
    # wcag_color, wcag_contrast = wcag_auto.getContrastColor(bg_c)
    wcag = fetch_wcag()
    wcag_color, wcag_contrast = wcag[r][g][b]

    fg.subheader("WCAG")
    # fg.text(html_boxes.wcag(bg_c, wcag_color))
    wcag_contrast_box = html_boxes.result(bg_c, wcag_color)
    fg.markdown(wcag_contrast_box, unsafe_allow_html=True)
    fg.text(f"Contrast: {wcag_contrast}:1")

    ### YIQ ###
    # yiq_color, yiq_result = yiq.getContrastColor(bg_c)
    yiq = fetch_yiq()
    yiq_color, yiq_result = yiq[r][g][b]

    bg.subheader("YIQ")
    yiq_contrast = html_boxes.result(bg_c, yiq_color)
    bg.markdown(yiq_contrast, unsafe_allow_html=True)
    bg.text(f"YIQ result: {round(yiq_result, 2)}")

    info = st.expander("About")
    info.write(
        "This app selects the text color for the highest contrast between foreground and background color. There's a couple of different ways to calculate the luminance of colors, here there's only according to WCAG's guidelines and YIQ's color space."
    )
