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
    return (tree[0], rimp(tree[1]), rimp(tree[2])) # Anything else



def cnf(tree):
    return dist(rneg(rimp(tree)))
