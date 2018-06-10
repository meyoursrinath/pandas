from flashtext import KeywordProcessor
import time
print "Imported all the libraries successfully"


def find_needles():
    needles = ["epclusa", "hcv", "chronic hepatitis c", "sofosbuvir+velpatasvir"]

    start = time.time()
    processor = KeywordProcessor()
    processor.add_keywords_from_list(needles)
    print "Processed needles in", time.time() - start, "secs"

    start = time.time()
    file = open("hello.txt", "r")
    for haystack in file.readlines():
        found = list(set(processor.extract_keywords(haystack.lower(), span_info=True)))
        print found
        # string = ""
        # for ele in found:
        #     ele = ele.replace('"', '\\"')
        #     string += ',"' + ele + '"'
        # print string, "\n\n\n"
    file.close()
    time.time() - start
    print "Found needles within haystack in", time.time() - start, "secs"


if __name__ == '__main__':
    start = time.time()
    find_needles()
    print "Total Time Elapsed for preparation:", time.time() - start, "secs"
