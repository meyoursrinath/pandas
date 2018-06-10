from flashtext import KeywordProcessor
import mysql.connector
# import json
import time
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


def find_needles():
    needles = []

    start = time.time()
    db = Database(None)
    print "Connected to DB in", time.time() - start, "secs"

    start = time.time()
    db.execute("SELECT STR FROM `Final_consolidated`")
    print "Retrieved info from DB in", time.time() - start, "secs"

    start = time.time()
    for ele in db.cursor:
        needles.append(ele[0].lower())
    print "Listed needles in", time.time() - start, "secs"

    start = time.time()
    processor = KeywordProcessor()
    processor.add_keywords_from_list(needles)
    print "Processed needles in", time.time() - start, "secs"
    start = time.time()
    file = open("hello.txt", "r")
    for haystack in file.readlines():
        print "Before hyphen removal:"
        found = list(set(processor.extract_keywords(haystack.lower(), span_info=True)))
        string = ""
        for ele in found:
            ele = ele.replace('"', '\\"')
            string += ',"' + ele + '"'
        print string, "\n\n"
        haystack = haystack.replace("-", " ")
        print "After hyphen removal:"
        found = list(set(processor.extract_keywords(haystack.lower())))
        string = ""
        for ele in found:
            ele = ele.replace('"', '\\"')
            string += ',"' + ele + '"'
        print string, "\n\n\n"
    # haystacks = []
    # db.execute("SELECT id, detailed_description FROM `sherlock_ct_new`.`trials`")
    # for row in db.cursor:
    #     if row[1]:
    #         haystack = row[1].lower()
    #         found = list(set(processor.extract_keywords(haystack.lower())))
    #         file.write(str(row[0]) + "," + json.dumps(found))
    file.close()
    time.time() - start
    print "Found needles within haystack in", time.time() - start, "secs"


if __name__ == '__main__':
    start = time.time()
    find_needles()
    print "Total Time Elapsed for preparation:", time.time() - start, "secs"
