import random
import math
import csv
from multiprocessing import Pool

import time

def exclude(wordstring, bitstring, arr):
    excluded_list = []
    char_bit = [(wordstring[i], bitstring[i]) for i in range(len(wordstring))]
    for i in range(len(char_bit)):
        (char,bit) = char_bit[i]

        n_bit = char_bit.count((char,'1'))+char_bit.count((char,'2')) #says n instances of some character exists
        n_0_bit = char_bit.count((char,'0')) #says there can't be more than n instances of that character
        
        #character repition information
        if n_0_bit != 0 and n_bit != 0:#exactly
            excluded_list.extend([word for word in arr if word.count(char)!=n_bit])
        elif n_bit > 1:#atleast
            excluded_list.extend([word for word in arr if word.count(char)<n_bit])
    
        if bit == '0' and n_bit==0: #grey
            excluded_list.extend([word for word in arr if char in word])
        elif bit == '1': #yellow
            excluded_list.extend([word for word in arr if char not in word or word[i]==char])
        elif bit == '2': #green
            excluded_list.extend([word for word in arr if word[i] != char])
    return [word for word in arr if word not in excluded_list]

def exclude_v_set(wordstring, bitstring, arr):
    excluded_list = set()
    char_bit = [(wordstring[i], bitstring[i]) for i in range(len(wordstring))]
    for i in range(len(char_bit)):
        (char,bit) = char_bit[i]

        n_bit = char_bit.count((char,'1'))+char_bit.count((char,'2')) #says n instances of some character exists
        n_0_bit = char_bit.count((char,'0')) #says there can't be more than n instances of that character
        
        #character repition information
        if n_0_bit != 0 and n_bit != 0:#exactly
            excluded_list = excluded_list.union({word for word in arr if word.count(char)!=n_bit})
        elif n_bit > 1:#atleast
            excluded_list = excluded_list.union({word for word in arr if word.count(char)<n_bit})
    
        if bit == '0' and n_bit==0: #grey
            excluded_list = excluded_list.union({word for word in arr if char in word})
        elif bit == '1': #yellow
            excluded_list = excluded_list.union({word for word in arr if char not in word or word[i]==char})
        elif bit == '2': #green
            excluded_list = excluded_list.union({word for word in arr if word[i] != char})
    return [word for word in arr if word not in excluded_list]

def wordle_response(answer, guess):
    bit_string = ""
    for i in range(len(guess)):
        guess_char  = guess[i]
        if guess_char == answer[i] and answer.count(guess_char)>=guess[:i+1].count(guess_char):
            bit_string += '2'
        elif guess_char in answer and answer.count(guess_char)>=guess[:i+1].count(guess_char):
            bit_string += '1'
        else:
            bit_string += '0'
    return bit_string

def shanon_bits(probability):
    return -math.log2(probability)


infile = open("venv/04 personal/projects/wordle_dict.txt", "r")
line_list = infile.readlines()
line_list_len = len(line_list)
for line_number in range(line_list_len):
    line_list[line_number] = line_list[line_number].strip()


benchmark_ansewr_list = [
    'chest', 'layer', 'whale', 'minor', 'faith', 'tests', 'judge', 'items', 'worry', 'waste',
    'hoped', 'strip', 'begun', 'aside', 'lakes', 'bound', 'depth', 'candy', 'event', 'worse',
    'aware', 'shell', 'rooms', 'ranch', 'image', 'snake', 'aloud', 'dried', 'likes', 'motor',
    'pound', 'knees', 'refer', 'fully', 'chain', 'shirt', 'flour', 'drops', 'spite', 'orbit',
    'banks', 'shoot', 'curve', 'tribe', 'tight', 'blind', 'slept', 'shade', 'claim', 'flies',
    'theme', 'queen', 'fifth', 'union', 'hence', 'straw', 'entry', 'issue', 'birth', 'feels',
    'anger', 'brief', 'rhyme', 'glory', 'guard', 'flows', 'flesh', 'owned', 'trick', 'yours',
    'sizes', 'noted', 'width', 'burst', 'route', 'lungs', 'uncle', 'bears', 'royal', 'kings',
    'forty', 'trial', 'cards', 'brass', 'opera', 'chose', 'owner', 'vapor', 'beats', 'mouse',
    'tough', 'wires', 'meter', 'tower', 'finds', 'inner', 'stuck', 'arrow', 'poems', 'label',
    'swing', 'solar', 'truly', 'tense', 'beans', 'split', 'rises', 'weigh', 'hotel', 'stems',
    'pride', 'swung', 'grade', 'digit', 'badly', 'boots', 'pilot', 'sales', 'swept', 'lucky',
    'prize', 'stove', 'tubes', 'acres', 'wound', 'steep', 'slide', 'trunk', 'error', 'porch',
    'slave', 'exist', 'faced', 'mines', 'marry', 'juice', 'raced', 'waved', 'goose', 'trust',
    'fewer', 'favor', 'mills', 'views', 'joint', 'eager', 'spots', 'blend', 'rings', 'adult',
    'index', 'nails', 'horns', 'balls', 'flame', 'rates', 'drill', 'trace', 'skins', 'waxed',
    'seats', 'stuff', 'ratio', 'minds', 'dirty', 'silly', 'coins', 'hello', 'trips', 'leads',
    'rifle', 'hopes', 'bases', 'shine', 'bench', 'moral', 'fires', 'meals', 'shake', 'shops',
    'cycle', 'movie', 'slope', 'canoe', 'teams', 'folks', 'fired'
]

#benchmark_ansewr_list = ['chest']
flag = True
# benchmarking control
shanon_nxn = [[None for _ in range(line_list_len)] for _ in range(line_list_len)]
nxn_bitstring = []
with open("venv/04 personal/projects/wordle_bit_output.csv", "r") as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        nxn_bitstring.append(row)

'''
for word_answer in benchmark_ansewr_list:
    print(word_answer)
    possible_words = line_list
    flag = True
    bit_string=""
    while len(possible_words) > 0 and bit_string != "22222":
        if flag:
            flag = False
            word_guess = "slate"
        bit_string = wordle_response(word_answer, word_guess)
        print(word_answer, word_guess, bit_string)

        possible_words = exclude_v_set(word_guess, bit_string, possible_words)
        word_guess = possible_words[0]
'''

start_time = time.time()
i = j = 0
for word_answer in line_list[:10]:
    j = 0
    for word_guess in line_list[:10]:
        bit_string = nxn_bitstring[j][i]
        #print(word_answer, word_guess, bit_string)
        probability = (len(exclude_v_set(word_guess, bit_string, line_list))/line_list_len)
        bits_gained = shanon_bits(probability)
        shanon_nxn[i][j] = bits_gained
        j+=1
    print(f'{i/line_list_len*100:.4f}')
    i+=1
print(f'=> time is {time.time() - start_time:.4f}')

start_time = time.time()
i = j = 0
for word_answer in line_list[:10]:
    j = 0
    for word_guess in line_list[:10]:
        bit_string = wordle_response(word_answer, word_guess)
        #print(word_answer, word_guess, bit_string)
        probability = (len(exclude_v_set(word_guess, bit_string, line_list))/line_list_len)
        bits_gained = shanon_bits(probability)
        shanon_nxn[i][j] = bits_gained
        j+=1
    #print(f'{i/line_list_len*100:.4f}')
    i+=1
print(f'=> time is {time.time() - start_time:.4f}')