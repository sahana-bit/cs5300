from src.task4 import calculate_discount


def test_discount_integers():
    assert calculate_discount(100, 50) == 50


def test_discount_floats():
    assert calculate_discount(200.0, 5.0) == 190.0


def test_mixed_types():
    assert calculate_discount(150, 10.0) == 135.0
    assert calculate_discount(150.0, 10) == 135.0


def test_invalid_price():
    assert calculate_discount("678", 10) == "invalid data type for price"


def test_invalid_discount():
    assert calculate_discount(678, "10") == "invalid data type for discount"
