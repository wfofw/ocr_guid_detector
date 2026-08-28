from collections import Counter

from PIL import Image, ImageOps

from guid_detector.patterns import GUID_STRICT


def preprocess_image(img: Image.Image, scale=2, threshold=None, invert=False):
    w, h = img.size
    img = img.resize((w * scale, h * scale), Image.Resampling.LANCZOS)
    img = img.convert("L")

    if invert:
        img = ImageOps.invert(img)

    if threshold is not None:
        img = img.point(lambda p: 255 if p > threshold else 0, mode="L")

    return img

def build_one_guid_from_lines(lines: list[str]):
    c1_8 = Counter()  # g1 length 8
    c2_4 = Counter()  # g2 length 4
    c3_4 = Counter()  # g3 length 4
    c4_4 = Counter()  # g4 length 4
    c5_12= Counter()  # g5 length 12

    for s in lines:
        if not s:
            continue
        token = s.strip().lower()
        parts = token.split("-")
        if len(parts) != 5:
            continue

        g1, g2, g3, g4, g5 = parts

        if len(g1) == 8:  c1_8[g1] += 1
        if len(g2) == 4:  c2_4[g2] += 1
        if len(g3) == 4:  c3_4[g3] += 1
        if len(g4) == 4:  c4_4[g4] += 1
        if len(g5) == 12: c5_12[g5] += 1

    # If there is not at least one "correct length" for critical groups, we do not guess
    if not (c1_8 and c2_4 and c3_4 and c4_4 and c5_12):
        return None

    g1 = c1_8.most_common(1)[0][0]
    g2 = c2_4.most_common(1)[0][0]
    g3 = c3_4.most_common(1)[0][0]
    g4 = c4_4.most_common(1)[0][0]
    g5 = c5_12.most_common(1)[0][0]

    candidate = f"{g1}-{g2}-{g3}-{g4}-{g5}"
    return candidate if GUID_STRICT.fullmatch(candidate) else None