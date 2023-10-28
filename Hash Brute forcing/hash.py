import hashlib
import pyfiglet

ascii_banner = pyfiglet.figlet_format("Python 4 Pentesters \n HASH CRACKER")
print(ascii_banner)

wordlist_location = str(input('Enter wordlist file: '))
hash_input = str(input('Enter hash to be cracked: '))

with open(wordlist_location, 'r') as file:
	for  line in file.readlines():
		hash_ob = hashlib.sha256(line.strip().encode()) # change this for whatever
		hashed_pass = hash_ob.hexdigest()
		if hashed_pass == hash_input:
			print("Found password: " + line.strip())
			exit(0)
