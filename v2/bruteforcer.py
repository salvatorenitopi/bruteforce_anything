import os
import time
import json
import queue
import threading
import itertools




class Bruteforcer(object):
	def __init__(self, number_threads, variables_dict, attempt_fx, stop_on_success=False, successful_attempts_filename="successful_attempts.txt"):
		super(Bruteforcer, self).__init__()
		self.number_threads = number_threads
		self.variables_dict = variables_dict
		self.attempt_fx = attempt_fx
		self.stop_on_success = stop_on_success
		self.successful_attempts_filename = successful_attempts_filename

		self.retry_delay = 1
		self.JOBS_QUEUE = queue.Queue()
		self.terminate_signal = ("<"*64) + "TERMINATE" + (">"*64)

		self.red = '\033[0;31m'
		self.light_red = '\033[1;31m'
		self.green = '\033[0;32m'
		self.light_green = '\033[1;32m'
		self.orange = '\033[0;33m'
		self.yellow = '\033[1;33m'
		self.blue = '\033[0;34m'
		self.light_blue = '\033[1;34m'
		self.purple = '\033[0;35m'
		self.light_purple = '\033[1;35m'
		self.cyan = '\033[0;36m'
		self.light_cyan = '\033[1;36m'
		self.light_gray = '\033[0;37m'
		self.dark_gray = '\033[1;30m'
		self.white = '\033[1;37m'
		self.nc = '\033[0m'

		self.cycle = True




	def kill_all_threads (self):
		for i in range(0, self.number_threads):
			self.JOBS_QUEUE.put(self.terminate_signal)




	def dispatcher_thread (self, tid):
		while self.cycle:
			item = self.JOBS_QUEUE.get()

			if (item == self.terminate_signal):
				break
						
			textual_item = str(item)
			try: 	textual_item = json.dumps(item)
			except:	pass
			
			now = time.perf_counter()
			outcome = self.attempt_fx(item)

			if (outcome == True):
				print (self.green + "[*] Attempt successful for " + textual_item + " (" + str(round(time.perf_counter(), 4)) + " seconds)" + self.nc)
				
				f = open(self.successful_attempts_filename, 'a')
				f.write(textual_item + "\n")
				f.close()

				if (self.stop_on_success == True):
					# Stop other threads
					self.cycle = False
					self.kill_all_threads()

			else:
				print (self.orange + "[!] Attempt failed for " + textual_item + " (" + str(round(time.perf_counter(), 4)) + " seconds)" + self.nc)


			#print (self.JOBS_QUEUE.qsize())
			self.JOBS_QUEUE.task_done()





	def run (self):
		#---------------------------------------------------------------------------------------------------------------------------------
		# CREATE N Threads
		#---------------------------------------------------------------------------------------------------------------------------------

		for i in range(0, self.number_threads):
			threading.Thread(target=self.dispatcher_thread, daemon=False, args=(i,)).start()


		#---------------------------------------------------------------------------------------------------------------------------------
		# EXPAND self.variables_dict
		#---------------------------------------------------------------------------------------------------------------------------------

		expanded_variables_dict = {}

		for k,v in self.variables_dict.items():

			if (type(v) == str):
				if (os.path.isfile(v) == True):
					lines = []
					with open(v) as f:
						while True:
							raw_line = f.readline()
						
							if ((raw_line == None) or (len(raw_line) < 1)):
								break

							line = raw_line[:-1] if (raw_line[-1] == "\n") else raw_line
							lines.append(line)

					# f = open(v, 'r')
					# lines = f.read().split('\n')
					# f.close()

					print ("[i] Using \"" + str(k) + "\":" + str(v) + " as a file")
					expanded_variables_dict[k] = lines

				else:
					print ("[i] Converting string in \"" + str(k) + "\" as list")
					expanded_variables_dict[k] = [v]


			elif (type(v) == int):
					print ("[i] Converting int in \"" + str(k) + "\" as list")
					expanded_variables_dict[k] = [str(v)]


			elif (type(v) == float):
					print ("[i] Converting float in \"" + str(k) + "\" as list")
					expanded_variables_dict[k] = [str(v)]


			elif (type(v) == list):
				print ("[i] Variable \"" + str(k) + "\" is ok")
				expanded_variables_dict[k] = v

			else:
				print ("[!] Variable \"" + str(k) + "\" is invalid")
				return -1


		self.variables_dict = None			# Free some RAM


		#---------------------------------------------------------------------------------------------------------------------------------
		# UNWRAP expanded_variables_dict
		#---------------------------------------------------------------------------------------------------------------------------------

		keys, values = zip(*expanded_variables_dict.items())
		permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]

		print ("[i] Un-wrapping completed, number of permutated dicts: " + str(len(permutations_dicts)))


		#---------------------------------------------------------------------------------------------------------------------------------
		# POPULATE JOBS_QUEUE
		#---------------------------------------------------------------------------------------------------------------------------------

		for d in permutations_dicts:
			self.JOBS_QUEUE.put(d)





##########################################################################################
# Example

'''
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
'''

##########################################################################################
