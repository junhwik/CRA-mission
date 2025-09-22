import pytest
import attendance

def test_print_result(capsys):
    attendance_list = attendance.input_file()
    attendance.analyze_attendance(attendance_list)

    with open("expected_result.txt", "r") as f:
        expected = f.read()
    captured = capsys.readouterr()

    assert captured.out == expected