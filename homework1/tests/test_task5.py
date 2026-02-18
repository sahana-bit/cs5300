from src.task5 import listBooks, dictDB

#checks if first 3 elements are printed
def test_listBooks_default(capsys):
    listBooks()
    captured = capsys.readouterr()
    assert captured.out.strip() == "['The poppy war, RF Kuang', 'Angels & Demons, Dan Brown', 'Doctors, Erich Segal']"


def test_listBooks_custom(capsys):
    books = ["A", "B", "C", "D"]
    listBooks(books)
    captured = capsys.readouterr()
    assert captured.out.strip() == "['A', 'B', 'C']"


def test_dictDB_type():
    result = dictDB()
    assert isinstance(result, dict)


def test_dictDB_contents():
    result = dictDB()
    assert result["June"] == "111001"
    assert result["May"] == "111002"
