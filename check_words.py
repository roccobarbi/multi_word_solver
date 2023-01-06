from dictionaries import dictionary
import sys
import argparse


program_epilog = (
    "",
    "EXAMPLES:",
    "",
    "python3 check_words.py -l en -k m,1 -k s,3 -i rab cjddjke",
    "",
    "  this would identify a word with the pattern cjddjke, where c is known to",
    "  represent the letter m, d is known to represent the letter s, the letters r, a",
    "  and b are known to be missing."
)


class KnownLetter:
    def __init__(self, letter, position):
        self.letter = letter
        self.position = int(position)

    def is_here(self, word):
        if len(word) >= self.position + 1 and word[self.position] == self.letter:
            return True
        return False


def known_letter_argument(argument):
    argument = argument.split(",")
    return KnownLetter(argument[0], argument[1])


def check_aca_illegal_letters(wordlist, pattern):
    output = []
    for word in wordlist:
        is_compliant = True
        for index, letter in enumerate(word):
            if letter == pattern[index]:
                is_compliant = False
        if is_compliant:
            output.append(word)
    return output


def lookup_candidates(word, language):
    return dictionary.lookup_pattern(word, language)


def main():
    argument_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="A program to check word patterns against a dictionary to help solve cryptograms.",
        epilog="\n".join(program_epilog)
    )
    argument_parser.add_argument("-l", "--language", required=True, help="The dictionary to be used.")
    argument_parser.add_argument("-a", "--aca", action="store_true", help="Flag if ACA rules should be applied.")
    argument_parser.add_argument("words", nargs="*", help="The words that you're looking for.")
    configuration = argument_parser.parse_args()
    words = []
    for word in configuration.words:
        word_entry = {word: word, candidates: {}}
        candidates = lookup_candidates(word, configuration.language)
        if configuration.aca:
            candidates = check_aca_illegal_letters(candidates, word)
        word_length = len(word)
        for candidate in candidates:
            candidate_map = {}
            for i in range(word_length):
                if word[i] not in candidate_map.keys():
                    candidate_map[word[i]] = candidate[i]
            word_entry["candidates"][candidate] = {candidate: candidate, map: candidate_map}
            word_entry["candidates_count"] = len(word_entry["candidates"].keys())
        words.append(word_entry)
    total_combinations = 1
    for word in words:
        if word["candidates_count"] > 0:
            total_combinations *= word["candidates_count"]
    print("[+] {} total combinations found.".format(total_combinations))
    for word in wordlist:
        print(word)


if __name__ == "__main__":
    main()
