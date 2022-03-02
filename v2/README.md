# bruteforce_anything_v2
You provide the testing function and a wordlist, and the script will do the rest.

This library allows you to easily create a multi-threaded script for fast bruteforcing virtually anything.

## How to use
1. Import the library.
```python
import bruteforcer
```
2. Write a testing function that takes in input a dictionary. Use the dictionary values as you need.
If the functions returns true the bruteforcer bruteforce will know that the attempt was successful, otherwise it will be considered as failed.
```python
def attempt_fx(input_dict):
	username = input_dict.get('username')
	password = input_dict.get('password')

	if (username[0] == "b"):
		return True
	else:
		return False
```
3. Configure the number of threads a dictionary with all the needed values.
```python
number_threads = 8
variables_dict = { "username": ["admin", "bill", "user", "demo"], "password": ["demo", "safe", "password"] }
```
4. Instantiate the object and call the run method.
```python
b = bruteforcer.Bruteforcer(number_threads, variables_dict, attempt_fx, stop_on_success=False, successful_attempts_filename="successful_attempts.txt")
b.run()
b.kill_all_threads()
```

Multiple test implementations can be found in the *examples/* folder.
