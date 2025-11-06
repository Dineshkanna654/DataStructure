# 1. Check if a string is a palindrome using slicing (s == s[::-1]).

def palin(txt):
	print("Input:" , txt)
	if txt == txt[::-1]:
		print('palindrom')
	else:
		print("Not palindrom")

palin('madam')

# 2. Remove the first and last character of a string using slicing.

def rm1stAndLast(txt):
	return txt[1:-1]

print(rm1stAndLast("qdineshq"))

# 3. Given s = "programming", extract "gram".

def ext(txt):
	return txt[3:7]


print(ext("programming"))
