import pytest

from ..config import deep_merge_dicts


def test_deep_merging_dicts():
    dict_a = {
        "number": 123,
        "string": "bravo",
        "list": [1, 2, "s"],
        "list2": [],
        "dict": {"number": 123, "otherlist": [1], "subdict": {"foo": "bar"}},
    }

    dict_b = {
        "string": "new bravo",
        "list": ["new item"],
        "dict": {
            "otherlist": ["another item"],
            "subdict": {"foo": "new bar", "new field": True},
        },
    }

    expected_dict = {
        "number": 123,
        "string": "new bravo",
        "list": [1, 2, "s", "new item"],
        "list2": [],
        "dict": {
            "number": 123,
            "otherlist": [1, "another item"],
            "subdict": {"foo": "new bar", "new field": True},
        },
    }

    assert deep_merge_dicts(dict_a, dict_b) == expected_dict


def test_fails_on_types_mismatch():
    dict_a = {"number": 123}
    dict_b = {"number": "new bravo"}

    with pytest.raises(ValueError):
        deep_merge_dicts(dict_a, dict_b)
