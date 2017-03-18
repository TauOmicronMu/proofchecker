UN_OPS = ["-"]
BIN_OPS = ["|", "&", ":", "="]

OPS = ["=", ":", "|", "&", "-"] # Used for precedence

""" 
    Returns an array containing the depths of each character
    in a propositional logic expression - based on how many
    parens the char is inside of. 
    Eg. depths(A&(B&C)) would return
             [111222210]
"""
def depths(exp):
    ret = []
    ctr = 0
    for c in exp:
        if c == '(':
            ctr += 1
        elif c == ')':
            ctr -= 1
        ret.append(ctr)
    return ret

"""
    Strips the outer parens from an expression iff it is in
    the form (...) and the two parentheses form the outermost
    parts of the same section (sect).
"""
def strip_parens(exp):
    dps = depths(exp)
    if sect(dps, exp, 0) == exp:
        return exp[1:-1]
    return exp

"""
    Returns the precedences of all operators at the uppermost
    depth (that contains ops), and 0 otherwise. Eg.
                      A:B=C&D|E
                     [020104030] 
    See: https://en.wikipedia.org/wiki/Logical_connective#Order_of_precedence
         for more details
"""
def prec(dps, exp):
    if(len(dps) == 0):
        return []
    for i in range(max(dps) + 1): # For each depth, starting with the lowest
        ret = []
        found = False # This will be set to true if we find something to split on
        for j in range(len(dps)): # For each element of exp/dps
            if(dps[j] == i and exp[j] in OPS): # If we have an OP at the current depth
                found = True 
                ret.append(OPS.index(exp[j])+1)
            else:
                ret.append(0)
        if(found):
            return ret

"""
    Returns the largest contiguous sequence (within parens) from the given
    position, n, in the expression, exp.
"""
def sect(dps, exp, n):
    if(len(exp) == 1):
        return exp
    ret = ""
    for i in range(n, len(dps)):
        ret += exp[i]
        if dps[i] < dps[n]:
            return ret
    return exp[n]

"""
    Parses a propositional logic expression into a parse tree in the form
    UnOp    ::= -
    BinOp   ::= | | & | : | =
    Literal ::= [A-Z]+[0-9]*
    Tree    ::= Literal
    Tree    ::= (UnOp, Tree)
    Tree    ::= (BinOp, Tree, Tree) 
"""
def parse(exp):
    # 1. Remove all spaces from the string and replace -> with : and <-> with =
    exp_c = "".join(exp.split()).replace('<->', '=').replace('->', ':')
 
    # 2. Recursively parse the structure as a tree.
    def tree(exp):
        exp = strip_parens(exp)
        dps = depths(exp)
        pre = prec(dps, exp)
        if(pre == None):
            return exp
        for i in range(4, 0, -1): # For each BinOp, starting with the highest precedence
            if i in pre: # Parse, with them at the root of the tree
                n = pre.index(i)
                left = exp[:n]
                right = exp[n+1:]
                if(len(left) != 1):
                    left = tree(left)
                if(len(right) != 1):
                    right = tree(right)
                return (OPS[i-1], left, right)
        if 5 in pre:
            n = pre.index(5)
            if(len(exp) == 2):
                return ('-', exp[1])
            return ('-', tree(sect(dps, exp, n+1)))
    return tree(exp_c)

"""
    Convert a given tree to a string using post-order
    traversal.
"""
def tostring(tree):
    if len(tree) == 1:
        return tree
    if tree[0] == '-':
        return '-' + "(" + tostring(tree[1]) + ")"
    return "(" + tostring(tree[1]) + tree[0] + tostring(tree[2]) + ")"   

# Test that the parser is doing it's job...
neg_lit = "".join("-A") # Test negation of literals
neg_nest_paren = "".join("-((A->B)&C)->D") # Test that negation is working properly over nested parens
multi_conj = "".join("(A -> B) & (B -> C) & (C -> D)") # Test multiple conjunctions at the same depth 
assert(parse(neg_lit) == ('-', 'A'))
assert(parse(neg_nest_paren) == (':', ('-', ('&', (':', 'A', 'B'), 'C')), 'D'))
assert(parse(multi_conj) == ('&', (':', 'A', 'B'), ('&', (':', 'B', 'C'), (':', 'C', 'D'))))
