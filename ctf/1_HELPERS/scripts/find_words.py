# usage: python3 find_words.py w.rd 1234 0

import sys

checks = sys.argv[1]
uniques = sys.argv[2]
pos = int(sys.argv[3])
len_to_find = len(checks)

words = ["words_3k.txt", "words_10k.txt", "words_58k.txt"]
f = open(words[pos], "r")
data = f.readlines()
f.close()

for word in data:
	word = word.strip()

	word_len = len(word)
	if word_len != len_to_find:
	    continue

	fits = True

	for i in range(word_len):
		if checks[i] != ".":
			if word[i] != checks[i]:
				fits = False

		else:
			# on "free char", check unique constraint
			this_n = uniques[i]
			for j in range(word_len):
				if j == i:
					continue

				if this_n != uniques[j]:
					if word[i] == word[j]:
						fits = False
						break
				else:
					if word[i] != word[j]:
						fits = False
						break
		if not fits:
			break

	if fits:
		print(word)
