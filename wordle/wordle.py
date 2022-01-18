from words import words
from itertools import permutations


# Count of letter appearance for each index in wordle. Last index is total count.
def count_letters(list_of_words: list[str], letter_counter: dict = {}):
    for word in list_of_words:
        for index, letter in enumerate(word):
            if letter in letter_counter:
                letter_counter[letter][5] += 1
                letter_counter[letter][index] += 1
            else:
                letter_counter[letter] = [0,0,0,0,0,1]
                letter_counter[letter][index] = 1
    return letter_counter


# Set indeces [0:5] of counter values to percentage weight of the letter occurring in that index
def normalize_letters_counter(counter: dict = {}) -> None:
    for counts in counter.values():
        total_count = counts[5]
        for index in range(5):
            counts[index] /= total_count
    return


# Check which of all possible permutations of the letters exist in the wordle list
def words_in_list(words: list[str] = [], permutations: list[tuple] = []) -> list[str]:
    possible_words: list[str] = []
    for perm in permutations:
        word = ''.join(perm)
        if word in words:
            possible_words.append(word)
    return possible_words


# Caculate the average weight of each permutation that exists in the wordle list
def find_weighted_words_in_list(words_in_list: list[str] = [], normalized_counter: dict = {}) -> dict:
    weighted_words = dict()
    for word in words_in_list:
        weight = 0
        for index, letter in enumerate(word):
            weight += normalized_counter[letter][index]
        weighted_words[word] = weight / 5
    return weighted_words


# Sort possible words based on average weight and return word with the greatest weight
def find_best_word(words: list[str] = [], sorted_counter: list[tuple] = [], starting_index: int = None, ending_index: int = None) -> str:
    letters: list[str] = []
    for letter_counter in sorted_counter[starting_index:ending_index]:
        letters.append(letter_counter[0])
    perms = list(permutations(letters))
    possible_words: list[str] = words_in_list(words, perms)
    weighted_words: dict = find_weighted_words_in_list(possible_words, dict(sorted_counter))
    sorted_weighted_words: list[str] = sorted(weighted_words, key=lambda x:x[1])
    return sorted_weighted_words[0]


# Return the probablity of having at least one letter exist in the wordle by inputting a given word
def probability_of_letter_in_wordle(word: str = '', list_of_words: list[str] = []) -> float:
    number_of_words: int = len(list_of_words)
    count_of_letter_in_words: int = 0
    for possible_word in list_of_words:
        for letter in word:
            if letter in possible_word:
                count_of_letter_in_words += 1
                break
    return float(count_of_letter_in_words) / number_of_words


def main():
    counter = count_letters(words)
    normalize_letters_counter(counter)
    sorted_counter = sorted(counter.items(), key=lambda x:x[1][5])
    
    first_word = find_best_word(words, sorted_counter, starting_index=-5, ending_index=None)
    first_word_probability: float = probability_of_letter_in_wordle(first_word, words)

    second_word = find_best_word(words, sorted_counter, starting_index=-10, ending_index=-5)
    second_word_probability = probability_of_letter_in_wordle(first_word + second_word, words)

    print(f"First Word: \"{first_word}\" with the probability of a letter in wordle of {format(100*first_word_probability, '.2f')}%")
    print(f"Second Word: \"{second_word}\" with the probability of a letter in wordle of {format(100*second_word_probability,'.2f')}%")

if __name__ == "__main__":
    main()
