def check_palindrom(text: str):
    if text[::-1] == text:
        return True
    else:
        return False

a = check_palindrom('elkdmekwm')
print(a)


