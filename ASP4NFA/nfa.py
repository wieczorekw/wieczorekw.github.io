from subprocess import Popen, PIPE
from pipetools import where
from FAdo.fa import *
import argparse
import time
import sys
import re

param_t = False

def readWords(file_name):
    """From Abbadingo competition format
    """
    positives = set()
    negatives = set()
    with open(file_name, encoding='utf-8') as file:
        it = iter(file)
        line = next(it)
        number_of_words = int(line.split()[0])
        for _ in range(number_of_words):
            line = next(it)
            cls, length, *symbols = line.split()
            s = "".join(symbols)
            if cls == '1':
                positives.add(s)
            else:
                negatives.add(s)
    assert len(positives & negatives) == 0
    return positives, negatives

def all_proper_prefixes(S):
    result = set()
    for s in S:
        n = len(s)
        if n > 0:
          result.update(s[:i] for i in range(1, n + 1))
    return result

def encode(X, Y, K, P, alphabet):
    lines = []
    lines.append("num(0..{}).".format(K - 1))
    lines.append("pref(lambda).")
    for p in P:
        lines.append("pref({}).".format(p))
    lines += [ \
    "x(P, N) :- pref(P), num(N), not not_x(P, N).", \
    "not_x(P, N) :- pref(P), num(N), not x(P, N).", \
    "has_num(P) :- pref(P), num(N), x(P, N).", \
    ":- pref(P), not has_num(P).", \
    "final(N) :- num(N), not not_final(N).", \
    "not_final(N) :- num(N), not final(N)."]
    for char in alphabet:
        lines.append("f{}(Q, R) :- num(Q), num(R), not not_f{}(Q, R).".format(char, char))
        lines.append("not_f{}(Q, R) :- num(Q), num(R), not f{}(Q, R).".format(char, char))
    lines.append(":- not x(lambda, 0).")
    for k in range(1, K):
        lines.append(":- x(lambda, {}).".format(k))
    ind = 0
    for p in P | {''}:
        for q in P:
            if p == q[:-1]:
                _p = "lambda" if p == '' else p
                lines.append("x({}, R) :- num(Q), num(R), x({}, Q), f{}(Q, R).".format(q, _p, q[-1]))
                for i in range(K):
                    for j in range(K):
                        ind += 1
                        lines.append("c{} :- x({}, {}), f{}({}, {}).".format(ind, _p, j, q[-1], j, i))
                    body = ":- x({}, {})".format(q, i)
                    for m in range(ind - K + 1, ind + 1):
                        body += ", not c{}".format(m)
                    body += "."
                    lines.append(body)
    if '' in Y:
        lines.append(":- final(0).")
    for sm in Y - {''}:
        lines.append(":- num(N), x({}, N), final(N).".format(sm))
    if '' in X:
        lines.append(":- not final(0).")
    ind = 0
    for sp in X - {''}:
        for j in range(K):
            ind += 1
            lines.append("g{} :- x({}, {}), final({}).".format(ind, sp, j, j))
        body = ":- "
        for m in range(ind - K + 1, ind):
            body += "not g{}, ".format(m)
        body += "not g{}.".format(ind)
        lines.append(body)
    return "\n".join(lines)

def extract(line, K, alphabet):
    aut = NFA()
    for j in range(K):
        aut.addState()
    aut.addInitial(0)
    for state in map(int, re.findall("(?<=\sfinal\()\d+", line)):
        aut.addFinal(state)
    for char in alphabet:
        for (q, r) in map(eval, re.findall("(?<=\sf{})\(\d+,\d+\)".format(char), line)):
            aut.addTransition(q, char, r)
    return aut

def synthesize(X, Y, K):
    global param_t
    P = all_proper_prefixes(X | Y)
    alphabet = set(c for s in X | Y for c in s)
    asp_code = encode(X, Y, K, P, alphabet)
    with open("code.asp", "w") as text_file:
        print(asp_code, file=text_file)
    p1 = Popen(["gringo", "code.asp"], stdout=PIPE)
    if param_t:
        p2 = Popen(["clasp", "-t", "16"], stdin=p1.stdout, stdout=PIPE)
    else:
        p2 = Popen(["clasp"], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()
    text = p2.communicate()[0]
    text = text.decode()
    aut = None
    for line in text.splitlines(False) > where(r'^(pref|num)'):
        aut = extract(line, K, alphabet)
        break
    return aut

def printAut(a):
    print("An automaton with {} states:".format(len(a)))
    print(a.Initial)
    print(a.Final)
    print(a.delta)

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='an input file in Abbadingo format', type=str, default="train.txt")
parser.add_argument('--threads', help='use 16 threads', nargs='?', const=True, default=False)
args = parser.parse_args()
print('Working with file: {fileName}'.format_map({ 'fileName': args.file }))
param_t = args.threads
print('Using threads:', param_t)
X, Y = readWords(args.file)

if X & Y:
    print("Common words:", X & Y)
    sys.exit()

whole_time = time.time()
NSTATES = 2
while True:
    print("{}".format(NSTATES))
    a = synthesize(X, Y, NSTATES)
    if a:
        break
    NSTATES += 1
# a.deleteStates(set(range(len(a))) - a.usefulStates())
printAut(a)
print("Błędy dla pozytywnych:")
for x in X:
    if not a.evalWordP(x):
        print(x if x != '' else "epsilon", end = ' ')
print("\nBłędy dla negatywnych:")
for y in Y:
    if a.evalWordP(y):
        print(y if y != '' else "epsilon", end = ' ')
print('')
print("Pełny czas = %.2f s" % (time.time() - whole_time))
