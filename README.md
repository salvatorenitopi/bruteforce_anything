# bruteforce_anything
You provide the testing function and a wordlist, and the script will do the rest.

This library allows you to easily create a multi-threaded script for fast bruteforcing virtually anything.

## How to use
1. Import the library.
```python
import bruteforcer
```
2. Write a testing function that takes in input the value/values that need to be tested.
If the functions returns true the bruteforcer bruteforce will know that the attempt was successful, otherwise it will be considered as failed.
```python
def attempt_fx(pair):
	username = pair[0]
	password = pair[1]
	if (username[0] == "b"):
		return True
	else:
		return False
```
3. Configure some variables.
```python
number_threads = 8
wordlist_var = None					# Can be None, list, str (str contains the file path to a wordlist)
username_var = ["admin", "bill", "user", "demo"]	# Can be None, list, str (str contains the file path to a wordlist)
password_var = "/home/root/wordlist.txt"		# Can be None, list, str (str contains the file path to a wordlist)
```
4. Instantiate the object and call the run method.
```python
b = bruteforcer.Bruteforcer(number_threads, wordlist_var, username_var, password_var, attempt_fx)
b.run()
b.kill_all_threads()
```

Multiple test implementations can be found in the *examples/* folder.


## Version 2

You can find a more flexible version of the *bruteforcer.py* library in the *v2/* folder.

WARNING: to keep the code as flexible as possible the implementation is not memory-efficient.
