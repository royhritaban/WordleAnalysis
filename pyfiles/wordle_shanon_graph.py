import matplotlib.pyplot as plt
import csv

with open("venv/04 personal/wordle/data/shanon.csv", "r") as file:
    bit_dataset = csv.reader(file)
    bit_dataset = [[float(_) for _ in line] for line in bit_dataset]

with open("venv/04 personal/wordle/data/wordle_dict.txt", "r") as file:
        wordle_dataset = file.readlines()
        n_words = len(wordle_dataset) #we will be using this a lot
        wordle_dataset = [wordle_dataset[i].strip() for i in range(n_words)] #cleaning up the data


average_shanon_arr = []

#finding best words
for i in bit_dataset:  
    average_shanon_arr.append(sum(i)/5757)
top_word = zip(average_shanon_arr, wordle_dataset)

average_shanon_arr = sorted(average_shanon_arr, reverse=True)
top_word = [(word, "%.2f" % _) for _,word in sorted(top_word, reverse=True)]
print('\n'*2)
counter = 1
for word, bits_gained in reversed(top_word[-10:]):
    print(str(counter)+".", word, bits_gained)
    counter +=1
print('\n'*2)
plt.plot(average_shanon_arr[-100:])
plt.show()