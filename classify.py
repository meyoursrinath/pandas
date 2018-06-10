import networkx as nx
graph = nx.read_edgelist("data.txt", delimiter=',')
file = open("classified_CUI.csv", "w+")
for ele in sorted(nx.connected_components(graph)):
    ids = list(ele)[0]
    for e in ele:
        file.write("\n" + ids + "," + e)
file.close()
