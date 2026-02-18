#Prints the first 3 elements of list
def listBooks(fav=None):
    if fav is None:
       fav = ["The poppy war, RF Kuang", "Angels & Demons, Dan Brown", "Doctors, Erich Segal","Sandstorm, James Rollins"]
    print(fav[0:3:1])

#Returns dictionary with student information
def dictDB():
    studentDB = {"June": "111001", "May":"111002", "Jenny":"111003","Viola":"111004"}
    return studentDB


