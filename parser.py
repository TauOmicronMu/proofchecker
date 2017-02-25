BIN_OPS = ["|", "&", ":", "="]

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
    if exp.startswith('(') and exp.endswith(')') :
        print(exp)
        print(exp[1:-1])
        return exp[1:-1]
    return exp
    

def parse(exp):
    # 1. Remove all spaces from the string
    exp_c = "".join(exp.split())
    
    # 2. Replace -> with : and <-> with =
    exp_c = exp_c.replace('<->', '=').replace('->', ':')

    # 3. Split on all operators, starting at the shallowest
    def tree(exp):
        dps = depths(exp)
        max_d = max(dps)
        for i in range(max_d + 1): # For each depth, starting with the lowest...
            for j in range(len(dps) - 1): # For each char in exp
                if dps[j] == i and exp[j] in BIN_OPS:
                    return (tree(strip_parens(exp[0:j])), exp[j], tree(strip_parens(exp[j+1:])))
        return exp

    exp_t = tree(exp_c)
    print(exp_t)

print("----------------------------------------")
parse('((A -> B) & (B -> (C -> -D))) <-> (E | -F)')
