import re
# import nltk.corpus
import numpy as np
# from itertools import chain

'''Create dictionary'''
d_list = []
with open("google-10000-english.txt") as dictionary:
    for line in dictionary:
        d_list.append(line.strip())

'''Create first paragraph of Jane Austen txt as a list of strings'''
text_list = []
with open("austen-sense-corrupted.txt") as text:
    for line in text:
        text_list.append(line)

austen_list = []
for i in text_list:
    austen_list.append(i.strip())

nested_list = []
for x in austen_list:
    nested_list.append(x.split(" "))

final_list = [item for sublist in nested_list for item in sublist]
# first paragraph
final_list = final_list[12:223]
# 12:223
# print(final_list)

'''Calculate minimum levenshtein distance between two word'''
def levenshtein_matrix(corruptedWord, correctedWord):
    # create empty matrix
    distances = np.zeros((len(corruptedWord) + 1, len(correctedWord) + 1), dtype = int)
    
    # initialize first row and column
    for w1 in range(1, len(corruptedWord) + 1):
        distances[w1][0] = w1
    for w2 in range(1, len(correctedWord) + 1):
        distances[0][w2] = w2

    for row in range(1, len(corruptedWord) + 1):
        for col in range(1, len(correctedWord) + 1):
            # calculate substitution cost
            if corruptedWord[row - 1] == correctedWord[col - 1]:
                sub_cost = 0
            else:
                sub_cost = 1
            # calculate minimum cost
            distances[row][col] = min(distances[row-1][col] + 1, distances[row-1][col-1] + sub_cost, distances[row][col-1] + 1)

    return distances[len(corruptedWord)][len(correctedWord)]

# print(levenshtein_matrix("estete", "estate"))

''' Takes a list of words and compare against dictionary. Returns word with shortest levenshtein distance'''
def correct_word(word, dictionary):
    min_dist = None
    for j in dictionary:
        current_dist = levenshtein_matrix(word, j)
        if (min_dist is None) or (current_dist <= min_dist):
            min_dist = current_dist
            current_word = j
    return current_word

'''Return list of corrected words from Jane Austen text
- If previous word ends with period, check capitalized word
- If not, pass
- If word[-1] is punctuation, remove punctuation, correct word, add punctuation
'''

def string_match(word_list, dictionary):
    corrected_story = []
    for i in word_list:
        if i in dictionary or i == "":
            corrected_story.append(i)
        elif re.findall(r"\w+[\.\,\;]$", i):
            punc = i[-1]
            only_word = i.replace(punc, "")
            c_word = correct_word(only_word, dictionary)
            corrected_story.append(c_word + punc)
        elif i[0].isupper() == True:
            corrected_story.append(i)
        else:
            corrected_story.append(correct_word(i, dictionary))
    return corrected_story

print(string_match(final_list, d_list))

'''Return final single string of story'''
def corrected_string(correct_story):
    final_story = ""
    for i in correct_story:
        final_story += str(i) + " "
    final_story = final_story[:-1]
    return final_story

# print(corrected_string(string_match(final_list, d_list)))

    




