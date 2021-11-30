"""Program to find the frequencies of digrams within a dictionary file."""
import re
import sys
from itertools import permutations


def loader(file):
    """Loads a dic.txt file into a list of strings."""
    try:
        with open(file, encoding='UTF-8') as in_file:
            loaded_text = in_file.read().strip().split('\n')
            loaded_text = list(map(lambda x: x.lower(), loaded_text))
            return loaded_text
    except IOError as err:
        print(f"{err}: Dictionary File not found at given path.")
        sys.exit(1)


def get_digrams(user_string):
    """Returns a set of all possible permutations for a given string."""
    digrams = set()
    all_perms = {''.join(i) for i in permutations(user_string)}
    for perm in all_perms:
        for i in range(0, len(perm)-1):
            digrams.add(perm[i] + perm[i+1])

    return digrams


def instances_of_digrams(dic_words, all_digrams):
    """Returns a dictionary item containing the frequency of digram presence in a dic file."""
    res = {}
    dic_as_string = ','.join(dic_words)
    for digram in all_digrams:
        regex = re.compile(digram)
        instances = regex.findall(dic_as_string)
        res[digram] = len(instances)
    return res


def main():
    """Calls a list of strings and returns the frequency of all digrams from a user string."""
    dic_words = loader(r'.\extra_files\dictionary_words.txt')
    user_string = input("Enter your string: ")
    all_digrams = get_digrams(user_string)

    frequencies = instances_of_digrams(dic_words, all_digrams)
    print("Final digram presence in dictionary:\n")
    for key, val in frequencies.items():
        print(f"{key}: {val}")


if __name__ == '__main__':
    main()
