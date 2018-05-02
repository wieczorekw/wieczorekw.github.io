import string
import random

def generate_unique_word(alphabet, size_min, size_max, unique_list):    
    unique_list = [] if unique_list is None else unique_list        
    while True:
        size = random.randint(size_min, size_max)
        str = ''.join(random.choice(alphabet) for c in range(size))
        if str not in unique_list:
            unique_list.append(str)
            return str    

def generate_set(alphabet_size, size_x, size_y, min_w, max_w, X, Y):
    alphabet_max = string.ascii_lowercase+string.ascii_uppercase;

    if len(alphabet_max) < alphabet_size:
        raise Exception('Too big alphabet')

    alphabet = alphabet_max[0:alphabet_size]
    unique_list = []
    X = [] if X is None else X
    Y = [] if Y is None else Y
    for x in range(size_x):
        X.append(generate_unique_word(alphabet, min_w, max_w, unique_list))
    for y in range(size_y):
        Y.append(generate_unique_word(alphabet, min_w, max_w, unique_list))

def generate_test(fn_prefix, alphabet_size, size_x, size_y, min_w, max_w):
    X = []
    Y = []
    generate_set(alphabet_size, size_x, size_y, min_w, max_w, X, Y) 
    with open('{0}_{1}_{2}_{3}_{4}_{5}.txt'.format(fn_prefix, alphabet_size, size_x, size_y, min_w, max_w), 'w') as file1:
      for w in X:
          file1.write(w+'\n')
      file1.write('\n')
      for w in Y:
          file1.write(w+'\n')   

generate_test('randomdata', 2, 10, 10, 1, 10)

generate_test('randomdata', 2, 100, 100, 2, 20)

generate_test('randomdata', 4, 500, 500, 3, 30)

generate_test('randomdata', 4, 1000, 1000, 4, 40)

generate_test('randomdata', 8, 5000, 5000, 5, 50)

generate_test('randomdata', 8, 6000, 6000, 6, 60)

generate_test('randomdata', 16, 7000, 7000, 7, 70)

generate_test('randomdata', 16, 8000, 8000, 8, 80)

generate_test('randomdata', 32, 9000, 9000, 9, 90)

generate_test('randomdata', 32, 10000, 10000, 10, 100)