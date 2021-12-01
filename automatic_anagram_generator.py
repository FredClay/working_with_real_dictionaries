"""Accepts a user phrase/name and returns possible anagram phrases."""
import sys
from collections import Counter
import time


def loader(file):
    """Opens a dic.txt file and returns a list of strings."""
    try:
        with open(file, encoding='UTF-8') as in_file:
            loaded_text = in_file.read().strip().split('\n')
            loaded_text = list(map(lambda x: x.lower(), loaded_text))
            return loaded_text
    except IOError as err:
        print(f"{err}: No dictionary file found at path - {file}...")
        sys.exit(1)


def dic_shortener(dic_words, spaceless_user_phrase):
    """Eliminates all words from the dictionary that are neither anagrams
    nor subsets of initial user phrase."""
    ok_words = []
    user_counter = Counter(spaceless_user_phrase)
    for word in dic_words:
        ok = True
        word_counter = Counter(word)
        for letter in word:
            if word_counter[letter] > user_counter[letter]:
                ok = False
        if ok:
            ok_words.append(word)
    return ok_words


def dic_word_searcher(dic_words, spaceless_user_phrase):
    """Returns a list of all possible words when given a user phrase."""
    user_counter = Counter(spaceless_user_phrase)
    finished_list = []
    continuing_list = []
    for word in dic_words:
        word_counter = Counter(word)
        if word_counter == user_counter:
            finished_list.append(word)
            continue

        ok = True
        for letter in word:
            if word_counter[letter] > user_counter[letter]:
                ok = False

        if ok:
            continuing_list.append(word)
    if not continuing_list:
        continuing_list = 0
    return finished_list, continuing_list


def dic_phrase_searcher(shortened_dictionary, cont_list, spaceless_user_phrase):
    """Sees if any further words can be added to a phrase."""
    user_counter = Counter(spaceless_user_phrase)
    finished_list = []
    continuing_list = []
    for phrase in cont_list:
        phrase_counter = Counter(phrase)
        remaining_letters = user_counter - phrase_counter
        del phrase_counter[' ']
        for word in shortened_dictionary:
            word_counter = Counter(word)
            if word_counter == remaining_letters:
                finished_list.append(phrase + ' ' + word)
            ok = True
            for letter in word:
                if word_counter[letter] > remaining_letters[letter]:
                    ok = False
            if ok:
                continuing_list.append(phrase + ' ' + word)
    if not continuing_list:
        continuing_list = 0
    return finished_list, continuing_list


def main():
    """Gets a user phrase and returns all possible anagram phrases."""
    initial_dictionary = loader(sys.argv[1])
    user_phrase = input("Enter your name of phrase here: ")
    print("Searching...")
    start_time = time.time()
    spaceless_user_phrase = user_phrase.replace(' ', '')

    # Shortens the dictionary and gets an initial list of subsets.
    shortened_dictionary = dic_shortener(initial_dictionary, spaceless_user_phrase)
    fin_list, cont_list = dic_word_searcher(shortened_dictionary, spaceless_user_phrase)

    # 'len(fin_list) < 250' helps to filter out a lot of 'small-word-phrases'.
    run_through = 0
    while cont_list and len(fin_list) < 250:
        finished_phrases, cont_list = dic_phrase_searcher(shortened_dictionary,
                                                          cont_list, spaceless_user_phrase)
        fin_list += finished_phrases
        print(f"Run through {run_through} complete.")
        run_through += 1

    end_time = time.time()
    search_time = end_time - start_time

    print(f"\nFound {len(fin_list)} results:")
    for i, phrase in enumerate(fin_list, 1):
        print(f"{i}: {phrase}")
    print(f"Search complete in: {search_time} seconds.")
    sys.exit()


if __name__ == '__main__':
    main()
