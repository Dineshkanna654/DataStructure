"""Create a program to find if a number is even or odd and return "Even" or "Odd" accordingly without moduls."""

def even_or_odd(n):
    if n & 1:
        return 'Odd'
    return 'Even'

print(even_or_odd(5))
print(even_or_odd(4))