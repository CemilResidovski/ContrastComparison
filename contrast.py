import streamlit as st
import html_boxes
import yiq
import wcag
import random

header = st.container()
inputs = st.container()


def fetch_wcag_reqs(contrast):
    if contrast >= 7:
        return "  \nContrast higher than 7.  \nLevel AAA reached for normal text."
    elif contrast >= 4.5:
        return "  \nContrast higher than 4.5, lower than 7.  \nLevel AAA reached for large text, AA for normal text."
    elif contrast >= 3:
        return "  \nContrast higher than 3, lower than 4.5.  \nLevel AA reached for large text and requirements for graphics and user interface components met."


def get_random_color(prev_color):
    random_colors = [
        "#009F75",
        "#D54799",
        "#FF0066",
        "#5D74CB",
        "#7E8712",
        "#777777",
        "#FF00FF",
        "#FF0000",
        "#239E9E",
    ]
    if prev_color in random_colors:
        random_colors.remove(prev_color)
    return random.choice(random_colors)


with header:
    st.header("Combined color contrast comparator")
    st.write(
        "For a given background color, will white or black foreground text color be more visible?  \n\nThis web app compares [WCAG](https://www.w3.org/TR/WCAG20-TECHS/G18.html) (ISO-9241) with [YIQ](https://24ways.org/2010/calculating-color-contrast) color contrast."
    )

    left, right = st.columns(2)
    bg_c = left.color_picker("Choose the background color", "#009F75").upper()
    left.text(bg_c)

    if right.button("Get random conflicting color"):
        bg_c = get_random_color(bg_c)

with inputs:

    left, right = st.columns(2)

    ### WCAG ###
    wcag_color, wcag_contrast, yiq_contrast = wcag.get_wcag_result(bg_c)

    left.subheader("WCAG")
    wcag_contrast_box = html_boxes.result(bg_c, wcag_color, wcag_contrast)
    left.markdown(wcag_contrast_box, unsafe_allow_html=True)
    left.write(f"Contrast: {wcag_contrast}:1. {fetch_wcag_reqs(wcag_contrast)}")

    ### YIQ ###
    yiq_color, yiq_result = yiq.get_contrast_color(bg_c)

    right.subheader("YIQ")
    yiq_result_text = f"YIQ result: {round(yiq_result, 2)}. "

    if yiq_color != wcag_color:
        yiq_result_text += (
            f"WCAG contrast: {yiq_contrast}:1. {fetch_wcag_reqs(yiq_contrast)}"
        )
    else:
        yiq_contrast = wcag_contrast
        yiq_result_text += f"WCAG contrast: {yiq_contrast}:1."

    yiq_contrast_box = html_boxes.result(bg_c, yiq_color, yiq_contrast)
    right.markdown(yiq_contrast_box, unsafe_allow_html=True)
    right.write(yiq_result_text)

    with st.expander("How would this look in greyscale?"):
        greyscaled_bg_color = f"rgb({yiq_result}, {yiq_result}, {yiq_result})"
        left_grey, right_grey = st.columns(2)
        left_grey.subheader("WCAG greyscale")
        wcag_greyscale = html_boxes.result(
            greyscaled_bg_color,
            wcag_color,
            wcag_contrast,
        )
        left_grey.markdown(wcag_greyscale, unsafe_allow_html=True)

        right_grey.subheader("YIQ greyscale")
        yiq_greyscale = html_boxes.result(greyscaled_bg_color, yiq_color, yiq_contrast)
        right_grey.markdown(yiq_greyscale, unsafe_allow_html=True)

    info = st.expander("So what's all this then?")
    info_text = html_boxes.info()
    info.markdown(info_text, unsafe_allow_html=True)
