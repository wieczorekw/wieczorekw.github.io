import subprocess
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
    lines.append("q(0..{}).".format(K - 1))
    for a in alphabet:
        lines.append(f"symbol({a}).")
    lines.append("prefix(lambda).")
    for p in P:
        lines.append("prefix({}).".format(p))
    for s in X:
        if s == "":
            lines.append("positive(lambda).")
        else:
            lines.append(f"positive({s}).")
    for s in Y:
        if s == "":
            lines.append("negative(lambda).")
        else:
            lines.append(f"negative({s}).")
    for p in P:
        n = len(p)
        if n >= 2:
            pivot = n-1
            b, c = p[:pivot], p[pivot:]
            lines.append(f"join({b}, {c}, {p}).")
        else:
            lines.append(f"join(lambda, {p}, {p}).")
    return "\n".join(lines)

def extract(line, K):
    aut = NFA()
    for j in range(K):
        aut.addState()
    aut.addInitial(0)
    for state in map(int, re.findall("(?<=final\()\d+", line)):
        aut.addFinal(state)
    for s in re.findall("(?<=delta)\(\d+,\w,\d+\)", line):
        q, a, r = s[1:-1].split(',')
        aut.addTransition(int(q), a, int(r))
    return aut

def synthesize(X, Y, K):
    global param_t
    P = all_proper_prefixes(X | Y)
    alphabet = set(c for s in X | Y for c in s)
    asp_facts = encode(X, Y, K, P, alphabet)
    with open("facts.lp", "w") as text_file:
        print(asp_facts, file=text_file)
    if param_t:
        process = subprocess.run(['clingo', '-t', '16', 'nfa.lp'], stdout=subprocess.PIPE)
    else:
        process = subprocess.run(['clingo', 'nfa.lp'], stdout=subprocess.PIPE)
    text = process.stdout
    text = text.decode()
    aut = None
    for line in text.splitlines(False) > where(r'^(delta|final)'):
        aut = extract(line, K)
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
print("Errors for positives:")
for x in X:
    if not a.evalWordP(x):
        print(x if x != '' else "epsilon", end = ' ')
print("\nErrors for negatives:")
for y in Y:
    if a.evalWordP(y):
        print(y if y != '' else "epsilon", end = ' ')
print('')
print("Total time = %.2f s" % (time.time() - whole_time))
