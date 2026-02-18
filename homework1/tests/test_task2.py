import pytest
from src.task2 import checkDataType

#Parametrized test for datatype
@pytest.mark.parametrize("value, expected", [
    (10, "integer"),
    (3.14, "float"),
    ("hello", "string"),
    (True, "boolean"),
    ([1, 2], "Function doesn't recognize data type.")
])
def test_check_data_type(value, expected):
    assert checkDataType(value) == expected
