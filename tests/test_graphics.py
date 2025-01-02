"""
RGB Multitool Tests - Graphics - Icon, Network
"""

import imagehash
import pytest
from rgbmultitool import graphics


REF_HASHES = {
    'icon_network': [
        "3c3c3c3c3c000000", # False False
        "3c3c3c3c3c1818ff", # True False
        "3c3c3c3c3c000000", # False True. Should be the same as False False.
        "3c3c3c3c3c1899ff" # True True
    ]
}

@pytest.mark.parametrize(
    "net, mqtt, ref_hash",
    [
        pytest.param(False, False, "3c3c3c3c3c000000", id="FF"),
        pytest.param(True, False, "3c3c3c3c3c1818ff", id="TF"),
        pytest.param(False, True, "3c3c3c3c3c000000", id="FT"),
        pytest.param(True, True, "3c3c3c3c3c1899ff", id="TT")
    ])
def test_icon_network_statuses(net, mqtt, ref_hash):
    assert imagehash.average_hash(graphics.icon_network(net, mqtt)) == imagehash.hex_to_hash(ref_hash)
