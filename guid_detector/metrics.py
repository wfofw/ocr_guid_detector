from collections import Counter


def hamming(a: str, b: str) -> int:
    """Counts how many positions the strings differ in (for GUIDs the length is the same)."""
    return sum(c1 != c2 for c1, c2 in zip(a, b))

def merge_similar_guid_counts(counts, max_dist=3, min_total=2):
    """
    counts: Counter({guid: cnt}) / dict / iterable guides / single line.
    Returns a set with guides after Hamming gluing.
    """

    if not counts:
        return set()
    
    if not hasattr(counts, "items"):
        counts = Counter(counts)

    # Single line - just return it
    if isinstance(counts, str):
        return {counts}

    items = list(counts.items())  # [(guid, cnt), ...]
    n = len(items)
    used = [False] * n
    result = set()

    for i in range(n):
        if used[i]:
            continue

        guid_i, cnt_i = items[i]
        total = cnt_i
        best_guid = guid_i
        best_cnt = cnt_i

        for j in range(i + 1, n):
            if used[j]:
                continue
            guid_j, cnt_j = items[j]

            if len(guid_i) != len(guid_j):
                continue

            if hamming(guid_i, guid_j) <= max_dist:
                used[j] = True
                total += cnt_j
                if cnt_j > best_cnt:
                    best_cnt = cnt_j
                    best_guid = guid_j

        if total >= min_total:
            result.add(best_guid)

    # If we threw everything out, let's at least return the ones that are used most often
    if not result:
        max_cnt = max(cnt for _, cnt in items)
        for g, c in items:
            if c == max_cnt:
                result.add(g)

    return result