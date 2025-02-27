def check_palin(text: str):
    if text[::-1] == text:
        return True
    else:
        return False

a = check_palin('elkdmekwm')
print(a)


