# methods 1

def sum_of_n(n):
    return n * (n + 1) // 2

print(sum_of_n(10))

# method 2
def sum_of_n2(n):
    for i in range(n):
        n = n + i
    return n

print(sum_of_n2(10))

#method 3

def sumRec(n):
    sum = 0
    if n == 0:
        return 0
    return n + sumRec(n - 1)

print(sumRec(10))
    
    
