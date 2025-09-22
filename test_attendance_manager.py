import pytest
import attendance

def test_print_result(capsys):

    attendance.input_file()
    with open("expected_result.txt", "r") as f:
        expected = f.read()
    captured = capsys.readouterr()

    assert captured.out == expected