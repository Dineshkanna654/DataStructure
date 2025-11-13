import requests

# 1. Error Handling Practice

# Try to GET data from a wrong URL like https://jsonplaceholder.typicode.com/postsss

# Use try-except and response.raise_for_status() to handle errors.


def Q1(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"Other error occurred: {err}"
    
# Example usage:
# print(Q1("https://jsonplaceholder.typicode.com/postsss"))


# 2. Download an Image Using Requests

# Download any image from https://picsum.photos/200

# Save it as random_image.jpg on your computer.

def Q2(image_url, save_path):
    try:
        res = requests.get(image_url)
        res.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(res.content)
        return f"Image successfully downloaded: {save_path}"
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"Other error occurred: {err}"
    
# Example usage:
print(Q2("https://picsum.photos/200", "random_image.jpg"))

