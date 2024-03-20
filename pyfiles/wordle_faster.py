from multiprocessing import Pool
import csv, math, time
from functools import partial
from collections import Counter


def exclude(wordstring, bitstring, possible_words):

    # excluded_words stores words to be removed from possible words
    excluded_words = set()

    # forming relation between wordle color / bit and respective character, for effective usage
    char_bit = [(wordstring[i], bitstring[i]) for i in range(len(wordstring))]

    for i in range(len(char_bit)):
        (char, bit) = char_bit[i]

        char_multiple = char_bit.count((char, "1")) + char_bit.count(
            (char, "2")
        )  # says n instances of some character exists
        char_does_not_exist = (
            char,
            "0",
        ) in char_bit  # says there can't be more than n instances of that character

        # character repition information
        if char_does_not_exist and char_multiple != 0:  # exactly
            excluded_words = excluded_words.union(
                {word for word in possible_words if word.count(char) != char_multiple}
            )
        elif char_multiple > 1:  # atleast
            excluded_words = excluded_words.union(
                {word for word in possible_words if word.count(char) < char_multiple}
            )

        if bit == "0" and char_multiple == 0:  # grey
            excluded_words = excluded_words.union(
                {word for word in possible_words if char in word}
            )
        elif bit == "1":  # yellow
            excluded_words = excluded_words.union(
                {word for word in possible_words if char not in word or word[i] == char}
            )
        elif bit == "2":  # green
            excluded_words = excluded_words.union(
                {word for word in possible_words if word[i] != char}
            )
    return [word for word in possible_words if word not in excluded_words]


def wordle_response(answer, guess):
    bit_string = ""
    for i in range(len(guess)):
        guess_char = guess[i]
        if guess_char == answer[i] and answer.count(guess_char) >= guess[: i + 1].count(
            guess_char
        ):
            bit_string += "2"
        elif guess_char in answer and answer.count(guess_char) >= guess[: i + 1].count(
            guess_char
        ):
            bit_string += "1"
        else:
            bit_string += "0"
    return bit_string


def shanon_bits(bitstring, guess, wordle_dataset):
    n_words = 5727
    outcomes = len(exclude(guess, bitstring, wordle_dataset))
    # if outcomes == 0:
    # return "ERROR"
    return -math.log2(outcomes / n_words)


if __name__ == "__main__":
    # loading wordle dataset
    with open("venv/04 personal/wordle/data/wordle_dict.txt", "r") as file:
        wordle_dataset = file.readlines()
        n_words = len(wordle_dataset)  # we will be using this a lot
        wordle_dataset = [
            wordle_dataset[i].strip() for i in range(n_words)
        ]  # cleaning up the data

    with open("venv/04 personal/wordle/data/wordle_bit_output.csv", "r") as file:
        bit_dataset = csv.reader(file)
        bit_dataset = [[_ for _ in line] for line in bit_dataset]

    # 1 guess per row
    shanon_count_for_guess = [None for _ in range(n_words)]
    i = 0
    for guess in wordle_dataset:
        # answers along rows
        bit_dataset_row = [wordle_response(answer, guess) for answer in wordle_dataset]
        bit_count_list = list(Counter(bit_dataset_row).items())

        # splitting up counts and bits for multiprocessing
        bit_list = []
        count_list = []
        for bit, count in bit_count_list:
            bit_list.append(bit)
            count_list.append(count)

        # constructing a partial function to use multiprocessing
        shanon_bits_partial = partial(shanon_bits, wordle_dataset=wordle_dataset)
        with Pool(processes=7) as p:
            row_result = p.starmap(
                shanon_bits_partial, zip(bit_list, [guess] * len(bit_list))
            )

        shanon_count_for_guess[i] = list(zip(row_result, count_list))
        """ 
        #code without multiprocessing
        row_shannon_tuple_list = [
            (shanon_bits(bit_response, guess,  wordle_dataset), count)
            for (bit_response, count) in bit_count_list
        ]
        """
        # shanon_count_for_guess.append(row_shannon_tuple_list)

        if i % 50 == 0:
            print(i * 0.01737015806)
        i += 1
    with open(
        "venv/04 personal/wordle/data/shanon_fast.csv", "w", newline=""
    ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(shanon_count_for_guess)
