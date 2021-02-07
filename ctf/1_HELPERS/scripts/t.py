f = open("words_en_sorted.txt", "r")
ltemp = f.readlines()
f.close()

l1 = [] 
for line in ltemp:
	l1.append(line.split(" ")[0] + "\n")

l1 = sorted(set(l1))
print(l1[:10])


f = open("words_en_nums.txt", "r")
l2 = f.readlines()
f.close()

l2 = sorted(set(l2))
print(l2[:10])

l1.extend(l2)
l = sorted(set(l1))

f = open("words_en", "w")
f.writelines(l)
f.close()