def check_palindrom(text: str):
    # conver the text lower case
    t = text.lower()
    if t[::-1] == t:
        return True
    else:
        return False

a = check_palindrom('A man, a plan, a canal: Panama')
print(a)


