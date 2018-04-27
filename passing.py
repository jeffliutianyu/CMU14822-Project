from pwn import *
import time

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

	def execute(self):
		if "scalpel" not in self.cmd:
			self.status = -1
			return
		else:
			p = process(self.cmd, shell=True)
			process_checker = 1
			# print(p.poll(True))
			# print p.recvall()
			while p.can_recv():
				result = ""
				pwnlib.tubes.newline = '\r'
				try:
					result = p.recvuntil('\r')
					if "Scalpel Version" in result:
						self.version = result.split(" ")[2].strip()
					elif "Golden G. Richard III" in result:
						self.authorInfo = result
					elif "Opening target" in result:
						self.target = result.split('"')[1].strip()
					elif "ETA" in result:
						percentage = float(result.split(" ")[2].strip('%'))
						byte = float(result.split(" ")[5].strip())
						if process_checker == 1:
							self.allocating_queue[0] = percentage
							self.allocating_queue[1] = byte
							if percentage == 100.0:
								process_checker == 2
						else:
							self.image_processing = percentage
							self.image_processing = byte
					elif "header" in result and "footer" in result:
						temp = []
						temp.append(result.split(" ")[0].strip())
						temp.append(result.split(" ")[3].strip('"'))
						temp.append(result.split(" ")[6].strip('"'))
						temp.append(result.split(" ")[8].strip())
						self.carving_list.append(temp)
					elif "Scalpel is done," in result:
						self.num_file_carving = int(result.split(" ")[6].strip(','))
						self.time_consumed = int(result.split(" ")[9].strip())
					else:
						if "ERROR:" in result:
							self.error_info += result
							self.error_info += p.recvall()
							break

				except EOFError:
					break

			# print(p.poll(True))


# a = Passing("scalpel -c jpg.conf practice1.dd -o out")
# a.execute()



if __name__ == '__main__':
    print ("Please don't call this file directly.")
