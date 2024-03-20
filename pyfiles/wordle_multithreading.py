import random
import math
import csv
from multiprocessing import Pool

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

def wordle_response(answer_guess_tuple):
    answer, guess = answer_guess_tuple
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

if __name__ == '__main__':
    #preprocessing dataset
    infile = open("venv/04 personal/wordle/data/wordle_dict.txt", "r")
    wordle_dataset = infile.readlines()
    infile.close()

    n_words = len(wordle_dataset)
    
    for i in range(n_words):
        wordle_dataset[i] = wordle_dataset[i].strip()

    counter = 0
    new_list = [None for _ in range(n_words)]
    #word_guess = "slate"
    n_by_n_list = [[(rows,cols) for rows in wordle_dataset] for cols in wordle_dataset]
    #n_by_n_wordle_bit = [[wordle_response(answer, guess) for answer in wordle_dataset] for guess in wordle_dataset]
    for rows in n_by_n_list:
        n_row = []
        with Pool(processes=5) as p:
            #print(rows)
            n_row =  p.map(wordle_response, rows, chunksize=5)
        new_list[counter] = n_row
        counter += 1
        print(counter/n_words*100, counter)
    with open('venv/04 personal/projects/wordle_bit_output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_list)    
    #print(n_by_n_list)




'''
for i in range(len(wordle_dataset)):
    word_answer = wordle_dataset[i]
    for j in range(len(wordle_dataset)):
        word_guess = wordle_dataset[j]
        wordle_bit_string = wordle_response(word_answer, word_guess)
        #print(word_guess, wordle_bit_string)
        line_list = exclude(word_guess, wordle_bit_string, wordle_dataset)
        probability = len(line_list)/n_words
        bits_gained = shanon_bits(probability)
        n_by_n_list[i][j] = bits_gained
        #print("Bits gained=", n_by_n_list[i][j], round(i/n_words*100,2), "%")
    print(round(i/n_words*100,2),"%")
    if (i+1)%10==0: #store n by n every 10 computed answers
        with open('venv/04 personal/projects/output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(n_by_n_list)
 '''       

