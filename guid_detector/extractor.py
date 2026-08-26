import re
from collections import Counter

import pytesseract
from PIL import Image

from guid_detector.metrics import merge_similar_guid_counts
from guid_detector.patterns import GUID_STRICT
from guid_detector.processing import (
    build_one_guid_from_lines,
    preprocess_image,
)


def crop_message_id_column(img, margin_x=20, offset_top=5, offset_bottom=5):
    """
    Searches for the word "message_id" in the screenshot and cuts out the column below it..
    Returning (crop_img, bbox), where bbox = (left, top, right, bottom).
    """
    # 1. OCR with coordinates
    data = pytesseract.image_to_data(
        img,
        lang="eng",
        config="--oem 3 --psm 6 -c user_defined_dpi=300",
        output_type=pytesseract.Output.DICT,
    )

    # 2. We are looking for a cell with the text message_id (case-insensitive)
    target_idx = None
    for i, txt in enumerate(data["text"]):
        if txt and txt.strip().lower() == "message_id":
            target_idx = i
            break

    if target_idx is None:
        return None

    x = data["left"][target_idx]
    y = data["top"][target_idx]
    w_box = data["width"][target_idx] + 35
    h_box = data["height"][target_idx]

    # 3. We construct the column boundaries along X
    left = max(0, x - margin_x)
    right = min(img.size[0], x + w_box + margin_x)

    # In Y - from the bottom of the title to the bottom of the picture
    top = min(img.size[1], y + h_box + offset_top)
    bottom = img.size[1] - offset_bottom

    crop_box = (left, top, right, bottom)
    crop_img = img.crop(crop_box)

    return crop_img


def find_guids_by_stripes(img: Image.Image, crop: int = 0):
    W, H = img.size
    window_h = 100
    overlap = 50
    step = window_h - overlap

    # Modes for different situations
    if crop:
        # The message_id column has already been removed, but you can upscale it more aggressively.
        scales = [8, 9, 10, 11]
        psms = [3]
        thresholds = [x for x in range(182, 198, 4)]
    else:
        # The overall screen is softer
        scales = [4, 8, 12, 16]
        psms = [3]
        thresholds = [140, 180, 220] #180, 190, 200, 210

    inverts = [False, True]

    y = 0
    guids = set()
    while y < H:
        top = y
        bottom = min(H, y + window_h)
        stripe = img.crop((0, top, W, bottom))
        guid_counts = Counter()
        all_txt_found = []
        for scale in scales:
            for thr in thresholds:
                for inv in inverts:
                    stripe_prep = preprocess_image(stripe, scale=scale, threshold=thr, invert=inv)
                    for psm in psms:
                        config_guid = (
                            "--oem 1 "
                            f"--psm {psm} "
                            "-c tessedit_char_whitelist=0123456789abcdef- "
                            "-c user_defined_dpi=300"
                        )
                        txt = pytesseract.image_to_string(stripe_prep, config=config_guid)
                        txt = (
                            txt.replace("-\n", "-")
                            .replace("\n", " ")
                            .replace("—", "-")
                            .replace("–", "-")
                        )
                        for g in re.findall(GUID_STRICT, txt):
                            guid_counts[g.lower()] += 1

                        all_txt_found.append(txt)

        cand = build_one_guid_from_lines(all_txt_found)
        if cand:
            guid_counts[cand.lower()] += 4

        merged_guids = merge_similar_guid_counts(
            guid_counts,
            max_dist=3,
            min_total=4,
        )

        guids.update(merged_guids)
        y += step

    guids = merge_similar_guid_counts(
        guids,
        max_dist=1,
        min_total=1,
    )

    return guids
