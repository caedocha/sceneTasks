import notifier
import sys
import pprint
from random import randint

def generate_random_task(min_range, max_range, length):
	if len(str(max_range)) > length:
		rand_notifier = notifier.Notifier()
		rand_notifier.error(("range diffrence", "max_range bigger than length"))
		exit()
	rand_number = randint(min_range,max_range)
	number_length = len(str(rand_number))
	difference = length - number_length
	leading_zeros = "0" * difference
	rand_task = leading_zeros + str(rand_number)
	return rand_task

def main(args):
	if len(args) >= 2:
		number_tasks = int(args[1])
	else:
		number_tasks = 1
	if len(args) == 3:
		extention = args[2]
	else:
		extention = None
	for n in range(number_tasks):
		if extention is None:
			rand_task = generate_random_task(0,9999,4)
		else:
			rand_task = extention + "-" + generate_random_task(0,9999,4)
		rand_notifier = notifier.Notifier()
		rand_notifier.success("Task: " + rand_task, False)
	
if __name__ == "__main__":
	main(sys.argv)
