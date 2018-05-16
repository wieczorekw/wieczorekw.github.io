from suffix_classifier import SuffixClassifier
from sequence_evaluation import seqEval
from fractions import Fraction
import random

NUMBER_OF_D_plus = 200
NUMBER_OF_D_minus = 200
ALPHABET = ['a', 'b', 'c']
MIN_LEN = 6
MAX_LEN = 30
NUMBER_OF_TESTS = 50
K = 4

random.seed()

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

def scount(s, w, k):
    c = 0
    n = len(s)
    for i in range(n - k + 1):
        for j in range(k):
            if s[i + j] != w[j]:
                break
        else:
            c += 1
    return c

def naiveSeqEval(string, k):
    global examples, counter_examples

    def freqForSubstring(w):
        n_plus, n_minus = 0, 0
        for s in examples:
            n_plus += scount(s, w, k)
        for s in counter_examples:
            n_minus += scount(s, w, k)
        if n_plus + n_minus == 0:
            return None
        else:
            return Fraction(n_plus, n_plus + n_minus)

    sum = Fraction(0, 1)
    counter = 0
    n = len(string)
    for pos in range(n - k + 1):
        f = freqForSubstring(string[pos : pos + k])
        if f != None:  # allowed to be 0
            counter += 1
            sum += f
    return sum / counter if counter else 0


sc = SuffixClassifier(examples, counter_examples, set(ALPHABET))
# sc.print_suffix_tree(False)
sc.truncate_tree()
# sc.print_suffix_tree(False)
sc.recalculate(0)
# sc.print_suffix_tree(False)

went_wrong = False
for step in range(NUMBER_OF_TESTS):
    test_word = randomWord(MIN_LEN, MAX_LEN)
    naive_result = naiveSeqEval(test_word, K)
    sc_result = seqEval(test_word, sc, K)
    if naive_result != sc_result:
        print(test_word)
        print("naive_result", naive_result)
        print("sc_result", sc_result)
        print("examples")
        print(examples)
        print("counter examples")
        print(counter_examples)
        went_wrong = True
        break
    else:
        print(step + 1, test_word, naive_result, sc_result)
print("OK" if not went_wrong else "")
