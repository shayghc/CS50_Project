import pytest
from unittest.mock import patch, Mock
from itertools import cycle
from project import get_valid_team_name

def custom_input(values):
    iterator = cycle(values)
    def side_effect(*args, **kwargs):
        return next(iterator)
    return Mock(side_effect=side_effect)

def test_get_valid_team_name_correct_input():
    with patch('builtins.input', custom_input(['TeamName', 'Y'])):
        assert get_valid_team_name() == 'TeamName'

def test_get_valid_team_name_blank_input_then_correct_input():
    with patch('builtins.input', custom_input(['', 'TeamName', 'Y'])):
        assert get_valid_team_name() == 'TeamName'

def test_get_valid_team_name_incorrect_confirmation_then_correct_input():
    with patch('builtins.input', custom_input(['TeamName', 'N', 'TeamName', 'Y'])):
        assert get_valid_team_name() == 'TeamName'

def test_get_valid_team_name_blank_input_then_incorrect_confirmation_then_correct_input():
    with patch('builtins.input', custom_input(['', 'TeamName', 'N', 'TeamName', 'Y'])):
        assert get_valid_team_name() == 'TeamName'