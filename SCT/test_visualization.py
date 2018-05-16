from suffix_classifier import SuffixClassifier
#import matplotlib.pyplot as plt
#import networkx as nx

#st = SuffixTree("ab1bc1bb0ba0")

#G=nx.DiGraph()

#for node in range(len(st.nodes)):
#    G.add_node(node)    

#for edge in st.edges.values():
#    G.add_edge(edge.source_node_index, edge.dest_node_index)    

#pos = nx.spring_layout(G, scale=2)

#nx.draw(G, pos, with_labels=True, arrows=False)

#edge_labels = {(e.source_node_index, e.dest_node_index): st.string[e.first_char_index:e.last_char_index+1] for e in st.edges.values()}

#nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, label_pos=0.5)

#plt.show()

classifier = SuffixClassifier('ab1ba1aa0bb0$')
classifier.print_suffix_tree()


