import sys
import notifier
import datetime as date
from random import randint
from randTask import generate_random_task

def generate_sprint_code():
	now = date.datetime.now()
	year = str(now.year)
	month = str(now.month)
	day = str(now.day)
	formatted_month = month if len(month) == 2 else "0" + month
	formatted_day = day if len(day) == 2 else "0" + day
	rand_code = generate_random_task(0,9999,4) # Random 4 digit number.
	sprint_code = year + formatted_month + formatted_day + rand_code
	return sprint_code

def main(args):
	n = notifier.Notifier()
	sprint_code = generate_sprint_code()
	n.success("Sprint: " + sprint_code, False)


if __name__ == "__main__":
	main(sys.argv)
