def count_occurrence(text: str):
    return {letter: text.count(letter) for letter in text}

a = count_occurrence('hello')
print(a)    
