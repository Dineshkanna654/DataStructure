
import requests

'''
1. https://httpbin.org/status/404

{
    "title": "My Post",
    "body": "Learning requests library",
    "userId": 101
}

Print the returned response (ID, title, etc.)'''

def Q1(url, data):
	res = requests.post(url, json=data)
	if res.status_code == 200 or res.status_code == 201:
		print(res.json())
	else:
		print(f"Error: {res.status_code}")


# Q1('https://httpbin.org/status/404', { "title": "My Post", "body": "Learning requests library", "userId": 101 })

''' 
2. Send Query Parameters

Fetch comments only for postId=1:
https://jsonplaceholder.typicode.com/comments?postId=1

Print the names of the first 5 commenters.

'''

def Q2(url, postId):
	res = requests.get(url=url, params={"page": 1, "limit": 5}).json()
	postIdOne = []
	for comment in res:
		if comment["postId"] == postId:
			postIdOne.append(comment)
	return postIdOne[:5]

print(Q2('https://jsonplaceholder.typicode.com/comments', postId=1))
