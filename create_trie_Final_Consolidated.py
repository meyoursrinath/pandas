from flashtext import KeywordProcessor
import mysql.connector
import marisa_trie
import pickle
import time
import json
print "Imported all the libraries successfully"


class Database():
    def __init__(self, configuration):
        config = {
            'user': 'sherlock',
            'password': 'z00mrxr0cks!',
            'host': '69.164.196.100',
            'database': 'metathesaurus',
            'raise_on_warnings': True,
        }
        if configuration:
            config = configuration
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor(buffered=True)

    def execute(self, query):
        return self.cursor.execute(query)

    def __del__(self):
        self.cursor.close()
        self.connection.close()


def create_trie():
    keys = []
    values = []
    start = time.time()
    db = Database(None)
    print "Connected to DB in", time.time() - start, "secs"
    start = time.time()
    db.execute("SELECT * FROM `Final_consolidated`")
    print "Retrieved Info from table in", time.time() - start, "secs"
    for row in db.cursor:
        value = []
        for i, ele in enumerate(row):
            if i == 2:
                keys.append(ele.lower())
            else:
                value.append(ele)
        values.append(json.dumps(value))
    trie = marisa_trie.Trie()
    print "Starting to zip into Marisa trie"
    trie = marisa_trie.BytesTrie(zip(keys, values))
    print "Completed zipping into Marisa trie"
    print "Pickling Trie"
    with open('consolidated.pkl', 'wb') as output:
        pickle.dump(trie, output, pickle.HIGHEST_PROTOCOL)
    print "Total number of Keys:", len(keys)


def test_trie():
    trie = None
    with open('consolidated.pkl', 'rb') as input:
        trie = pickle.load(input)
    loop = True
    while loop:
        ele = raw_input("Element to search in trie: ")
        ele = unicode(ele, "latin1")
        if ele in trie:
            print "Found"
            print json.dumps(json.loads(trie[ele][0]), indent=4)
        else:
            print "Not found"

        if ele == 'quit':
            loop = False


def flash_text():
    needles = []
    start = time.time()
    db = Database(None)
    print "Connected to DB in", time.time() - start, "secs"
    start = time.time()
    db.execute("SELECT STR FROM `Final_consolidated`")
    print "Retrieved Info from table in", time.time() - start, "secs"
    start = time.time()
    for ele in db.cursor:
        needles.append(ele[0].lower())
    print "Needles are ready in", time.time() - start, "secs"
    processor = KeywordProcessor()
    start = time.time()
    for i, needle in enumerate(needles):
        if i % 100000 == 0:
            print i
            if needle.lower() == "sofosbuvir/velpatasvir":
                print True
        processor.add_keyword(needle.lower())
    print "Processed needles in", time.time() - start, "secs"
    file = open("keywords_DD.csv", "w+")

    db.execute("SELECT id, detailed_description FROM `sherlock_ct_new`.`trials`")
    start = time.time()
    for row in db.cursor:
        if row[1]:
            string = str(row[0])
            haystack = row[1].lower()
            found = list(set(processor.extract_keywords(haystack.lower())))
            for ele in found:
                string += "," + ele
            string += "\n"
            file.write(string)
    file.close()
    f = time.time() - start
    print "Found needles within haystack in", f, "secs"
    return f


if __name__ == '__main__':
    start = time.time()
    # create_trie()
    # test_trie()
    # create_automaton()
    t = flash_text()
    print "Total Time Elapsed for preparation:", time.time() - start - t, "secs"
