
num = [2,4,2,4,6,71,2,4,9,6,0]

print("1", list(set(num)))

unique_num= []
for item in num:
    Found = False
    for uq in unique_num:
        if item == uq:
            Found = True
            break
    if not Found:
        unique_num.append(item)
print("2", unique_num)

for i in num:
    if i not in unique_num:
        unique_num.append(i)
print("3", unique_num)
    
