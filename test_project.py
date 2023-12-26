import pytest
from unittest.mock import patch, Mock
from itertools import cycle
from project import get_valid_team_name, get_sprint_details

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

def test_get_sprint_details_valid_input():
    with patch('builtins.input', side_effect=['2023-01-01', '10', '14']):
        result = get_sprint_details(1, [])
        assert result == {
            'sprint_start_date': '2023-01-01',
            'sprint_throughput': 10,
            'sprint_duration': 14
        }

def test_get_sprint_details_invalid_date_then_valid_input():
    with patch('builtins.input', side_effect=['invalid_date', '2023-01-01', '10', '14']):
        result = get_sprint_details(1, [])
        assert result == {
            'sprint_start_date': '2023-01-01',
            'sprint_throughput': 10,
            'sprint_duration': 14
        }

def test_get_sprint_details_invalid_throughput_then_valid_input():
    with patch('builtins.input', side_effect=['2023-01-01', 'invalid_throughput', '10', '14']):
        result = get_sprint_details(1, [])
        assert result == {
            'sprint_start_date': '2023-01-01',
            'sprint_throughput': 10,
            'sprint_duration': 14
        }

def test_get_sprint_details_invalid_duration_then_valid_input():
    with patch('builtins.input', side_effect=['2023-01-01', '10', 'invalid_duration', '14']):
        result = get_sprint_details(1, [])
        assert result == {
            'sprint_start_date': '2023-01-01',
            'sprint_throughput': 10,
            'sprint_duration': 14
        }

def test_get_sprint_details_overlap_existing_sprints():
    existing_sprints = [
        {'sprint_start_date': '2023-01-05', 'sprint_duration': 7},
        {'sprint_start_date': '2023-01-20', 'sprint_duration': 14}
    ]

    with patch('builtins.input', side_effect=['2023-01-10', '10', '14']):
        result = get_sprint_details(3, existing_sprints)
        assert result is None  # Expecting None due to overlap

def test_get_sprint_details_invalid_date_format_then_valid_input():
    with patch('builtins.input', side_effect=['invalid_date_format', '2023-01-01', '10', '14']):
        result = get_sprint_details(1, [])
        assert result == {
            'sprint_start_date': '2023-01-01',
            'sprint_throughput': 10,
            'sprint_duration': 14
        }