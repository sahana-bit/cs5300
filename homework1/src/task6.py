from pathlib import Path
#returns number of words in a file
def countWords(flname):
    path = Path(flname)
    if not path.is_file():
        raise FileNotFoundError(f"{flname} not found")
    with path.open("r", encoding="utf-8") as fl:
       words = [word for line in fl for word in line.strip().split() if word.isalpha()]
    wordCount = len(words)
    return wordCount
    
#print(countWords("/home/student/cs5300/homework1/task6_read_me.txt"))