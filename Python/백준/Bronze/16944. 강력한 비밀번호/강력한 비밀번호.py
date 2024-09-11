import re

numbers = r"[0-9]"
lower_words = r"[a-z]"
upper_words = r"[A-Z]"
sp_words = r"[\!\@\#\$\%\^\&\*\(\)\-\+]"

checks = [numbers, lower_words, upper_words, sp_words]

N = int(input())
K = 0 if N >= 6 else 6 - N
C = 0
word = input()

for check in checks:
    if not re.search(check, word):
        C += 1

print(max(K, C))
