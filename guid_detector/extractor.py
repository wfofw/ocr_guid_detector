import re
import time
from collections import Counter

import pytesseract
from PIL import Image

from guid_detector.metrics import merge_similar_guid_counts
from guid_detector.patterns import GUID_STRICT
from guid_detector.processing import (
    build_one_guid_from_lines,
    preprocess_image,
)


def find_guids_by_stripes(img: Image.Image):
    start_time = time.time()

    W, H = img.size
    window_h = 100
    overlap = 50
    step = window_h - overlap

    # Modes for different situations
    scales = [4, 8, 10]
    psms = [3]
    thresholds = [180, 190, 200, 210] #180, 190, 200, 210
    inverts = [False]

    num_stripes = 0
    y_tmp = 0
    while y_tmp < H:
        num_stripes += 1
        y_tmp += step

    total_steps = num_stripes * len(scales) * len(thresholds) * len(inverts) * len(psms)
    current_step = 0

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

                        current_step += 1
                        
                        # Calculating seconds and speed
                        elapsed = time.time() - start_time
                        speed = current_step / elapsed if elapsed > 0 else 0
                        remaining_steps = total_steps - current_step
                        eta = max(0.0, remaining_steps / speed) if speed > 0 else 0
                        percent = min(100.0, round((current_step / total_steps) * 100, 1))

                        # Sending an extended progress event
                        yield {
                            "type": "progress",
                            "current": current_step,
                            "total": total_steps,
                            "percent": percent,
                            "elapsed_seconds": round(elapsed, 0),
                            "eta_seconds": round(eta, 0),
                            "speed_steps_per_sec": round(speed, 2),
                        }

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

    total_time = round(time.time() - start_time, 2)

    yield {
        "type": "result",
        "count": len(guids),
        "guids": sorted(guids),
        "total_time_seconds": total_time,
    }