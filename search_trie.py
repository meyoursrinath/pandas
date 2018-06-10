import marisa_trie
import pickle
import json

trie = marisa_trie.Trie()
with open('consolidated.pkl', 'rb') as input:
    trie = pickle.load(input)


def main():
    global trie
    loop = True
    while loop:
        ele = raw_input("Element to search in trie: ")
        ele = unicode(ele, "utf-8")
        if ele in trie:
            print "Found"
            print json.dumps(json.loads(trie[ele][0]), indent=4)
        else:
            print "Not found"

        choice = raw_input("\nContinue? (y/n) ")
        if choice is not 'y':
            loop = False


if __name__ == '__main__':
    main()
