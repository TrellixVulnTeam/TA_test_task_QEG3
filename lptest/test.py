from collections import Counter
import re

b = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

i = 0
while i < len(b):
    text = b[i]
    j = 0
    while j < len(text):
        if text[j] == "1" or text[j] == "2" or text[j] == "3":
            del (text[j])
        else:
            j += 1

    if len(text) == 0:
        del(b[i])
    else:
        i += 1

print(b)
