import parser

debug = True

def rimp(tree):
    '''
        Replaces all implications and equivalences from the given
        tree, replacing them as follows:
            A -> B  => ¬A V B
            A <-> B => (A & B) V (¬A & ¬B) 
    '''
    if(len(tree) == 1): # Literal
        if debug:
            print("[rimp] Literal: " + parser.tostring(tree))
        return tree 
    if tree[0] == ':': # Implication
        ret_val = ('|', ('-', rimp(tree[1])), rimp(tree[2]))
        if debug:
            print("[rimp] Removing Implication: " + parser.tostring(tree) + " => " + parser.tostring(ret_val))
        return ret_val
    if tree[0] == '=': # Equivalence
        ret_val = ('|', ('&', rimp(tree[1]), rimp(tree[2])), 
                     ('&', ('-', rimp(tree[1])), ('-', rimp(tree[2]))))
        print("[rimp] Removing Equivalence: " + parser.tostring(tree) + " => " + parser.tostring(ret_val))
        return ret_val
    if debug:
        print("[rimp] No cases matched.")
    if tree[0] == '-':        
        return (tree[0], rimp(tree[1])) # Negation
    return (tree[0], rimp(tree[1]), rimp(tree[2])) # Anything else

def rneg(tree):
    '''
        Pushes all negations to the leaves of the tree - i.e. the 
        only negations left are on the literals (eg. -A).
    '''
    if(len(tree) == 1): # Literal
        if debug:
            print("[rneg] Literal: " + parser.tostring(tree))
        return tree
    root = tree[0]
    left = tree[1] 
    if root == '-': # Negation
        op = left[0]
        if(len(left) == 1):
            return tree
        left = left[1]
        if op == '-': # Double Negation
            ret_val = rneg(left)
            if debug:
                print("[rneg] Double Negation: " + parser.tostring(tree) + " => " + parser.tostring(ret_val))
            return ret_val
        right = tree[1][2]
        if op == '&' or op == '|': # DeMorgan's
            op = '|' if op == '&' else '|' # Swap the op over
            ret_val = (op, rneg(('-', left)), rneg(('-', right)))
            if debug:
                print("[rneg] DeMorgan's on: " + parser.tostring(tree) + " => " + parser.tostring(ret_val))
            return ret_val
    if debug:
        print("[rneg] " + parser.tostring(tree) + " : No cases matched.")
    return (root, rneg(tree[1]), rneg(tree[2])) 

def dist(tree):
    '''
        Distributes over Vs until we are in CNF.
    '''
    if len(tree) == 1: # Literal
        if debug:
            print("[dist] Literal : " + parser.tostring(tree))
        return tree
    root = tree[0]
    if root == '|':
        left = tree[1]
        right = tree[2]
        leftop = left[0]
        rightop = right[0]
        # P V (Q & R) => (P V Q) & (P V R)
        if rightop == '&':
            ret_val = ('&', ('|', left, right[1]), ('|', left, right[2]))
            if debug:
                print("[dist] V-Distributivity on right : " + parser.tostring(tree) +  " => " + parser.tostring(ret_val))
            return ret_val
        # (P & Q) V R => (P V R) & (Q V R)
        if leftop == '&':
            ret_val = ('&', ('|', left[1], right), ('|', left[2], right))
            if debug: 
                print("[dist] V-Distributivity on left : " + parser.tostring(tree) + " => " + parser.tostring(ret_val))
            return ret_val
    if debug:
        print("[dist] " + parser.tostring(tree) + " : No cases matched.")
    if root == '-':
        return (root, dist(tree[1]))
    return (root, dist(tree[1]), dist(tree[2]))

def cnf_tree(tree):
    '''
        Returns the Conjunctive Normal Form tree of the given 
        initial tree. (combination of dist, rneg and rimp).
    '''
    return dist(rneg(rimp(tree)))

def cnf_pretty(tree):
    '''
        Pretty-prints the Clause NF of the given tree
    '''
    cnf_t = cnf_tree(tree)
    cs = parser.tostring(cnf_t).split("&") 
    ret = ""
    for c in cs:
        ret += "("
        ret += c
        ret += ")"
        ret += " & "
    return ret[:-3] # :-3 so &s are interspersed properly...

def clause_nf(tree):
    '''
        Takes a PL tree and converts it to clause NF. Returns a
        set of sets (i.e. {{...}, {...}, {...}, {...}}) where each 
        inner set represents a clause (i.e. a disjunction of 
        literals.

        Converts to a non-'paren-ned' version and splits on & then
        | to give lists to convert to sets.
    '''

    cnf = rationalise(set([frozenset(x) for x in [l.split('|') for l in parser.noptostring(cnf_tree(tree)).split('&')]]))
    if debug:
        print("[clause_nf] Clause NF : " + str(cnf))
    return cnf

def rationalise(s):
    '''
        Takes a set in CNF (see clause_nf function docstring), and removes any 
        sets with rationalisale elements - eg. {A, -A} => T
    '''
    ret_set = set([])
    for c in s:
        for l in c:
            if(not neg(l) in c):
                ret_set.add(c)
    return ret_set
    
def neg(l):
    '''
        Returns the negated form of a literal:
            L => -L
           -L => L
    '''  
    return (l[1] if len(l) > 1 else "-" + l)

# Tests
# rimp tests
# rneg tests
# dist tests
