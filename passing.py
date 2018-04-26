from pwn import *

cmd = "scalpel -c jpg.conf practice1.dd -o out"

p = process(cmd, shell=True)
result = p.recvall()

for line in result.splitlines():
	print line
