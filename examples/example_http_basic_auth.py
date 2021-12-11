import requests



def attempt_fx(pair):
	try:
		username = pair[0]
		password = pair[1]

		auth = requests.auth.HTTPBasicAuth(username, password)

		r = requests.get(url="http://127.0.0.1:8888", auth=auth, verify=False, timeout=5)

		if (r.status_code == 200):
			return True
		else:
			return False

	except Exception as e:
		print ("[!] Exception: " + str(e))
		return "retry"



###################################################################################################################



import bruteforcer

number_threads = 8
wordlist_var = None
username_var = ["admin", "bill", "user", "demo"]
password_var = ["demo", "safe", "password"]

b = bruteforcer.Bruteforcer(number_threads, wordlist_var, username_var, password_var, attempt_fx)
b.run()
b.kill_all_threads()
