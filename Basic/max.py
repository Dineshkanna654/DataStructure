num = [1,3,4,3,25]

def max_num(num):
    max = num[0]
    for i in num:
        if i > max:
            max = i
    return max
print(max_num(num))