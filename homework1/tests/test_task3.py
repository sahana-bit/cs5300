from src.task3 import PosNeg, sumOnetoHundred, printPrime

def test_PosNeg_positive():
    assert PosNeg(5) == "positive"
    assert PosNeg(2.5) == "positive"


def test_PosNeg_negative():
    assert PosNeg(-3) == "negative"
    assert PosNeg(-0.01) == "negative"


def test_PosNeg_zero():
    assert PosNeg(0) == "It's zero"
    assert PosNeg(0.0) == "It's zero"


def test_PosNeg_not_a_number():
    assert PosNeg("5") == "Not a number"
    assert PosNeg(None) == "Not a number"


def test_sumOneToHundred():
    assert sumOnetoHundred() == 5050


def test_printPrime_output(capsys):
    printPrime()
    captured = capsys.readouterr()
    assert captured.out.strip() == "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]"
