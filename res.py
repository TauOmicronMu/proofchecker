import parser
import cnf

debug = True

def res(e):
    '''
        Returns SAT or UNSAT based on the result of
        propositional resolution on the given logical
        expression, e.
    '''
    return res_a(cnf.clause_nf(parser.parse(e)))
    
     
def choose(s):
    '''
        Given a set of clauses, S, choose all pairs of two clauses
        such that one contains ¬L and the other contains
        L (with a complimentary literal) 
    '''
    ls = literals(s) 
    ret_val = set()
    # For each literal, see if there are two clauses
    # that contain complimentary forms of it.
    if debug : 
        print("[choose] Literals : " + str(ls))
    for l in ls:
        c_l = set()
        c_nl = set()
        for c in s:
            if l in c:
                c_l.add(c)
            elif cnf.neg(l) in c:
                c_nl.add(c)
        if len(c_l) > 0 and len(c_nl) > 0:
            # We've found two clauses with a complimentary literal...
            val = (l, c_l.pop(), c_nl.pop()) 
            if debug:
                print("[choose] Pair found : " + str(val))
            ret_val.add(val)
    if len(ret_val) != 0:
        if debug:
            print("[choose] Final pairs found : " + str(ret_val)) 
        return ret_val
    if debug:
        print("[choose] No pair found...")
    return None # No pairs found...  

def literals(s):
    acc = set([])
    for c in s:
        for l in c:
            acc.add(l if len(l) == 1 else cnf.neg(l))
    return acc

def cpywo(s, l):
    '''
        Copies all elements of a frozenset s in to a new
        frozenset, except the element l (and returns the
        new frozenset). For sets, use sremove instead of
        cpywo.
    '''
    return frozenset([x for x in s if x != l])

def sreplace(s, c, nc): 
    ''' 
        Copies all elements of a set s in to a new set, 
        except for the element c, which is replaced with
        nc (and the new set is returned).
    '''
    return set([x if x != c else nc for x in s])    

def sremove(s, c):
    ''' 
        Copies all elements of a set s in to a new set,
        except for the element c (and returns the new
        set). For frozensets, use cpywo instead of
        sremove.
    '''
    return set([x for x in s if x != c])

def res_a(s):
    '''
        Auxiliary function for res(), recursively applies 
        resolution rules to the set until SAT (true) or UNSAT (false) is 
        found.
    '''
    if debug:
        print("[res_a] Resolving : " + str(s))    

    # Choose all pairs of clauses, C1, C2 that have not yet
    # been resolved and contain one complimentary literal
    choices = choose(s)
  
    return resolve_choice(choices, s)


def resolve_choice(choice, s):
    if choice != None and len(choice) == 0: 
        return false
    if choice != None and len(choice) > 1 and isinstance(choice, set):
        return resolve_choice(choice.pop(), s) or resolve_choice(choice, s)   
    if choice != None and len(choice) == 1 and isinstance(choice, set):
        choice = choice.pop()

    P = s # Keep track of the original set
    cn = frozenset()
    if choice != None:
        # Resolve P & update accordingly
        l = choice[0]
        nl = cnf.neg(l)
        c1 = choice[1]
        c2 = choice[2]
        c1_n = cpywo(c1, l) if l in c1 else cpywo(c1, nl)
        c2_n = cpywo(c2, l) if l in c2 else cpywo(c2, nl)
        cn = c1_n.union(c2_n)
        if debug:
            print("[res_a] Resolvent Clause : " + str(cn))        

        # Add the resolvent clause in
        P = sremove(P, c1) # Remove one of the current clauses
        P = sreplace(P, c2, cn) # Replace the other clause with the resolvent clause

        if debug:
            print("[res_a] Resolved P : " + str(P))

    if choice == None and debug:
        print("[res_a] Resolvent Clause : " + str(cn))

    # If PN == P (i.e. nothing has changed) return SAT     
    if P == s:
        if debug:
            print("[res_a] PN == P, .: SAT")
        return True

    # If the resolvent clause is [] (i.e. frozenset()), return UNSAT
    if cn == frozenset():
        if debug:
            print("[res_a] [] .: UNSAT")
        return False

    # Call the thing again
    res_a(P)  
