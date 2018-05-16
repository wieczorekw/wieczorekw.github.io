from fractions import Fraction

def seqEval(string, sc, k):
    
    def findNodeForSubstring(i, j):
        curr_edge = None if (0, string[i]) not in sc.edges else sc.edges[(0, string[i])]
        while curr_edge:
            source = curr_edge.source_node_index
            dest = curr_edge.dest_node_index
            p = curr_edge.first_char_index
            q = curr_edge.last_char_index
            idx = p
            while idx <= q and i <= j and sc.word[idx] == string[i]:
                idx += 1
                i += 1
            if idx > q and i > j:
                return dest
            elif idx > q:
                curr_edge = None if (dest, string[i]) not in sc.edges else sc.edges[(dest, string[i])]
            elif i > j:
                return dest
            else:
                return None
        return None
        
    sum = Fraction(0, 1)
    counter = 0
    n = len(string)
    for pos in range(n - k + 1):
        u = findNodeForSubstring(pos, pos + k - 1)
        if u:
            counter += 1
            sum += Fraction(sc.nodes[u].positive, sc.nodes[u].negative + sc.nodes[u].positive)
    return sum / counter if counter else 0
