#!/usr/env/bin python3
import subprocess, requests, re, sys
import operator
import argparse, apt, os
import threading
from shutil import copyfile

result_url = []

class fetch_thread(threading.Thread):	
	def __init__(self, count, url,schema):
		threading.Thread.__init__(self)
		self.count = count + 1
		self.url = url
		self.schema = schema

	def run(self):
		response = requests.get(self.schema+self.url).status_code
		if response == 200:
			result_url.append(self.url)

def fetch_url(urls,schema):
	threads = []	
	for count, url in enumerate(urls):
		count = fetch_thread(count, url,schema)
		threads.append(count)

	for i in threads:
		i.start()

	for i in threads:
		i.join()

	return result_url

def ask(question,default):
	yes = set(['yes','y','ye'])
	no = set(['no','n'])
	yes.add('') if default == 'y' else no.add('')
	while True:
		choice = input(question + " Default [" + default + "]: ").lower()
		if choice in yes:
			return True
		elif choice in no:
			return False
		else:
			print("\t    Please answer with [y] or [n]: ");

def ping(hostname):
	p = subprocess.Popen(['ping','-c 3', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	p = [str(x.decode('utf-8')) for x in p]

	if not p[0].strip():
		# error
		print("\t[!] Error: Something went wrong ...")
		print("\t    " + p[1].strip())

		response = ask("\t   Do you want to retry[y] or skip[n]?",'n')
		if response:
			ping(hostname)
		else:
			return p
	else:
		return p


def main():

	# Check if user is root first.
	if os.getuid() != 0:
		sys.exit("[!] Must run as root/sudo\n")

	# Argument parser

	parser = argparse.ArgumentParser(description='Kali Source Updater automatically select the best kali mirror server and apply the configuration')
	parser.add_argument('-v','--verbose', help='enable verbose output', action="store_true")
	parser.add_argument('-https', help='use HTTPS in apt transport (default HTTP)', action="store_true")
	parser.add_argument('-src', help='enable sources packages (default disable)', action="store_true")
	parser.add_argument('-u','--update', help='update and upgrade completely (default disable)', action="store_true")
	args = parser.parse_args()

	# Initialize arguments
	https = True if args.https else False
	verbose = True if args.verbose else False
	sources = True if args.src else False
	update = True if args.update else False

	# Banner
	print("                                                                                 ") 
	print("  _  __     _ _   ___                        _   _          _      _             ")
	print(" | |/ /__ _| (_) / __| ___ _  _ _ _ __ ___  | | | |_ __  __| |__ _| |_ ___ _ _   ")
	print(" | ' </ _` | | | \__ \/ _ \ || | '_/ _/ -_) | |_| | '_ \/ _` / _` |  _/ -_) '_|  ")
	print(" |_|\_\__,_|_|_| |___/\___/\_,_|_| \__\___|  \___/| .__/\__,_\__,_|\__\___|_|    ")
	print("                                                  |_|                            ")
	print("									- v1.0  	")									


	# Preparing
	cache = apt.Cache()
	cache.open()

	if https:
		package = "apt-transport-https" 
		print("[-] Checking if '" + package + "' package is installed.")
		if cache[package].is_installed:
			if verbose:
				print("\t- "+package+" is installed\n")
		else:
			print("\t! "+package+" is NOT installed. Attempting to install ...")
			cache[package].mark_install()
			print("\t- Installing "+package+"\n")
			try:
				cache.commit()
				print("\n\t- "+package+" installed succesfully")
			except Exception as e:
				print("\t! package "+package+" is failing to install")
				print("\t  "+str(e))
				sys.exit(1)

	if update:
		print("[+] Please wait unitil the update gets completed !!")
		print("[+] Executing command --> apt-get update -y && apt-get upgrade -y && apt-get full-upgrade -y && apt-get dist-upgrade -y && apt-get autoremove -y\n")
		os.system('apt-get update -y && apt-get upgrade -y && apt-get full-upgrade -y && apt-get dist-upgrade -y && apt-get autoremove -y')
		print("\n")
		print("[+] All updates and upgrades completed successfully")
		sys.exit(1)


	print("[+] Getting mirror list ...")
	response = requests.get('https://http.kali.org/README.mirrorlist').text
	urls = re.findall(r'(?:href="http(?:s|))(.*)(?:/README")',response)[2:]
	
	if verbose:
		print("[+] Found a lists of mirrors:")
		for url in urls:
			print("\t- https" + url)
		print("")

	print("[+] Checking mirrors ...")
	schema = 'https' if https else 'http'
	new_urls = fetch_url(urls,schema)

	mirrors = {}
	print("[+] Finding the best latency")

	for hostname in new_urls:
		hostname = hostname.split("//")[-1].split("/")[0].split('?')[0]

		while True:
			p = ping(hostname)
			try:
				average = p[0].strip().splitlines()[7].split('=')[1].split('/')[1]
				mirrors[hostname] = str(str(average).zfill(7))
				break
			except Exception as e:
				if not ask("\t[!] Something went wrong. would you like to try again [y] or [n].",'y'):
					print ("\t    Exiting ...\n")
					sys.exit(1)

		if verbose:
			print("\t- {0:30} : {1}".format(hostname,average))

	if verbose:
		print("")

	
	# sorted to fastest mirror
	sorted_mirrors = sorted(mirrors.items(), key=operator.itemgetter(1))
	print("[+] Fastest mirror: " + str(sorted_mirrors[0]))

	print("[+] Preparing ...")

	# Making backup
	if verbose:
		print("\t- Making a backup file /etc/apt/sources.list.bk ...")

	copyfile('/etc/apt/sources.list', '/etc/apt/sources.list.bk')

	if verbose:
		print("\t- Checking sources.list for older entries ...")

	contents = []
	file = open("/etc/apt/sources.list", "r+")
	if verbose:
		print("\t- Commenting older entries ...")
	i = 0
	for line in file.readlines():
		if (re.search(r'^deb http(?:s|)://http.kali.org/kali', line, re.I)) or (re.search(r'^deb-src http(?:s|)://http.kali.org/kali', line, re.I)):
			newline = "#" + line
			file.write(newline)
			contents.append(newline)
		elif re.search(r'^# Autogenerated script by Kali-Source Updater', line, re.I):
			print("\t! Found previous applies! Commenting it out ...")
			contents.append(line)
			i = 1
		elif i == 1:
			if not line.startswith("#"):
				newline = "#" + line
				file.write(newline)
				contents.append(newline)
			else:
				contents.append(line)
			i = i+1
		elif i == 2:
			if not line.startswith("#"):
				newline = "#" + line
				file.write(newline)
				contents.append(newline)
			else:
				contents.append(line)
			i = 0
		else:
			contents.append(line)
	file.seek(0)
	file.truncate()
	file.seek(0)
	for line in contents:
		file.write(line)
	file.close()
	if verbose:
		print("\t- Done\n")

	print("[+] Updating sources.list with new entry ...")
	
	matching = [s for s in urls if sorted_mirrors[0][0] in s]
	new_mirror = schema + matching[0]
	if verbose:
		print("\t- Your new mirror: " + new_mirror + "\n")

	temp = "sh -c \'echo \"\n# Autogenerated script by Kali-Source Updater\" >> /etc/apt/sources.list\'"

	subprocess.Popen(temp, shell=True, stdout=subprocess.PIPE).stdout.read()

	line = "deb " + new_mirror + " kali-rolling main contrib non-free"
	temp = "sh -c \'echo %s >> /etc/apt/sources.list\'"
	subprocess.Popen(temp % line, shell=True, stdout=subprocess.PIPE).stdout.read()

	line = "deb-src " + new_mirror + " kali-rolling main contrib non-free"
	if not sources:
		line = "#" + line
	temp = "sh -c \'echo \"%s\" >> /etc/apt/sources.list\'"
	subprocess.Popen(temp % line, shell=True, stdout=subprocess.PIPE).stdout.read()

	print("[+] Done!")
 	
	print("[+] This command would be executed --> apt-get update -y && apt-get upgrade -y && apt-get full-upgrade -y && apt-get dist-upgrade -y && apt-get autoremove -y")
	response = ask("\t Enter [y] or [n] for running all updates, upgrades and autoremoval in the system",'n')

	if response:
		print("[+] Please wait unitil the update gets completed !!\n")
		os.system('apt-get update -y && apt-get upgrade -y && apt-get full-upgrade -y && apt-get dist-upgrade -y && apt-get autoremove -y')
		print("\n")
		print("[+] All updates and upgrades completed successfully")
	else:
		sys.exit(1)

	
if __name__ == "__main__":
	main()
