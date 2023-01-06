from dictionaries import dictionary
import time
import argparse

program_epilog = (
    "",
    "EXAMPLES:",
    "",
    "python3 solve.py -l en -k m,1 -k s,3 -i rab cjddjke",
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


def check_common(word1, word2, candidate1, candidate2, common):
    if word2 in common[word1].keys():
        for letter in common[word1][word2].keys():
            if candidate1[letter] != candidate2[common[word1][word2][letter]]:
                return False
    return True


def check_candidate(previous, candidate, index, words, common_letters):
    current = []
    for i in range(0, index):
        if not check_common(words[i]["word"], words[index]["word"], previous[i], candidate, common_letters):
            return False, []
        if candidate == previous[i]:
            return False, []
        current.append(previous[i])
    current.append(candidate)
    return True, current


def recursive_check(previous, index, words, common_letters, checks):
    current_check = checks
    for candidate in words[index]["candidates"]:
        good, current = check_candidate(previous, candidate, index, words, common_letters)
        current_check += 1
        if current_check % 1000000 == 0:
            print("[+] {} million checks run...".format(current_check//1000000))
        if good:
            if index < len(words) - 1:
                current_check = recursive_check(current, index + 1, words, common_letters, current_check)
            else:
                print(current)
    return current_check


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
    print("[+] Extracting candidates for each word")
    for word in configuration.words:
        print("\t[+] {}...".format(word))
        word_entry = {"word": word, "candidates": {}}
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
        print("\t[+] {}: {} candidates".format(word, word_entry["candidates_count"]))
    total_combinations = 1
    for word in words:
        if word["candidates_count"] > 0:
            total_combinations *= word["candidates_count"]
    print("[+] Candidates extracted: {} total combinations found.".format(total_combinations))
    print("[+] Optimizing candidate checks.")
    common_letters = {}
    for word in configuration.words:
        print("\t[+] Optimizing {}".format(word))
        word_common = {}
        for other_word in configuration.words:
            if other_word != word:
                word_common[other_word] = {}
                for letter in word:
                    if letter in other_word:
                        word_common[other_word][word.index(letter)] = other_word.index(letter)
                print("\t[+] {} has {} unique letters in common with {}".format(word, len(word_common[other_word].keys()), other_word))
        common_letters[word] = word_common
    print("[+] Optimizations completed!")
    print("[+] Running recursive checks...")
    checks = recursive_check([], 0, words, common_letters, 0)
    print("[+] {} checks run.".format(checks))
    print("[+] Recursive checks completed!")


if __name__ == "__main__":
    main()
