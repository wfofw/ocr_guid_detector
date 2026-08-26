import re

guid_regex = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-11f0-[0-9a-f]{4}-[0-9a-f]{12}",
    re.IGNORECASE
)

GUID5_ANY = re.compile(
    r"\b([0-9a-f]{6,8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{3,4})-([0-9a-f]{11,12})\b",
    re.IGNORECASE
)

GUID_STRICT = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    re.IGNORECASE
)