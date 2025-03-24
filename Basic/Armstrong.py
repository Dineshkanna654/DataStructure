
def Arm(n):
    num_list = [int(num)**3 for num in str(n)]
    print(num_list)
    sum = 0
    print(num_list)
    for i in num_list:
        sum = sum + i
    if sum == n:
        return f"This is Armstrong Number"
    else:
        return "Not a Armstrong"


a = Arm(153)
print(a)
