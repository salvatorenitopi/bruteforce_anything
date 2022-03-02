import socket
import time



def attempt_fx(input_dict):


	# def grab_banner(ip_address, port):
	# 	try:
	# 		s = socket.socket()
	# 		s.settimeout(60)
	# 		s.connect((ip_address, port))
	# 		banner = s.recv(1024)
	# 		s.close()
	# 		return banner

	# 	except:
	# 		return None



	def grab_banner(ip_address, port):
		try:
			s = socket.socket()
			s.settimeout(60)

			if (s.connect_ex((ip_address, port)) != 0):
				return None

			banner = s.recv(1024)
			s.close()
			return banner

		except:
			return None



	destination = input_dict.get("destination").split(":")
	ip = destination[0]
	port = int(destination[1])


	banner = grab_banner(ip, port)
	
	if (banner == None):
		return False
	else:
		return True





###################################################################################################################



import bruteforcer

number_threads = 64
variables_dict = { "destination": ["192.168.1.1:80", "192.168.1.1:443"]  }

b = bruteforcer.Bruteforcer(number_threads, variables_dict, attempt_fx, stop_on_success=False, successful_attempts_filename="successful_attempts.txt")
b.run()
b.kill_all_threads()
