from pwn import *
import time
import string
import os
import fnmatch

class Passing:

	def __init__(self, cmd):
		# the scalpel command received from GUI
		self.cmd = cmd
		# status of executing the command
		# -1: command itself constructed with errors
		# 0: command executed correctly
		# 1: command executed with error
		self.status = -2
		# Scalpel version
		self.version = ""
		# Author Informaiton
		self.authorInfo = ""
		# Images to be carved
		self.target = ""

		##### TODO, multiple images support #####

		# percentage info for allocation, contains two float numbers:
		# 1, percentage info as NUM, such as 4.9 %
		# 2, bytes carved as NUM, such as 10.0 MB
		self.allocating_queue = ["", ""]
		# Carving signature list, contains four strings:
		# 1, type of carving files, such as "gif", "jpg"
		# 2, header, such as "\x47\x49\x46\x38\x37\x61"
		# 3, footer, such as "\x00\x3b"
		# 4, number of files carved for this signature, such as "20" files
		self.carving_list = []
		# percentage info for processing of images, contains two float numbers:
		# 1, percentage info as NUM, such as 48.8 %
		# 2, bytes carved as NUM, such as 100.0 MB
		self.image_processing = ["", ""]

		##### TODO							#####

		# Total number of file carved
		self.num_file_carving = -1
		# Total time consumed
		self.time_consumed = -1
		# Error informaiton if occured
		self.error_info = ""
		# MD5 list of all carved files
		self.md5list = {}

	# Main function to execute and parse result
	def execute(self):
		if "scalpel" not in self.cmd:
			self.status = -1
			return
		else:
			p = process(self.cmd, shell=True)
			process_checker = 1
			front = p.recvlines(5)
			path = ""

			# Assign version and author information
			for line in front:
				if "Scalpel version" in line:
					self.version = line.split(" ")[2].strip()
				if "Golden G. Richard III" in line:
					self.authorInfo = line

			if "ERROR:" in front[2]:
				for line in front[2:]:
					self.error_info += line + "\n"
				self.status = 1
				return
			# Assign images to be processed
			else:
				self.status = 0
				for line in front:
					if "Opening target" in line:
						# print "target: " + result.split(" ")[2].strip('"')
						self.target = line.split(" ")[2].strip('"')
					else:
						continue

			while p.can_recv():
				result = ""
				try:
					result = p.recvuntil('\r')
					if "ETA" in result and "Allocating work queues" not in result and "Processing of image" not in result:
						percentage = float(result.split(":")[1].split("%")[0].strip())
						byte = float(result.split(":")[1].split("%")[1].split("MB")[0].strip())
						if process_checker == 1:
							self.allocating_queue[0] = percentage
							self.allocating_queue[1] = byte
						else:
							self.image_processing[0] = percentage
							self.image_processing[1] = byte
							if percentage > 97:
								break
					elif "Allocating work queues" in result:
						percentage = float(result.splitlines()[0].split(":")[1].split("%")[0].strip())
						byte = float(result.splitlines()[0].split(":")[1].split("%")[1].split("MB")[0].strip())
						if process_checker == 1:
							self.allocating_queue[0] = percentage
							self.allocating_queue[1] = byte
							process_checker = 2

						for line in result.splitlines()[1:]:
							if "header" in line and "footer" in line:
								temp = []
								temp.append(line.split(" ")[0].strip())
								temp.append(line.split(" ")[3].strip('"'))
								temp.append(line.split(" ")[6].strip('"'))
								temp.append(line.split(" ")[8].strip())
								self.carving_list.append(temp)
					else:
						continue

				except EOFError:
					break
			# Handle the rest of parsing info
			end = p.recvall()
			for line in end.splitlines():
				if "Processing of image" in line:
					self.image_processing[0] = float(line.split(":")[1].split("%")[0].strip())
					self.image_processing[1] = float(line.split(":")[1].split("%")[1].split("MB")[0].strip())
				elif "Scalpel is done," in line:
					self.num_file_carving = int(line.split(" ")[6].strip(','))
					self.time_consumed = int(line.split(" ")[9].strip())
				else:
					continue

			if self.status == 0:
				parameter = self.cmd.split(" ")
				for i in range(0,len(parameter)):
					if parameter[i] == "-o":
						path = parameter[i+1]
						break
				# print path
				for root, dirs, files in os.walk(path):
					for file in files:
						if file == "audit.txt":
							continue
						else:
							filename = os.path.join(root, file)
							self.md5list[filename] = self.md5(filename)

	def md5(self, fname):
	    hash_md5 = hashlib.md5()
	    with open(fname, "rb") as f:
	        for chunk in iter(lambda: f.read(4096), b""):
	            hash_md5.update(chunk)
	    f.close()
	    return hash_md5.hexdigest()

# a = Passing("scalpel -c jpg.conf practice1.dd -o out")
# a.execute()

if __name__ == '__main__':
    print ("Please don't call this file directly.")
