import streamlit as st
import utils
import yiq
import wcag
import compare
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
    else:
        return "  \nContrast lower than 3.  \nNo WCAG contrast requirements met."


RANDOM_COLORS = [
    "#009F75",
    "#D54799",
    "#5D74CB",
    "#7E8712",
    "#8D70B0",
    "#FF5800",
    "#FF00F8",
    "#B058D0",
    "#7F7F7F",
    "#02A7FF",
]


def randomize_color():
    current = st.session_state.bg_color.upper()
    choices = [c for c in RANDOM_COLORS if c != current]
    st.session_state.bg_color = random.choice(choices)


with header:
    st.header("Combined color contrast comparator")
    st.write(utils.intro())

    left, right = st.columns(2)
    if "bg_color" not in st.session_state:
        st.session_state.bg_color = "#D54799"
    bg_c = left.color_picker("Choose the background color", key="bg_color").upper()
    left.text(bg_c)

    right.button("Get random conflicting color", on_click=randomize_color)

with inputs:

    left, right = st.columns(2)

    ### WCAG ###
    wcag_color, wcag_contrast, other_contrast = wcag.get_wcag_result(bg_c)

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
            f"WCAG contrast: {other_contrast}:1. {fetch_wcag_reqs(other_contrast)}"
        )
    else:
        other_contrast = wcag_contrast
        yiq_result_text += f"WCAG contrast: {other_contrast}:1."

    other_contrast_box = utils.result(bg_c, yiq_color, other_contrast)
    right.markdown(other_contrast_box, unsafe_allow_html=True)
    right.write(yiq_result_text)

    with st.expander("How would this look in greyscale?"):
        greyscaled_bg_color = f"rgb({round(yiq_result, 2)}, {round(yiq_result, 2)}, {round(yiq_result, 2)})"
        left_grey, right_grey = st.columns(2)
        left_grey.subheader("WCAG greyscale")
        wcag_grey = utils.result(
            grey,
            wcag_color,
            wcag_contrast,
        )
        left_grey.markdown(wcag_grey, unsafe_allow_html=True)

        right_grey.subheader("YIQ greyscale")
        yiq_greyscale = utils.result(greyscaled_bg_color, yiq_color, other_contrast)
        right_grey.markdown(yiq_greyscale, unsafe_allow_html=True)

    info = st.expander("So what's all this then?")
    info_text = utils.info()
    info.markdown(info_text, unsafe_allow_html=True)

    st.subheader("Where do WCAG and YIQ disagree?")
    st.write(
        "For these colors, WCAG and YIQ return different 'best text color'. "
        "Bright pixels = disagreement, dimmed pixels = agreement."
    )

    left_ctrl, right_ctrl = st.columns(2)
    channel = left_ctrl.selectbox("Fixed channel", ["Red", "Green", "Blue"])
    value = right_ctrl.slider(f"{channel} value", 0, 255, 128)

    result_img, row_label, col_label, disagree_count, disagree_pct = (
        compare.compute_disagreement(channel, value)
    )

    st.image(
        result_img,
        caption=f"{channel} = {value} | X: {col_label} (0→255) | Y: {row_label} (0→255) | Disagreements: {disagree_count} ({disagree_pct:.1f}%)",
    )
