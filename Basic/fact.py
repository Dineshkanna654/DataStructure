
def factorialN(n):
    fact = 1
    if n == 0:
        return 1
    for i in range(1, n+1):
        fact *= i
    return fact

def factoRec(n):
    if n == 0 or n == 1:
        return 1
    print(factoRec(n - 1))
    return n * factoRec(n - 1)
    

n = int(input("Enter the Number: "))


a = factoRec(n)
