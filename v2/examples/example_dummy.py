import bruteforcer

def attempt_fx(input_dict):
	username = input_dict.get('username')
	password = input_dict.get('password')

	if (username[0] == "b"):
		return True
	else:
		return False


number_threads = 8
variables_dict = { "username": ["admin", "bill", "user", "demo"], "password": ["demo", "safe", "password"] }

b = bruteforcer.Bruteforcer(number_threads, variables_dict, attempt_fx, stop_on_success=False, successful_attempts_filename="successful_attempts.txt")
b.run()
b.kill_all_threads()
