import streamlit as st
import numpy as np
import utils
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
        "#FF00FF",
        "#FF0000",
        "#00A4FE",
    ]
    if prev_color in random_colors:
        random_colors.remove(prev_color)
    return random.choice(random_colors)


with header:
    st.header("Combined color contrast comparator")
    st.write(
        "For a given background color, will white or black foreground text color be more visible?  \n\nThis web app compares [WCAG](https://www.w3.org/TR/WCAG20-TECHS/G18.html) (ISO-9241) with [YIQ](https://24ways.org/2010/calculating-color-contrast) color contrast, and checks which WCAG requirements the foreground text color clears."
    )

    left, right = st.columns(2)
    bg_c = left.color_picker("Choose the background color", "#7F7F7F").upper()
    left.text(bg_c)

    if right.button("Get random conflicting color"):
        bg_c = get_random_color(bg_c)

with inputs:

    left, right = st.columns(2)

    ### WCAG ###
    wcag_color, wcag_contrast, yiq_contrast = wcag.get_wcag_result(bg_c)

    left.subheader("WCAG")
    wcag_contrast_box = utils.result(bg_c, wcag_color, wcag_contrast)
    left.markdown(wcag_contrast_box, unsafe_allow_html=True)
    left.write(f"Contrast: {wcag_contrast}:1. {fetch_wcag_reqs(wcag_contrast)}")

    ### YIQ ###
    yiq_color, yiq_result = yiq.get_yiq_result(bg_c)

    right.subheader("YIQ")
    yiq_result_text = f"YIQ result: {round(yiq_result, 2)}. "

    if yiq_color != wcag_color:
        yiq_result_text += (
            f"WCAG contrast: {yiq_contrast}:1. {fetch_wcag_reqs(yiq_contrast)}"
        )
    else:
        yiq_contrast = wcag_contrast
        yiq_result_text += f"WCAG contrast: {yiq_contrast}:1."

    yiq_contrast_box = utils.result(bg_c, yiq_color, yiq_contrast)
    right.markdown(yiq_contrast_box, unsafe_allow_html=True)
    right.write(yiq_result_text)

    with st.expander("How would this look in greyscale?"):
        greyscaled_bg_color = f"rgb({yiq_result}, {yiq_result}, {yiq_result})"
        left_grey, right_grey = st.columns(2)
        left_grey.subheader("WCAG greyscale")
        wcag_greyscale = utils.result(
            greyscaled_bg_color,
            wcag_color,
            wcag_contrast,
        )
        left_grey.markdown(wcag_greyscale, unsafe_allow_html=True)

        right_grey.subheader("YIQ greyscale")
        yiq_greyscale = utils.result(greyscaled_bg_color, yiq_color, yiq_contrast)
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

    # The disagreement region is always a contiguous band along the free channel axis.
    # Instead of evaluating every pixel, analytically solve each algorithm's flip point.
    # Mark the band as "disagreement" and visualize.
    YIQ_W = [299, 587, 114]  # R, G, B
    WCAG_W = [0.2126, 0.7152, 0.0722]
    WCAG_LUM_THRESHOLD = np.sqrt(0.0525) - 0.05

    def srgb_normalize(ch):
        ch_n = ch / 255.0
        return np.where(ch_n <= 0.03928, ch_n / 12.92, ((ch_n + 0.055) / 1.055) ** 2.4)

    def srgb_denormalize(ch_n):
        ch_n = np.clip(ch_n, 0, None)
        ch_linear = np.where(
            ch_n <= 0.003040, ch_n * 12.92, ch_n ** (1 / 2.4) * 1.055 - 0.055
        )
        return ch_linear * 255.0

    fixed_idx = ["Red", "Green", "Blue"].index(channel)
    free = [i for i in range(3) if i != fixed_idx]
    row_idx, col_idx = free

    row_axis = np.arange(256, dtype=np.float64)
    col_axis = np.arange(256, dtype=np.float64)

    # YIQ flip point: solve (fixed*w_f + row*w_r + col*w_c)/1000 = 128 for col
    col_yiq = (128000 - value * YIQ_W[fixed_idx] - row_axis * YIQ_W[row_idx]) / YIQ_W[
        col_idx
    ]

    # WCAG flip point: solve 0.2126*R_n + 0.7152*G_n + 0.0722*B_n = threshold for col
    fixed_n = srgb_normalize(np.array([value], dtype=np.float64))[0]
    row_n = srgb_normalize(row_axis)
    col_n_target = (
        WCAG_LUM_THRESHOLD - WCAG_W[fixed_idx] * fixed_n - WCAG_W[row_idx] * row_n
    ) / WCAG_W[col_idx]
    col_wcag = srgb_denormalize(col_n_target)

    # Disagreement = pixels between the two flip points
    low = np.minimum(col_yiq, col_wcag)
    high = np.maximum(col_yiq, col_wcag)
    disagree = (col_axis[np.newaxis, :] >= np.ceil(low[:, np.newaxis])) & (
        col_axis[np.newaxis, :] < np.ceil(high[:, np.newaxis])
    )

    # Build RGB image
    row_grid, col_grid = np.meshgrid(row_axis, col_axis, indexing="ij")
    channels = [None, None, None]
    channels[fixed_idx] = np.full_like(row_grid, value)
    channels[row_idx] = row_grid
    channels[col_idx] = col_grid
    img = np.stack(channels, axis=-1).astype(np.uint8)
    dimmed = (img * 0.3).astype(np.uint8)
    result_img = np.where(disagree[..., np.newaxis], img, dimmed)

    st.image(result_img, caption=f"{channel} = {value}", width=512)
