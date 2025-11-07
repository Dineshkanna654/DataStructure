# 1. Write a program to get every 2nd character of a string → s[::2]

def every2nd(txt):
	return txt[::2]

print(every2nd('kakakaka'))

# 2. Slice "datascience" into two halves using slicing.

def half(txt):
	l = len(txt)
	print(txt[:l//2])
	print(txt[l//2:])

half('datascience')
