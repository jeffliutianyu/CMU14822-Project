from pwn import *

class Passing:
	# the scalpel command received from GUI
	cmd = ""
	# status of executing the command
	# -1: command itself constructed with errors
	# 0: command executed correctly
	# 1: command executed with error
	status = -2
	# Scalpel version
	version = ""
	# Author Informaiton
	authorInfo = ""
	# Images to be carved
	target = ""

	##### TODO, multiple images support #####

	# percentage info for allocation, contains two numbers:
	# 1, percentage info as NUM, such as 4.9
	# 2, bytes carved as NUM, such as 10.0
	allocating_queue = []
	# Carving signature list, contains four strings:
	# 1, type of carving files, such as "gif", "jpg"
	# 2, header, such as "\x47\x49\x46\x38\x37\x61"
	# 3, footer, such as "\x00\x3b"
	# 4, number of files carved for this signature, such as "20" files
	carving_list = []
	# percentage info for processing of images, contains two numbers:
	# 1, percentage info as NUM, such as 48.8
	# 2, bytes carved as NUM, such as 100.0 
	image_processing = []

	##### TODO							#####

	# Total number of file carved
	num_file_carving = -1
	# Total time consumed
	time_consumed = -1
	# Error informaiton if occured
	error_info = ""

	def exec():
		if "scalpel" not in cmd:
			status = -1
			return
		else:
			p = process(Passing.cmd, shell=True)
			result = p.recvline_endwith()



# for line in result.splitlines():
# 	if "stopped with exit code 0" in line:
# 		status = 0
# 	if "stopped with exit code 255" in line:
# 		status = 1
# 	print line



if __name__ == '__main__':
    print ("Please don't call this file directly.")