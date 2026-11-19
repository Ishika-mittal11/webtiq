from PIL import Image, ImageDraw, ImageFilter
import math, os

os.makedirs("bg", exist_ok=True)
W, H = 1920, 1080

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def diagonal(stops, path):
    """stops: list of (pos 0-1, (r,g,b)) along the diagonal."""
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        for x in range(0, W, 4):
            t = (x / W * 0.68 + y / H * 0.32)
            t = min(max(t, 0.0), 1.0)
            # find segment
            for i in range(len(stops) - 1):
                p0, c0 = stops[i]
                p1, c1 = stops[i + 1]
                if p0 <= t <= p1:
                    c = lerp(c0, c1, (t - p0) / (p1 - p0))
                    break
            else:
                c = stops[-1][1]
            for dx in range(4):
                if x + dx < W:
                    px[x + dx, y] = c
    img = img.filter(ImageFilter.GaussianBlur(2))
    img.save(path, quality=95)
    print("wrote", path)

# Title / closing: deep blue -> azure -> cyan
diagonal([(0.0, (11, 45, 107)), (0.45, (29, 111, 232)), (0.78, (34, 170, 226)), (1.0, (34, 211, 238))],
         "bg/bg_dark.jpg")

# Content: airy light gradient (blue -> lavender -> blush)
diagonal([(0.0, (233, 241, 255)), (0.5, (241, 237, 254)), (1.0, (253, 238, 246))],
         "bg/bg_light.jpg")

# Section divider: indigo -> violet
diagonal([(0.0, (23, 37, 84)), (0.5, (49, 46, 129)), (1.0, (109, 40, 217))],
         "bg/bg_section.jpg")
