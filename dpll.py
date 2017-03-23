import parser

from cnf import * 
from res import *

debug = True

def DPLL(P):
    '''
        Implementation of the standard DPLL procedure for SAT solving.
        
        DPLL(Φ):
            If Φ is a consistent set of literals
                return true
            If Φ contains an empty clause
                return false
            for φ ∈ Φ
                Φ <- propagate(φ, Φ)
            for ψ ∈ φ ∈ Φ, pure(ψ)
                Φ <- propagate(ψ, Φ)
            φ <- choose_literal(Φ)
            return DPLL(Φ ∩ φ) or DPLL(Φ ∩ ¬φ)
    '''
    if P == set() : # If P is an empty set - i.e. a set of consistent literals return SAT
        return True
    if frozenset() in P: # If P contains box (frozenset()) - return UNSAT
        return False
    copyP = P
    for p in P: # Unit Propagation
        if len(p) == 1:
            if debug:
                print("[DPLL] Unit Propagation : " + str(p))
            copyP = propagate(next(iter(p)), copyP)
    P = copyP
    if debug:
        print("[DPLL] Post-Unit Propagation : " + str(P))
    # TODO: Make a choice and return the branched result on that choice
    pass # TODO: Implement this :D 

def propagate(l, P):
    '''
        Propagate the interpretation, l = T through
        the clauses in the set P. Return the new
        set, with any simplifications etc.
    '''
    ret_val = set()
    for c in P: 
        if neg(l) in c:
            ret_val.add(cpywo(c, neg(l))) # Remove this because it can never be true :) 
        elif l not in c:
            ret_val.add(l) # Only add the clause if it isn't now true!
    return ret_val 
        

