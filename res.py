import parser
import cnf

def res(s):
    P = cnf.clause_nf(parser.parse(s))

'''
    Given a set of clauses, S, choose two clauses
    such that one contains ¬L and the other contains
    L (with a complimentary literal) 
'''
def choose(s):
    acc = set([])
    for c in s:
        for l in c:
            print(l)
            print(cnf.neg(l))
            acc.add(l if len(l) == 1 else cnf.neg(l))
    return acc       

def res_a(s):
    # Choose 2 clauses, C1, C2 that have not yet
    # been resolved and contain one complimentary
    # literal
    
    # Resolve P

    # PN = P UNION(?) Resolved P

    # If len(P) == 0 return UNSAT

    # If PN == P return SAT      

    # Call the thing again
  
    pass 
