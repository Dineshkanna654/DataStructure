# Create a function that counts the occurrence of each character in a string. Example: "hello" → {'h': 1, 'e': 1, 'l': 2, 'o': 1}
def T2obj(text: str):
    obj = {}
    for letter in text:
        count = text.count(letter)
        obj[letter] = count
    return obj

a = T2obj('hello')
print(a)


# Dictionary comprehension way
text = 'Dineshkanna'
objs = {letter: text.count(letter) for letter in text}
print(objs)
