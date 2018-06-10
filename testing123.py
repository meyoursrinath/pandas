import json

file = open("hello.csv", "w+")
string = ["I'm, and indian", "I\""]
file.write(str(1) + "," + json.dumps(string))
file.close()
print json.loads(json.dumps(string))


print type(json.loads(json.dumps(string)))
