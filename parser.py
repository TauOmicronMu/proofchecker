UN_OPS = ["-"]
BIN_OPS = ["|", "&", ":", "="]

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
    Strips the outer parens from an expression iff the expression
    is in the form (...)  
"""
def strip_parens(exp):
    if exp.startswith('(') and exp.endswith(')') :
        return exp[1:-1]
    return exp

def strip_neg(exp):
    if exp[0:2] == '-(' and exp.endswith(')') : 
        return exp[2:-1]
    return exp   

"""
    Returns whether or not an expression is in the form -(...)
    (i.e. the expression is negated)
"""
def is_neg(exp):
    return exp[0:2] == '-(' and exp.endswith(')')

"""
    Parses a propositional logic expression into a parse tree in the form
    UnOp    ::= -
    BinOp   ::= | | & | : | =
    Literal ::= [A-Z]+[0-9]* | -[A-Z]+[0-9]*
    Tree    ::= Literal
    Tree    ::= (UnOp, Tree)
    Tree    ::= (BinOp, Tree, Tree) 
"""
def parse(exp):
    # 1. Remove all spaces from the string
    exp_c = "".join(exp.split())
    
    # 2. Replace -> with : and <-> with =
    exp_c = exp_c.replace('<->', '=').replace('->', ':')

    # 3. Split on all operators, starting at the shallowest
    def tree(exp):
        if(is_neg(exp)) :
            return ('-', tree(strip_neg(exp)))
        dps = depths(exp)
        max_d = max(dps)
        for i in range(max_d + 1): # For each depth, starting with the lowest...
            for j in range(len(dps) - 1): # For each char in exp
                if dps[j] == i and exp[j] in BIN_OPS:
                    return (exp[j], tree(strip_parens(exp[0:j])), tree(strip_parens(exp[j+1:])))
        return exp

    return tree(exp_c)


print(parse('(-(A -> B) & (B -> (C -> D))) <-> (E | F))'))

# Make sure that the parser is working as it should
assert(parse('(-(A -> B) & (B -> (C -> D))) <-> (E | F))') == ('=', ('-', (':', 'A', (':', 'B)&(B', (':', 'C', 'D')))), ('|', 'E', 'F)')))
