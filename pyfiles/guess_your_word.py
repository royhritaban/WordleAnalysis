import random
import math

def exclude3(wordstring, bitstring, arr):
    excluded_list = []
    char_bit = [(wordstring[i], bitstring[i]) for i in range(len(wordstring))]
    for i in range(len(char_bit)):
        (char,bit) = char_bit[i]

        n_bit = char_bit.count((char,'1'))+char_bit.count((char,'2'))
        n_0_bit = char_bit.count((char,'0'))
        #print(n_0_bit, n_bit)
        #print(n_bit, n_0_bit, char_bit)
        
        if n_0_bit != 0 and n_bit != 0:#exactly
            print("=>",wordstring, bit_string, char, "EXACTLY", n_bit)
            excluded_list.extend([word for word in arr if word.count(char)!=n_bit])
        elif n_bit > 1:#atleast
            print("=>",wordstring, bit_string, char, "atleast", n_bit)
            excluded_list.extend([word for word in arr if word.count(char)<n_bit])
    
        if bit == '0' and n_bit==0: #grey
            excluded_list.extend([word for word in arr if char in word])
        elif bit == '1': #yellow
            excluded_list.extend([word for word in arr if char not in word or word[i]==char])
        elif bit == '2': #green
            excluded_list.extend([word for word in arr if word[i] != char])
#print(len(excluded_list))
    return [word for word in arr if word not in excluded_list]

def wordle_response(answer, guess):
    #char_bit = [None for _ in range(len(guess))]
    bit_string = ""
    for i in range(len(guess)):
        guess_char  = guess[i]
        if guess_char == answer[i] and answer.count(guess_char)>=guess[:i+1].count(guess_char):
            #char_bit[i] = [guess[i], 2]
            bit_string += '2'
        elif guess_char in answer and answer.count(guess_char)>=guess[:i+1].count(guess_char):
            #print(answer[:i], answer[:i].count(guess_char), guess[:i], guess[:i].count(guess_char))
            #char_bit[i] = [guess[i], 1]
            bit_string += '1'
        else:
            #char_bit[i] = [guess[i], 0]
            bit_string += '0'

    return bit_string

infile = open("venv/04 personal/projects/wordle_dict.txt", "r")
line_list = infile.readlines()
line_list_len = len(line_list)
for line_number in range(line_list_len):
    line_list[line_number] = line_list[line_number].strip()

word_answer= "penis"
bit_string=""
flag = True

while len(line_list) > 0 and bit_string != "22222":
        #for i in range(10):
        if flag:
            #word_guess = input("\nEnter attempted word: ")
            flag = False
            word_guess = "slate"
        bit_string = wordle_response(word_answer, word_guess)
        print(word_guess, bit_string)
        line_list = exclude3(word_guess, bit_string, line_list)
        #print(line_list, "\n=>>>", word_guess)
        word_guess = line_list[0]
        probability = 1/len(line_list) * 100


infile.close()