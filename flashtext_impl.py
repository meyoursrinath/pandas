from flashtext import KeywordProcessor
import mysql.connector
import time
print "Imported all the libraries successfully"

processor = None


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


def create_pickle(sql_query, filename):
    global processor
    print "\nStarted", filename
    file = open(filename + ".csv", "w+")
    start = time.time()
    db.execute(sql_query)
    for row in db.cursor:
        string = str(row[0])
        if row[1]:
            haystack = row[1].lower()
            haystack = haystack.replace("-", " ")
            found = list(set(processor.extract_keywords(haystack.lower())))
            for ele in found:
                ele = ele.replace('"', '\\"')
                string += ',"' + ele + '"'
            file.write(string.encode('utf-8'))
            file.write("\n")
    file.close()
    time.time() - start
    print "Found needles within haystack in", time.time() - start, "secs"
    print "\nFinished", filename


if __name__ == '__main__':
    start = time.time()
    create_pickle("SELECT id, official_title FROM `sherlock_ct_new`.`trials`", "official_title_keywords")
    create_pickle("SELECT id, name FROM `sherlock_ct_new`.`interventions`", "interventions_name_keywords")
    create_pickle("SELECT id, description FROM `sherlock_ct_new`.`interventions`", "interventions_description_keywords")
    create_pickle("SELECT id, label FROM `sherlock_ct_new`.`arm_groups`", "arm_groups_label_keywords")
    create_pickle("SELECT id, description FROM `sherlock_ct_new`.`arm_groups`", "arm_groups_description_keywords")
    print "Total Time Elapsed for preparation:", time.time() - start, "secs"
