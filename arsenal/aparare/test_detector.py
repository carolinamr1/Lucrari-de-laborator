from collections import Counter

import pytest

from arsenal.aparare.detector import suspecti


def test_pragul_taie():
    counts = Counter({"a": 13, "b": 2})
    assert suspecti(counts, 10) == [("a", 13)]


def test_prag_invalid():
    with pytest.raises(ValueError):
        suspecti({}, 0)
