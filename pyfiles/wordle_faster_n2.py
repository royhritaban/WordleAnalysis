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

    with open("venv/04 personal/wordle/data/n1_performance_sorted.csv", "r") as file:
        bit_dataset = csv.reader(file)
        n1_sorted_dataset = [line for line in bit_dataset]

    # 1 guess per row
    shanon_count_for_guess = []
    i = 0
    for guess in n1_sorted_dataset:
        # answers along rows
        bit_dataset_row = [wordle_response(answer, guess) for answer in wordle_dataset]
        bit_count_list = list(Counter(bit_dataset_row).items())

        # splitting up counts and bits for multiprocessing
        bit_list = []
        count_list = []

        average_performance_n2 = {}
        # we look at each case of restriction
        for bit, count in bit_count_list:
            bit_list.append(bit)
            count_list.append(count)

            restricted_worlde_dataset = exclude(guess, bit, wordle_dataset)

            # evaluate all guesses in that restriction
            shanon_bits_partial = partial(
                shanon_bits, wordle_dataset=restricted_worlde_dataset
            )

            for guess_n2 in restricted_worlde_dataset:
                average_performance_n2[guess_n2] = []
                bit_list_n2 = []
                count_list_n2 = []

                # wordle responses for guess_n2 guess in restricted domain
                bit_dataset_row_n2 = [
                    wordle_response(answer_n2, guess_n2)
                    for answer_n2 in restricted_worlde_dataset
                ]
                bit_count_list_n2 = list(Counter(bit_dataset_row_n2).items())

                # splitting tuple for multiprocessing
                for bit_n2, count_n2 in bit_count_list_n2:
                    bit_list_n2.append(bit_n2)
                    count_list_n2.append(count_n2)

                # constructing a partial function to use multiprocessing
                with Pool(processes=7) as p:
                    shanon_result_for_guess = p.starmap(
                        shanon_bits_partial,
                        zip(bit_list_n2, [guess_n2] * len(bit_list_n2)),
                    )

                # calculating average sharon bit for current guess
                shanon_average = sum(
                    [
                        (count_list_n2[k] * shanon_result_for_guess[k])
                        for k, _ in enumerate(count_list_n2)
                    ]
                ) / sum(count_list_n2)
                average_performance_n2[guess_n2].append(shanon_average * count)

        average_performance_n2_list = []
        for word in wordle_dataset:
            if len(average_performance_n2[word]) != 0:
                average_performance_n2_list.append(
                    (word, (sum(average_performance_n2[word]) / n_words)),
                )

        average_performance_n2_list.sort(key=lambda tup: tup[1], reverse=True)
        shanon_count_for_guess.append(average_performance_n2_list)
        print(guess, shanon_count_for_guess[:10])
        print("WEEWOO", i)
        i += 1
        # shanon_count_for_guess.append(row_shannon_tuple_list)
        with open(
            "venv/04 personal/wordle/data/shanon_n2.csv", "w", newline=""
        ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(shanon_count_for_guess)
