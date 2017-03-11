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

def strip_parens(exp):
    dps = depths(exp)
    if sect(dps, exp, 0) == exp:
        return exp[1:-1]
    return exp

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

def sect(dps, exp, n):
    if(len(exp) == 1):
        return exp
    ret = ""
    for i in range(n, len(dps)):
        ret += exp[i]
        if dps[i] < dps[n]:
            return ret
    return exp[n]

def parse(exp):
    # 1. Remove all spaces from the string and replace -> with : and <-> with =
    exp_c = "".join(exp.split()).replace('<->', '=').replace('->', ':')
 
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
            return ('-', tree(sect(dps, exp, n+1)))

    return tree(exp_c)

exp = "".join("-((A->B)&C)->D")
exp2 = "".join("(A -> B) & (B -> C) & (C -> D)") 
assert(parse(exp) == (':', ('-', ('&', (':', 'A', 'B'), 'C')), 'D'))
assert(parse(exp2) == ('&', (':', 'A', 'B'), ('&', (':', 'B', 'C'), (':', 'C', 'D'))))

