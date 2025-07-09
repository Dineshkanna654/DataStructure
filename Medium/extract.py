import re

log_data = """[2025-07-07 10:15:32] INFO: User login successful - user_id=123
[2025-07-07 10:17:11] ERROR: Payment failed - user_id=456
[2025-07-07 10:18:55] INFO: User logout - user_id=123
[2025-07-07 10:21:00] ERROR: Server timeout - user_id=789
"""

def main(data: str):
	line_by_list =  data.splitlines()
	output = {
		'error_count': 0,
		'error_user_ids': [],
		'error_lines': []
	}
	for line in line_by_list:
		if (re.search("ERROR", line)):
			output['error_count'] = output['error_count'] + 1
			user_match = re.search(r"user_id=(\w+)", line)
			if user_match:
				output['error_user_ids'].append(user_match.group(1))
			output['error_lines'].append(line)
	return output

print(main(log_data))


