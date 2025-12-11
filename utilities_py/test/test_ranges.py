from utilities_py import merge_overlapping_ranges


def test_merge_overlapping_ranges():
    """Verify that overlapping ranges are merged."""

    # 1. Prepare
    input_ranges = [
        range(1, 5),
        range(10, 15),
        range(3, 7),
        range(20, 25),
        range(12, 18),
        range(30, 35),
    ]

    # 2. Execute
    result = merge_overlapping_ranges(input_ranges)

    # 3. Verify
    expected_ranges = [
        range(1, 7),
        range(10, 18),
        range(20, 25),
        range(30, 35),
    ]

    assert result == expected_ranges
