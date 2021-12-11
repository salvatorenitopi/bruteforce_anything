import os
import time
import queue
import threading




class Bruteforcer(object):
	def __init__(self, number_threads, wordlist_var, username_var, password_var, attempt_fx):
		super(Bruteforcer, self).__init__()
		self.number_threads = number_threads
		self.wordlist_var = wordlist_var
		self.username_var = username_var
		self.password_var = password_var
		self.attempt_fx = attempt_fx

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




	def kill_all_threads (self):
		for i in range(0, self.number_threads):
			self.JOBS_QUEUE.put(self.terminate_signal)




	def dispatcher_thread (self, tid):
		while True:
			item = self.JOBS_QUEUE.get()

			if (item == self.terminate_signal):
				break
			
			now = time.perf_counter()
			outcome = None
			while (outcome == None):
				outcome = self.attempt_fx(item)

				if (outcome == True):
					print (self.green + "[*] Attempt successful for " + str(item) + " (" + str(round(time.perf_counter(), 4)) + " seconds)" + self.nc)
					
					# Stop other threads
					self.kill_all_threads()

				elif (outcome == False):
					print (self.orange + "[!] Attempt failed for " + str(item) + " (" + str(round(time.perf_counter(), 4)) + " seconds)" + self.nc)

				elif (outcome == "retry"):
					print ("[i] Requested retry for " + str(item) + " (" + str(round(time.perf_counter(), 4)) + " seconds)")
					time.sleep(self.retry_delay)

				else:
					print (self.red + "[!] Got unexpected outcome (" + str(outcome) + ") for " + str(item) + " (" + str(round(time.perf_counter(), 4)) + " seconds)" + self.nc)


			#print (self.JOBS_QUEUE.qsize())
			self.JOBS_QUEUE.task_done()





	def run (self):
		for i in range(0, self.number_threads):
			threading.Thread(target=self.dispatcher_thread, daemon=False, args=(i,)).start()


		#---------------------------------------------------------------------------------------------------------------------------------
		# WORDLIST - List Mode
		#---------------------------------------------------------------------------------------------------------------------------------

		if ((type(self.wordlist_var) == list) and (len(self.wordlist_var) > 0)):
			print ("[i] Using Wordlist in list mode")
			print ("\tnumber of elements: " + str(len(self.wordlist_var)) + "\n")

			for word in self.wordlist_var:
				self.JOBS_QUEUE.put([word])

			return 0




		#---------------------------------------------------------------------------------------------------------------------------------
		# WORDLIST - File Mode
		#---------------------------------------------------------------------------------------------------------------------------------

		elif ((type(self.wordlist_var) == str) and (os.path.isfile(self.wordlist_var) == True)):
			print ("[i] Using Wordlist in file mode")
			print ("\tfilename: " + self.wordlist_var + "\n")

			with open(self.wordlist_var) as f:
				while True:
					if (self.JOBS_QUEUE.qsize() > self.number_threads * 10000):				# Don't saturate memory
						time.sleep(0.5)

					raw_line = f.readline()
				
					if ((raw_line == None) or (len(raw_line) < 1)):
						break

					line = raw_line[:-1] if (raw_line[-1] == "\n") else raw_line
					self.JOBS_QUEUE.put([line])

			return 0




		#---------------------------------------------------------------------------------------------------------------------------------
		# USERNAME + PASSWORD - List mode
		#---------------------------------------------------------------------------------------------------------------------------------

		elif ((type(self.username_var) == list) and (len(self.username_var) > 0) and (type(self.password_var) == list) and (len(self.password_var) > 0)):
			print ("[i] Using Username List combined with Password File")
			print ("\tusername elements: " + str(len(self.username_var)))
			print ("\tpassword elements: " + str(len(self.password_var)) + "\n")

			for username in self.username_var:
				for password in self.password_var:
					self.JOBS_QUEUE.put([username, password])

			return 0




		#---------------------------------------------------------------------------------------------------------------------------------
		# USERNAME + PASSWORD - Hybrid (List + File)
		#---------------------------------------------------------------------------------------------------------------------------------

		elif ((type(self.username_var) == list) and (len(self.username_var) > 0) and (type(self.password_var) == str) and (os.path.isfile(self.password_var) == True)):
			print ("[i] Using Username List combined with Password File")
			print ("\tusername elements: " + str(len(self.username_var)))
			print ("\tpassword filename: " + self.password_var + "\n")

			for username in self.username_var:

				with open(self.password_var) as f_pass:
					while True:
						if (self.JOBS_QUEUE.qsize() > self.number_threads * 10000):				# Don't saturate memory
							time.sleep(0.5)

						raw_password = f_pass.readline()
				
						if ((raw_password == None) or (len(raw_password) < 1)):
							break

						password = raw_password[:-1] if (raw_password[-1] == "\n") else raw_password

						self.JOBS_QUEUE.put([username, password])

			return 0




		#---------------------------------------------------------------------------------------------------------------------------------
		# USERNAME + PASSWORD - Hybrid (File + List)
		#---------------------------------------------------------------------------------------------------------------------------------

		elif ((type(self.username_var) == str) and (os.path.isfile(self.username_var) == True) and (type(self.password_var) == list) and (len(self.password_var) > 0)):
			print ("[i] Using Username File combined with Password List")
			print ("\tusername filename: " + self.username_var)
			print ("\tpassword elements: " + str(len(self.password_var)) + "\n")

			with open(self.username_var) as f_user:
				while True:
					raw_username = f_user.readline()
					
					if ((raw_username == None) or (len(raw_username) < 1)):
						break

					username = raw_username[:-1] if (raw_username[-1] == "\n") else raw_username


					for password in self.password_var:

							self.JOBS_QUEUE.put([username, password])

			return 0




		#---------------------------------------------------------------------------------------------------------------------------------
		# USERNAME + PASSWORD - File Mode
		#---------------------------------------------------------------------------------------------------------------------------------

		elif ((type(self.username_var) == str) and (os.path.isfile(self.username_var) == True) and (type(self.password_var) == str) and (os.path.isfile(self.password_var) == True)):
			print ("[i] Using Username File combined with Password File")
			print ("\tusername filename: " + self.username_var)
			print ("\tpassword filename: " + self.password_var + "\n")

			with open(self.username_var) as f_user:
				while True:
					raw_username = f_user.readline()
					
					if ((raw_username == None) or (len(raw_username) < 1)):
						break

					username = raw_username[:-1] if (raw_username[-1] == "\n") else raw_username


					with open(self.password_var) as f_pass:
						while True:
							if (self.JOBS_QUEUE.qsize() > self.number_threads * 10000):				# Don't saturate memory
								time.sleep(0.5)

							raw_password = f_pass.readline()
					
							if ((raw_password == None) or (len(raw_password) < 1)):
								break

							password = raw_password[:-1] if (raw_password[-1] == "\n") else raw_password

							self.JOBS_QUEUE.put([username, password])

				return 0




		else:
			print ("[!] Can not find suitable mode")
			self.kill_all_threads()
			return -1
