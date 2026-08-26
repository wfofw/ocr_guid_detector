from guid_detector.metrics import hamming, merge_similar_guid_counts
from guid_detector.processing import build_one_guid_from_lines


def test_hamming():
    # Identical lines -> 0 errors
    assert hamming("12345", "12345") == 0
    # The difference is one character (OCR mixed up f and e)
    assert hamming("1234f", "1234e") == 1

def test_merge_similar_guid_counts():
    raw_guids = [
        "12345678-1234-11f0-1234-123456789abc",
        "12345678-1234-11f0-1234-123456789abe",  # difference by 1 character
        "12345678-1234-11f0-1234-123456789abc",
    ]
    # Should merge broken lines and return the correct GUID
    result = merge_similar_guid_counts(raw_guids, max_dist=2, min_total=2)
    assert "12345678-1234-11f0-1234-123456789abc" in result

def test_build_one_guid_from_lines():
    # Simulation of OCR fragments from different passes
    ocr_lines = [
        "12345678-1234-11f0-1234-123456789abc",
        "12345678-1234-11f0-1234-123456789abe",
        "12345678-1234-11f0-1234-123456789abc"
    ]
    candidate = build_one_guid_from_lines(ocr_lines)
    assert candidate == "12345678-1234-11f0-1234-123456789abc"