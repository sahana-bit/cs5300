
import math

#Returns positive/negative or zero for a given parameter
def PosNeg(value):
    if isinstance(value,int) or isinstance(value, float):
        if value<0:
            return "negative"

        elif value>0:
            return "positive"

        else:
            return "It's zero"
    else:
        return "Not a number"

#Returns sum of the first 100 numbers
def sumOnetoHundred():
    total=0
    for i in range(1,101):
      total = total+i
    return total

#Prints first 10 prime numbers
def printPrime():
    primes = []
    for i in range(2, 100):
        if len(primes) >= 10:
            break
        is_prime = True
        for j in range(2, int(math.sqrt(i)) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    print(primes)
            

