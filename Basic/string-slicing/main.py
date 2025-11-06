

# 1. Input: s = "python" → print first 3 letters.

def f3(txt):
	return txt[:3]

print(f"first 3 letter of python is {f3('python')}")

# 2. Print last 2 characters of "coding".

def l2(txt):
	return txt[-2:]

print(f"last 2 letter of coding is {l2('coding')}")

# 3. Get the string "din" from "dinesh" using slicing.

def slice1(txt):
	return txt[:3]

print(f"first 3 letter of dinesh is {slice1('dinesh')}")

# 4. Reverse the string "hello" using slicing.

def rev(txt):
	return txt[::-1]

print(f"The reverse string of [hello] is {rev('hello')}")

# 5 Print characters from index 1 to 4 of "developer".

def oneto4(txt):
	return txt[1:5]

print(f"index 1 to 4 of [developer] is {oneto4('developer')}")



