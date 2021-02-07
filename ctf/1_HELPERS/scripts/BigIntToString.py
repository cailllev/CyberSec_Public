import sys

# ASCII base = 128, byte-wise base = 256

num = int(sys.argv[1])
base = 256

if len(sys.argv) == 3:
    base = int(sys.argv[2])

char_vals = []

while num > 0:
	quotient, remainder = divmod(num, base)
	num = quotient

	char_vals.append(chr(remainder))

char_vals.reverse()
print(''.join(char_vals))