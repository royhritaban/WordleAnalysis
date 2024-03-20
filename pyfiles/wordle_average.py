from multiprocessing import Pool
import csv, math, time
from functools import partial
from collections import Counter
from operator import itemgetter


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

    with open("venv/04 personal/wordle/data/shanon_fast.csv", "r") as file:
        bit_dataset = csv.reader(file)
        bit_dataset = [[_ for _ in line] for line in bit_dataset]

    # 1 guess per row
    shanon_count_for_guess = [None for _ in range(n_words)]
    i = 0
    # shanon tuple values for every guess
    for shanon_row_of_guess in bit_dataset:  # shanon tuple values for every guess
        shanon_sum = 0
        count_sum = 0
        for shanon_count in shanon_row_of_guess:  # going through each tuple
            # string csv to tuple
            shanon_count = shanon_count.split(",")
            shanon = shanon_count[0][1:]
            count = shanon_count[1][:-1]
            shanon_sum += float(shanon) * int(count)
        average_shanon = shanon_sum / n_words
        shanon_count_for_guess[i] = (wordle_dataset[i], average_shanon)
        i += 1
    shanon_count_for_guess.sort(key=lambda tup: tup[1], reverse=True)
    print(shanon_count_for_guess[:10])
    with open(
        "venv/04 personal/wordle/data/n1_performance_sorted.csv", "w", newline=""
    ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(shanon_count_for_guess)
