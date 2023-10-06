import pytest

from batch_file_rename import utils

def test_color_string():
    assert(utils.color_string('y', 'test string') == "\033[33mtest string\033[0m")

def test_paginate_list():
    lst = ['item 1', 'item 2', 'item 3', 'item 4', 'item 5']
    result = list(utils.paginate_list(lst, 2))
    assert len(result) == 3
    assert result[0] == ['item 1', 'item 2']
    assert result[1] == ['item 3', 'item 4']
    assert result[2] == ['item 5']