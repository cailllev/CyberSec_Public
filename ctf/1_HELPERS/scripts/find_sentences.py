# usage: python3 find_sentences.py wh.r.i.myw.rd 123435678194A 0 10000

# 123435678194A
# wh.r.i.myw.rd

import sys
import language_tool_python
tool = language_tool_python.LanguageTool('en-US')

partial_sentence = sys.argv[1]
uniques = sys.argv[2]
start_at = int(sys.argv[3])
word_count = int(sys.argv[4])

len_to_find = len(partial_sentence)

assert len(
    uniques) == len_to_find, f"Length of uniques {len(uniques)} and length of partial sentence {len_to_find} " \
                             f"has to match."

partial_sentence = partial_sentence.lower()


def check_grammar(sentence, until):
    s = (sentence[start_at:until]).capitalize()
    matches = tool.check(s)
    
    if len(matches) > 0:
        return False

    return True


def adapt_uniques(partial):
    adapted_uniques = [c for c in uniques]  # where_is_m.w.rd: 123435678914A => 12343_56_78914A
    for i in range(len(partial)):
        if partial[i] == " ":
            adapted_uniques.insert(i, " ")

    return adapted_uniques


def update_via_uniques(partial, at_pos, word):
    to_update = {}
    partial = [c for c in partial]

    adapted_uniques = adapt_uniques(partial)

    # find corresponding uniques
    for i in range(len(word)):
        to_update[adapted_uniques[i + at_pos]] = word[i]

    # insert all chars for newly restrained uniques
    for i in range(at_pos, len(adapted_uniques)):
        if adapted_uniques[i] in to_update:
            partial[i] = to_update[adapted_uniques[i]]

    # insert " " after word
    partial.insert(at_pos + len(word), " ")
    partial = "".join(partial)
    return partial


def find_next(partial, at_pos, found_chars):
    pot_next = {}

    adapted_uniques = adapt_uniques(partial)

    for word in data:
        if found_chars + len(word) > len_to_find:
            continue

        fits = True

        for i in range(len(word)):

            # check partial at "current word insert pos"
            if partial[i + at_pos] != ".":
                if word[i] != partial[i + at_pos]:
                    fits = False
                    break

            # on "free char", check unique constraint
            else:
                this_unique_nr = adapted_uniques[at_pos + i]

                for j in range(len(adapted_uniques)):
                    # skip itself, ? and " " checks
                    if j == at_pos + i or adapted_uniques[j] in ["?", " "]:
                        continue

                    # uniques do not match -> chars have to differ
                    if this_unique_nr != adapted_uniques[j]:

                        # char at partial[j] is too in the word
                        if at_pos <= j < at_pos + len(word):
                            if word[i] == word[j - at_pos]:
                                fits = False
                                break

                        # if 2nd char not in word -> partial char has to differ
                        else:
                            if word[i] == partial[j]:
                                fits = False
                                break

                    # uniques match -> chars have to match if both in word
                    else:

                        # char at partial[j] is too in the word
                        if at_pos <= j < at_pos + len(word):
                            if word[i] != word[j - at_pos]:
                                fits = False
                                break

                        # if 2nd char not in word -> partial has to be "." or same char
                        else:
                            if partial[j] != "." and word[i] != partial[j]:
                                fits = False
                                break

        if fits:
            updated_partial = update_via_uniques(partial, at_pos, word)

            # plus 1 for the added " "
            next_word_pos = at_pos + len(word) + 1
            count_found_chars = found_chars + len(word)

            pot_next[(updated_partial, next_word_pos, count_found_chars)] = {}

    return pot_next


def find_solutions(from_state):
    global solutions

    next_state = find_next(*from_state)

    # found some solutions, now test them
    for n in next_state:
        if not check_grammar(n[0], n[1]):
            continue

        if n[2] == len_to_find:
            solutions.append(n[0] + " - " + (n[0].replace(" ", "")).upper())

        else:
            find_solutions(n)


f = open("words_en.txt", "r")
data = []
for _ in range(word_count):
    try:
        data.append((f.readline()).split(" ")[0])
    except Exception:
        break

f.close()

'''
wh..e..myw.rd (partial_sentence) -> changes
123435678194A (uniques) -> does not change

keys in next are: ["partial_solution", insert next word at this pos, found chars]

program sequence:
next = {
    ["wh..e..myw.rd", 0]: {
        [["whate..myw.rd", 3]: {
            !!! NO SOLUTIONS !!!
        }, 
        ["where..myw.rd", 4]: {
            ["whereismyw.rd", 6]: {
                ["whereismyw.rd", 8]: {
                    ["whereismyword", 12]: {
                        -> solutions.append("whereismyword")
                    }
                }
            }
            ["whereitmyw.rd", 6]: {
                ["whereitmyw.rd", 8]: {
                    ["whereitmyword", 12]: {
                        -> solutions.append("whereitmyword")
                    }
                }
            }
        }
    }
}
'''
solutions = []
current_state = (partial_sentence, start_at, start_at)
found = {current_state: {}}

find_solutions(current_state)
info = "Found " + str(len(solutions)) + " solutions:\n" + "\n".join(solutions)
print(info)

f = open("solutions.txt", "w")
f.write(partial_sentence)
f.write(uniques)
f.write(str(start_at) + "\n")

f.writelines(info)
f.close()
