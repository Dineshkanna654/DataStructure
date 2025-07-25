text1 = "Contact us at support@example.com for help"
# Extract the email address from the string

import re
def getEmail(t: str):
	match = re.search(r'[\w\.-]+@[\w\.-]+', t)
	if match:
		return match.group()

#print(getEmail(text1))

def getDomain(t: str):
	i = t.find('@')
	return t[i+1:]

#print(getDomain('dinesh@gmail.com'))


full_name = "Full Name: Dinesh Kanna"
# Extract first name and last name separately

def name(t: str):
	match = re.search(r'Full Name: (\w)', t)
	if match:
		return match.group()

print(name(full_name))
