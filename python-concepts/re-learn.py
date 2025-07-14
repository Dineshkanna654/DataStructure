import re

# pattern = r'\d{3}-\d{3}-\d{4}'
# text = "Call me at 987-654-3210"
# match = re.search(pattern, text)

# if match:
#     print("Found:", match.group())

#  return the text after the 'URL' keyword
def find_after_url(text):
    url_pattern = r'URL:\s*(.*)'
    match = re.search(url_pattern, text)
    if match:
        return match.group(1)

# print(find_after_url('URL:wwww.com'))

t = 'hhh okkk llll dddd'

x = re.search('/d', t)
print(x.start())