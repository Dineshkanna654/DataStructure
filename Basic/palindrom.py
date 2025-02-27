def palin(n: int):
    for i in range(1, n+1):
        if str(i) == str(i)[::-1]:
            print(i)


palin(1000)

