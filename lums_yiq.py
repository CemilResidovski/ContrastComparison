import json
from collections import defaultdict


def get_color(lum):
    return ("black", round(lum, 2)) if (lum >= 128) else ("white", round(lum, 2))


lums = defaultdict(lambda: defaultdict(dict))

for r in range(256):
    for g in range(256):
        for b in range(256):
            lum = (r * 299 + g * 587 + b * 114) / 1000
            lums[r][g][b] = get_color(lum)

with open("result_yiq.json", "w") as f:
    json.dump(lums, f)
