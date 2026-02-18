from src.task1 import printHelloWorld

#Checks if Hello World is printed
def test_print_hello_world(capsys):
    printHelloWorld()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"