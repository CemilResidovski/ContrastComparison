import numpy as np

YIQ_W = [299, 587, 114]  # R, G, B
WCAG_W = [0.2126, 0.7152, 0.0722]

# Raw luminance threshold for WCAG contrast ratio of 4.5:1, from the contrast ratio formula.
# Used for the "decision boundary" between black and white text in WCAG.
# Assuming black or white foreground text color, a ratio of 4.5:1 will always be met.
WCAG_LUM_THRESHOLD = np.sqrt(0.0525) - 0.05

CHANNEL_NAMES = ["Red", "Green", "Blue"]


# This is the same method used in wcag.py, but easier and faster to scale for the whole color space.
def srgb_normalize(ch):
    ch_n = ch / 255.0
    return np.where(ch_n <= 0.03928, ch_n / 12.92, ((ch_n + 0.055) / 1.055) ** 2.4)


def srgb_denormalize(ch_n):
    ch_n = np.clip(ch_n, 0, None)
    ch_linear = np.where(
        ch_n <= 0.003040, ch_n * 12.92, ch_n ** (1 / 2.4) * 1.055 - 0.055
    )
    return ch_linear * 255.0


def compute_disagreement(channel, value, scale=2):
    """Compute a visualization of where WCAG and YIQ disagree for a color space slice.

    Args:
        channel: "Red", "Green", or "Blue" — the fixed channel.
        value: 0–255 value for the fixed channel.
        scale: nearest-neighbor upscale factor for crisp rendering.

    Returns:
        image: uint8 numpy array (256*scale, 256*scale, 3).
        row_label: name of the row (Y-axis) channel.
        col_label: name of the column (X-axis) channel.
        disagree_count: number of disagreeing pixels.
        disagree_pct: percentage of disagreeing pixels.
    """
    fixed_idx = CHANNEL_NAMES.index(channel)
    free = [i for i in range(3) if i != fixed_idx]
    row_idx, col_idx = free

    row_axis = np.arange(256, dtype=np.float64)
    col_axis = np.arange(256, dtype=np.float64)

    # The disagreement region is always a contiguous band along the free channel axis.
    # Instead of evaluating every pixel, analytically solve each algorithm's flip point.

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

    # Upscale with nearest-neighbor so pixels stay crisp instead of blurry
    if scale > 1:
        result_img = np.repeat(np.repeat(result_img, scale, axis=0), scale, axis=1)

    disagree_count = int(disagree.sum())
    disagree_pct = 100 * disagree_count / disagree.size

    return (
        result_img,
        CHANNEL_NAMES[row_idx],
        CHANNEL_NAMES[col_idx],
        disagree_count,
        disagree_pct,
    )
