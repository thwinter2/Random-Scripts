from words import words
from typing import List
from itertools import permutations


def count_letters(list_of_words: List[str], letter_counter: dict = {}):
    for word in list_of_words:
        for index, letter in enumerate(word):
            if letter in letter_counter:
                letter_counter[letter][index] += 1
                letter_counter[letter][5] += 1
            else:
                letter_counter[letter] = [0,0,0,0,0,1]
                letter_counter[letter][index] = 1
    return letter_counter


def normalize_letters_counter(counter: dict = {}):
    for counts in counter.values():
        total_count = counts[5]
        for index in range(5):
            counts[index] /= total_count
    return counter


def words_in_list(words: List[str] = [], permutations: List[tuple] = []):
    possible_words: List[str] = []
    for perm in permutations:
        word = ''.join(perm)
        if word in words:
            possible_words.append(word)
    return possible_words


def words_to_enter(words: List[str] = [], sorted_counter: List[tuple] = [], starting_index: int = None, ending_index: int = None):
    letters: List[str] = []
    for letter_counter in sorted_counter[starting_index:ending_index]:
        letters.append(letter_counter[0])
    perms = list(permutations(letters))
    return words_in_list(words, perms)


def find_weighted_words_in_list(words_in_list: List[str] = [], normalized_counter: dict = {}):
    weighted_words = dict()
    for word in words_in_list:
        weight = 0
        for index, letter in enumerate(word):
            weight += normalized_counter[letter][index]
        weighted_words[word] = weight / 5
    return weighted_words


def probability_of_letter_in_wordle(word: str = '', list_of_words: List[str] = []) -> float:
    number_of_words: int = len(list_of_words)
    count_of_letter_in_words: int = 0
    for possible_word in list_of_words:
        for letter in word:
            if letter in possible_word:
                count_of_letter_in_words += 1
                break
    return count_of_letter_in_words / number_of_words


def main():
    counter = count_letters(words)
    counter = normalize_letters_counter(counter)
    sorted_counter = sorted(counter.items(), key=lambda x:x[1][5])
    first_words = words_to_enter(words, sorted_counter, starting_index=-5, ending_index=None)
    weighted_first_words = find_weighted_words_in_list(first_words, counter)
    sorted_first_words = sorted(weighted_first_words, key=lambda x:x[1])
    first_word = sorted_first_words[0]
    first_word_probability = probability_of_letter_in_wordle(first_word, words)

    second_words = words_to_enter(words, sorted_counter, starting_index=-10, ending_index=-5)
    weighted_second_words = find_weighted_words_in_list(second_words, counter)
    sorted_second_words = sorted(weighted_second_words, key=lambda x:x[1])
    second_word: str = sorted_second_words[0]
    second_word_probability = probability_of_letter_in_wordle(first_word + second_word, words)

    print(f"First Words: {first_words}")
    print(f"Second Words: {second_words}")
    print(f"First Word: \"{first_word}\" with a probability of a letter in wordle of {format(100*first_word_probability, '.2f')}%")
    print(f"Second Word: \"{second_word}\" with a probability of a letter in wordle of {format(100*second_word_probability,'.2f')}%")

if __name__ == "__main__":
    main()