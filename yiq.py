# https://24ways.org/2010/calculating-color-contrast

# In YIQ, Y represents luminance and hence is the only relevant thing here.


def getContrastColor(bg_color):
    bg_color = [int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:], 16)]

    y = 0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2]

    # Calculate contrast with white (Y = 1.0)
    contrast_with_white = abs(1.0 - y)

    # Calculate contrast with black (Y = 0.0)
    contrast_with_black = abs(0.0 - y)

    # Choose the color with the highest contrast
    return ["white", y] if (contrast_with_white > contrast_with_black) else ["black", y]
