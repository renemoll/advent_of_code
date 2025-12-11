def merge_overlapping_ranges(ranges: list[range]) -> list[range]:
    """Merge overlapping ranges into non-overlapping ranges.

    Args:
        ranges (list[range]): List of ranges to merge.

    Returns:
        list[range]: Merged list of non-overlapping ranges.
    """
    if not ranges:
        return []

    ranges.sort(key=lambda r: r.start)

    result = []
    for r in ranges:
        if not result or r.start > result[-1].stop:
            result.append(r)
        else:
            result[-1] = range(result[-1].start, max(result[-1].stop, r.stop))
    return result
