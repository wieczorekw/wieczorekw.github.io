from suffix_classifier import SuffixClassifier
import random
import time

NUMBER_OF_D_plus = 5000
NUMBER_OF_D_minus = 5000
ALPHABET = list("abcdefghijklmnopqrst")
MIN_LEN = 30
MAX_LEN = 30
K = 6

random.seed()
factors = dict()

def randomWord(d_min, d_max):
    s = bytearray()
    d = random.randint(d_min, d_max)
    for i in range(d):
        s.append(ord(random.choice(ALPHABET)))
    return s.decode()

examples = set()
while len(examples) < NUMBER_OF_D_plus:
    examples.add(randomWord(MIN_LEN, MAX_LEN))
counter_examples = set()
while len(counter_examples) < NUMBER_OF_D_minus:
    rw = randomWord(MIN_LEN, MAX_LEN)
    if rw not in examples:
        counter_examples.add(rw)

def naive(string, k):
    global examples, counter_examples

    def freqForSubstring(w):

        def scount():
            nonlocal s, w, k
            c = 0
            n = len(s)
            for i in range(n - k + 1):
                for j in range(k):
                    if s[i + j] != w[j]:
                        break
                else:
                    c += 1
            return c

        n_plus, n_minus = 0, 0
        for s in examples:
            n_plus += scount()
        for s in counter_examples:
            n_minus += scount()
        return n_plus, n_minus

    n = len(string)
    for pos in range(n - k + 1):
        f = string[pos : pos + k]
        if f not in factors:
            factors[f] = freqForSubstring(f)

"""
t0 = time.time()
for word in examples:
    naive(word, K)
for word in counter_examples:
    naive(word, K)
print(time.time() - t0, "seconds wall time")
"""

t0 = time.time()
sc = SuffixClassifier(examples, counter_examples, set(ALPHABET))
# sc.print_suffix_tree(False)
sc.truncate_tree()
# sc.print_suffix_tree(False)
sc.recalculate(0)
# sc.print_suffix_tree(False)
print(time.time() - t0, "seconds wall time")
