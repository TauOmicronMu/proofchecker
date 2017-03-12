import parser

'''
    Replaces all implications and equivalences from the given
    tree, replacing them as follows:
        A -> B  => ¬A V B
        A <-> B => (A & B) V (¬A & ¬B) 
'''
def rimp(tree):
    if(len(tree) == 1): # Literal
        return tree 
    if tree[0] == ':': # Implication
        return ('|', ('-', rimp(tree[1])), rimp(tree[2]))
    if tree[0] == '=': # Equivalence
        return ('|', ('&', rimp(tree[1]), rimp(tree[2])), 
                     ('&', ('-', rimp(tree[1])), ('-', rimp(tree[2]))))
    if tree[0] == '-':
        return (tree[0], rimp(tree[1])) # Negation
    return (tree[0], rimp(tree[1]), rimp(tree[2])) # Anything else

def rneg(tree):
    if(len(tree) == 1): # Literal
        return tree
    root = tree[0]
    left = tree[1] 
    if root == '-': # Negation
        op = tree[1][0]
        if(len(left) == 1):
            return tree
        left = tree[1][1]
        if op == '-': # Double Negation
            return rneg(left)
        right = tree[1][2]
        if op == '&' or op == '|': # DeMorgan's
            op = '|' if op == '&' else '&' # Swap the op over
            return (op, rneg(('-', left)), rneg(('-', right)))
    return (root, rneg(tree[1]), rneg(tree[2])) 

def cnf(tree):
    return dist(rneg(rimp(tree)))
