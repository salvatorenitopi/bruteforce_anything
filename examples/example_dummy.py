import bruteforcer

def attempt_fx(pair):
	username = pair[0]
	password = pair[1]
	if (username[0] == "b"):
		return True
	else:
		return False

number_threads = 8
wordlist_var = None
username_var = ["admin", "bill", "user", "demo"]
password_var = ["demo", "safe", "password"]

b = bruteforcer.Bruteforcer(number_threads, wordlist_var, username_var, password_var, attempt_fx)
b.run()
b.kill_all_threads()
