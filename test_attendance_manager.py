import pytest
from attendance import AttendanceManager
import subprocess

@pytest.fixture
def attendance_manager():
    AttendanceManager().clear()
    attendance_manager = AttendanceManager()
    return attendance_manager


def test_print_result(capsys, attendance_manager):
    attendance_manager.analyze()

    with open("expected_result.txt", "r") as f:
        expected = f.read()
    captured = capsys.readouterr()

    assert captured.out == expected

def test_print_singleton_reset(capsys, attendance_manager):
    attendance_manager.analyze()

    with open("expected_result.txt", "r") as f:
        expected = f.read()
    captured = capsys.readouterr()

    assert captured.out == expected


def test_error_file(capsys, attendance_manager):
    attendance_manager._input_file(list_file="error path")
    expected = "파일을 찾을 수 없습니다.\n"
    captured = capsys.readouterr()
    assert captured.out == expected


def test_valid_attendance_history_length(attendance_manager):
    test_string = "invalid length history"
    test_parts = test_string.split()
    assert attendance_manager._is_valid(test_parts) == False


def test_valid_attendance_history_weekday(attendance_manager):

    test_string = "invalid weekday"
    test_parts = test_string.split()
    assert attendance_manager._is_valid(test_parts) == False


def test_valid_attendance_skip(mocker, attendance_manager):
    mocker.patch('attendance.AttendanceManager._is_valid', return_value=False)
    attendance_manager.analyze()
    assert len(attendance_manager.club_members) == 0

