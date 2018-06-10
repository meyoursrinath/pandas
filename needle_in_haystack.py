# Aho-Corasick Algorithm
import ahocorasick
from flashtext import KeywordProcessor
import time


def main():
    A = ahocorasick.Automaton()

    needles = ["Narendra Modi", "Prime Minister ", "Gujarat", "Modi", "Narendra"]

    for idx, key in enumerate(needles):
        A.add_word(key, (idx, key))

    print "Narendra Modi" in A  # True
    print "narendra modi" in A  # False, case sensitive

    haystack = "Narendra Narendras Modi is the Prime Minister of India. He was a Chief Minister of Gujarat. Gujarat is a nice place"

    A.make_automaton()

    print list(A.keys(haystack, "*", ahocorasick.MATCH_EXACT_LENGTH))

    # for end_index, (insert_order, original_value) in A.iter(haystack):
    #     start_index = end_index - len(original_value) + 1
    #     print (start_index, end_index, (insert_order, original_value))
    #     assert haystack[start_index:start_index + len(original_value)] == original_value


def identify():
    A = ahocorasick.Automaton()

    needles = ["sodium", "sodium chloride"]

    for idx, key in enumerate(needles):
        A.add_word(key, (idx, key))

    # print "Narendra Modi" in A  # True
    # print "narendra modi" in A  # False, case sensitive

    haystack = "We use both sodium and sodium chloride for our drug"

    A.make_automaton()

    for end_index, (insert_order, original_value) in A.iter(haystack):
        start_index = end_index - len(original_value) + 1
        print (start_index, end_index, (insert_order, original_value))
        assert haystack[start_index:start_index + len(original_value)] == original_value


def flash_text():
    # haystack = "Narendra Narendra Modi is the Prime Minister of India. He was a Chief Minister of Gujarat. Gujarat is a nice place"
    haystack = "sof/vel is a short form for sofosbuvir/velpatasvir"
    # needles = ["Narendra Modi", "Prime Minister", "Gujarat", "Modi", "Narendra"]
    needles = ["sof/vel", "sofosbuvir/velpatasvir"]
    processor = KeywordProcessor()
    processor.add_keywords_from_list(needles)
    found = processor.extract_keywords(haystack)
    print found


if __name__ == '__main__':
    start = time.time()
    # main()
    # identify()
    flash_text()
    print time.time() - start
