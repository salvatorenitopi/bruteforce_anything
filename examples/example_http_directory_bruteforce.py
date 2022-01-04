import requests



def attempt_fx(path):
	try:
		r = requests.get(url="http://127.0.0.1:8000/" + path[0], verify=False, timeout=5)

		if (r.status_code != 404):
			return True
		else:
			return False

	except Exception as e:
		print ("[!] Exception: " + str(e))
		return "retry"



###################################################################################################################



import bruteforcer

number_threads = 8
wordlist_var = ["secret.txt", "admin.php", "login.php", "index.php"]
username_var = None
password_var = None

b = bruteforcer.Bruteforcer(number_threads, wordlist_var, username_var, password_var, attempt_fx)
b.run()
b.kill_all_threads()



'''
# Example of Excecution 


python3 -m http.server 
	Serving HTTP on :: port 8000 (http://[::]:8000/) ...
	::ffff:127.0.0.1 - - [04/Jan/2022 15:32:28] code 404, message File not found
	::ffff:127.0.0.1 - - [04/Jan/2022 15:32:28] "GET /index.php HTTP/1.1" 404 -
	::ffff:127.0.0.1 - - [04/Jan/2022 15:32:28] "GET /secret.txt HTTP/1.1" 200 -
	::ffff:127.0.0.1 - - [04/Jan/2022 15:32:28] code 404, message File not found
	::ffff:127.0.0.1 - - [04/Jan/2022 15:32:28] code 404, message File not found
	::ffff:127.0.0.1 - - [04/Jan/2022 15:32:28] "GET /login.php HTTP/1.1" 404 -
	::ffff:127.0.0.1 - - [04/Jan/2022 15:32:28] "GET /admin.php HTTP/1.1" 404 -



python3 example_http_directory_bruteforce.py
	[i] Using Wordlist in list mode
		number of elements: 3
	
	[!] Attempt failed for ['index.php'] (0.2366 seconds)
	[*] Attempt successful for ['secret.txt'] (0.225 seconds)
	[!] Attempt failed for ['login.php'] (0.2367 seconds)
	[!] Attempt failed for ['admin.php'] (0.2369 seconds)
'''
