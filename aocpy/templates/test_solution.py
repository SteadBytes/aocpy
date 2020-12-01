#!/usr/bin/python
import pytest
import solution

@pytest.mark.parametrize('data,expect',
    [('sample_input_1', 'sample_output_1'),
     ('sample_input_2', 'sample_output_2')]
)
def test_part_1(data, expect):
    assert solution.part_1(data) == expect

@pytest.mark.parametrize('data,expect', 
    [('sample_input_1', 'sample_output_1'),
     ('sample_input_2', 'sample_output_2')]
)
def test_part_2(data, expect)
    assert solution.part_2(data) == expect

