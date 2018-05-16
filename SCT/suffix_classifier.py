from suffix_tree import SuffixTree

class Label(object):

    def __init__(self, sc, beginning, end):
        self.sc = sc
        self.beginning = beginning
        self.end = end

    def __iter__(self):
        self.idx = self.beginning
        return self

    def __next__(self):
        if self.idx > self.end:
            raise StopIteration
        self.idx += 1
        return self.sc.word[self.idx - 1]

    def __getitem__(self, idx):
        if idx < 0 or idx > self.end - self.beginning:
            raise IndexError
        return self.sc.word[idx + self.beginning]

    def __contains__(self, item):
        i = self.beginning
        while i <= self.end:
            if self.sc.word[i] == item:
                return True
            i += 1
        return False

class SuffixClassifier(object):

    def __init__(self, D_plus, D_minus, alphabet):
        self.word = '1'.join(D_plus) + '1' + '0'.join(D_minus) + '0$'
        self.suffixTree = SuffixTree(self.word)
        self.alphabet = alphabet | {'0', '1', '$'}
        self.edges = self.suffixTree.edges
        if self.__has_edges(0): # bug fix
            self.suffixTree.nodes[0].suffix_node = 0

    def print_suffix_tree(self, printDirectDebug = True):
        print(self.word)
        self.print_tree_part('0', 0)
        print()
        if printDirectDebug:
            print(self.suffixTree.__repr__())

    def print_tree_part(self, prefix, nodeId):
        found = False
        first = True
        for e in self.suffixTree.edges.values():
            if e.source_node_index == nodeId:
                found = True
                text = self.suffixTree.string[e.first_char_index:e.last_char_index+1]
                if first:
                    first = False
                else:
                    prefix = (' ' * (len(prefix) - 1)) + '\\'
                data_node = self.__print_data_node(e.source_node_index)
                link = "%s%s--'%s'--%d" % (prefix, data_node, text, e.dest_node_index)
                if not self.__has_edges(e.dest_node_index):
                    link += self.__print_data_node(e.dest_node_index)
                self.print_tree_part(link, e.dest_node_index)
        if found == False:
            print(('\n' if prefix[0] in ['0','\\'] else '') + prefix)

    def __print_data_node(self, nodeId):
        if hasattr(self.suffixTree.nodes[nodeId], 'negative'):
            node = self.suffixTree.nodes[nodeId]
            return "(%d,%d)" % (node.negative, node.positive)

        return ""

    def truncate_tree(self):
        self.nodes = {} # convert to dictionary because we need node
                   # at specific index after remove any elements before
        for i in range(len(self.suffixTree.nodes)):
            u = self.suffixTree.nodes[i]
            u.positive = 0 #n_+
            u.negative = 0 #n_-
            self.nodes[i] = u

        self.__truncate(0)

    def __truncate(self, u: int):
        for v, l in self.__traverse(u):
            if not any(c in l for c in ['0','1','$']): # case (a)
                self.__truncate(v)
            elif l[0] in ['0', '1']: # (b) or (c)
                leafs = self.__remove_with_edge(u, v, l)
                self.__increment(u, l[0], leafs)
            elif l[0] == '$': #(d)
                self.edges.pop((u, l[0]))
                self.nodes.pop(v) # not remove u!
            else:
                e = self.edges[(u, l[0])]
                sub = e.first_char_index
                for c in l:
                    if c in ['0', '1']: # (e) or (f)
                        leafs = self.__remove_from_node(v)
                        self.__increment(v, c, leafs)
                        break
                    sub += 1
                e.last_char_index = sub - 1

    def __remove_from_node(self, u: int): #remove subtree from node
        if self.nodes[u].suffix_node == -1: #speedup, leaf
            return 1
        leafs = 0
        for v, l in self.__traverse(u):
            leafs += self.__remove_from_node(v)
            self.edges.pop((u, l[0]))
            self.nodes.pop(v)

        self.nodes[u].suffix_node = -1
        return leafs

    def __remove_with_edge(self, u: int, v: int, l: Label): #remove subtree from edge
        leafs = self.__remove_from_node(v)
        self.edges.pop((u, l[0]))
        self.nodes.pop(v)

        #check if u is not leaf now
        if not self.__has_edges(u):
            self.nodes[u].suffix_node = -1

        return leafs

    def recalculate(self, u):
        if self.nodes[u].suffix_node == -1:
            return self.nodes[u].negative, self.nodes[u].positive
        negative = 0
        positive = 0

        for v, l in self.__traverse(u):
            neg, pos = self.recalculate(v)
            negative += neg
            positive += pos
        self.__increment(u, '0', negative)
        self.__increment(u, '1', positive)
        return self.nodes[u].negative, self.nodes[u].positive

    def __increment(self, u: int, type: str, leafs):
        if type == '0':
            self.nodes[u].negative += leafs
        else:
            self.nodes[u].positive += leafs

    def __has_edges(self, u: int):
        return any(self.__traverse(u))

    def __traverse(self, u):
        for c in self.alphabet:
            if (u, c) in self.edges:
                e = self.edges[(u, c)]
                l = Label(self, e.first_char_index, e.last_char_index)
                yield (e.dest_node_index, l)
