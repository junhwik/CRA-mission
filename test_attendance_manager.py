import pytest
from attendance import AttendanceManager

def test_print_result(capsys):
    attendance_manager = AttendanceManager()
    attendance_manager.analyze()

    with open("expected_result.txt", "r") as f:
        expected = f.read()
    captured = capsys.readouterr()

    assert captured.out == expected