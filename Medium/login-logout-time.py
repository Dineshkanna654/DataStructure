#Design a Python class called UserActivityTracker to track login/logout times for users and calculate their total session duration.

from datetime import datetime

class UserActivityTracker:
	def __init__(self):
		self.data = {}

	def login(self, user: str, time: str):
		self.user = user
		self.time = time
		data = self.data
		data[user] = {"login": time}

	def logout(self, user: str, time: str):
		self.user = user
		self.time = time
		data = self.data
		time_data = data[user]
		time_data["logout"] = time

	def showData(self):
		data = self.data
		return data

	def get_total_time(self, user):
		self.user = user
		data = self.data
		users_time_data = data[user]
		login_time = users_time_data["login"]
		logout_time = users_time_data["logout"]
		t1 = datetime.strptime(login_time, "%H:%M")
		t2 = datetime.strptime(logout_time, "%H:%M")
		delta = (t2 - t1).total_seconds()/60
		return delta

tracker = UserActivityTracker()

tracker.login("Dinesh", "10:30")
tracker.logout("Dinesh", "13:00")

data = tracker.showData()
total_time = tracker.get_total_time("Dinesh")

print(f"data {data} \n")

print(f"total time: {total_time} minutes")


