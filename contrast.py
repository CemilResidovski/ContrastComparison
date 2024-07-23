import streamlit as st
import utils
import yiq
import wcag

header = st.container()
inputs = st.container()
colors = st.container()


with header:
    st.header("Combined color contrast comparator")
    st.write(utils.intro())

    left, right = st.columns(2)

    bg_c = left.color_picker("Choose the background color", "#7F7F7F").upper()
    if right.button("Get random conflicting color"):
        bg_c = utils.get_random_color(bg_c)
    left.text(bg_c)


with inputs:

    left, right = st.columns(2)

    ### WCAG ###
    wcag_color, wcag_contrast, yiq_contrast = wcag.get_wcag_result(bg_c)

    left.subheader("WCAG")
    wcag_contrast_box = utils.result(bg_c, wcag_color, wcag_contrast)
    left.markdown(wcag_contrast_box, unsafe_allow_html=True)
    left.write(f"Contrast: {wcag_contrast}:1. {utils.fetch_wcag_reqs(wcag_contrast)}")

    ### YIQ ###
    if utils.format_hex(bg_c)[1] <= "DA":
        yiq_color, yiq_result = yiq.get_yiq_result(bg_c)
    else:
        yiq_color = wcag_color
        yiq_result = None

    right.subheader("YIQ")
    yiq_result_text = f"YIQ result: {yiq_result}. "

    if yiq_color != wcag_color:
        yiq_result_text += (
            f"WCAG contrast: {yiq_contrast}:1. {utils.fetch_wcag_reqs(yiq_contrast)}"
        )
    else:
        yiq_contrast = wcag_contrast
        yiq_result_text += f"WCAG contrast: {yiq_contrast}:1."

    yiq_contrast_box = utils.result(bg_c, yiq_color, yiq_contrast)
    right.markdown(yiq_contrast_box, unsafe_allow_html=True)
    right.write(yiq_result_text)

    with st.expander("How would this look in greyscale?"):
        grey = f"rgb({yiq_result}, {yiq_result}, {yiq_result})"
        left_grey, right_grey = st.columns(2)
        left_grey.subheader("WCAG greyscale")
        wcag_grey = utils.result(
            grey,
            wcag_color,
            wcag_contrast,
        )
        left_grey.markdown(wcag_grey, unsafe_allow_html=True)

        right_grey.subheader("YIQ greyscale")
        yiq_grey = utils.result(grey, yiq_color, yiq_contrast)
        right_grey.markdown(yiq_grey, unsafe_allow_html=True)

with colors:
    with st.expander("Show color spectrums"):
        r, g, b = st.columns(3)
        c = utils.hex_to_rgb(bg_c)

        r.image(f"r/{c[0]}.png")

        if c[1] >= 219:
            g.image("g/219.png")
        else:
            g.image(f"g/{c[1]}.png")

        b.image(f"b/{c[2]}.png")
        r.caption(f"Colors with differing foreground colors for red value of {c[0]}")
        g.caption(f"Colors with differing foreground colors for green value of {c[1]}")
        b.caption(f"Colors with differing foreground colors for blue value of {c[2]}")

    info = st.expander("So what's all this then?")
    info_text = utils.info()
    info.markdown(info_text, unsafe_allow_html=True)
