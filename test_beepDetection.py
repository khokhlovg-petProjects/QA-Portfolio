def match_found(expected_frequencies: list, detected_frequencies: list) -> bool:
    for frequency in expected_frequencies:
        if frequency in detected_frequencies:
            return True
    return False


def test_match_found_when_overlap_exists():
    expected = [915, 1371, 1777]
    detected = [1371, 2000]
    assert match_found(expected, detected) is True


def test_match_found_when_no_overlap():
    expected = [915, 1371, 1777]
    detected = [100, 200]
    assert match_found(expected, detected) is False


def test_match_found_with_empty_detected_list():
    expected = [915, 1371, 1777]
    detected = []
    assert match_found(expected, detected) is False
