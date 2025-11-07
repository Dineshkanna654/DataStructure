
import requests
import json

'''
1. Use requests.get() to fetch data from https://jsonplaceholder.typicode.com/posts/1
Print the status code and response JSON
'''

def Q1(url):
	res = requests.get(url)
	print("Status Code:", res.status_code)
	print("Response JSON:", res.json())
# Q1("https://jsonplaceholder.typicode.com/posts/1")


# List All Posts

# Get all posts from https://jsonplaceholder.typicode.com/posts

# Print the titles of the first 10 posts.

def Q2(url):
	res = requests.get(url).json()
	print("Title od first 10 posts")
	for post in res[:10]:
		print("Title:", post['title'])
# Q2('https://jsonplaceholder.typicode.com/posts')


# Make a request to https://httpbin.org/status/200

# Then make another request to https://httpbin.org/status/404

# Use response.ok and response.status_code to check success or failure.

def Q3(url1, url2):
	res1 = requests.get(url1)
	res2 = requests.get(url2)
	print("res1 status", res1.status_code, res1.ok)
	print("res2 status", res2.status_code, res2.ok)

Q3('https://httpbin.org/status/200', 'https://httpbin.org/status/404')
