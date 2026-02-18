import pytest
from pathlib import Path
from src.task6 import countWords

#Checks word count in task6_read_me.txt
@pytest.mark.parametrize("expected", [104])
def test_countWords_real_readme(expected):
    filename = "task6_read_me.txt"
    assert countWords(filename) == expected

#parametrized test and robust I/O test
@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello world", 2),    
        ("Hello world\nThis is pytest", 5),
        ("123 456", 0),
        ("mix 123 mix", 2),
        ("", 0),
    ],
)
def test_countWords_temp_files(tmp_path, text, expected):
    f = tmp_path / "sample.txt"
    f.write_text(text, encoding="utf-8")
    assert countWords(f) == expected


@pytest.mark.parametrize("bad_name", ["missing.txt", "nope/also_missing.txt"])
def test_countWords_file_not_found(tmp_path, bad_name):
    missing = tmp_path / bad_name
    with pytest.raises(FileNotFoundError):
        countWords(missing)
