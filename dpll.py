import parser

from cnf import * 
from res import *

debug = True

def DPLL(P):
    '''
        Wrapper for DPLL_a, which is an implementation of the standard
        DPLL procedure for SAT solving. 
    '''
    if debug:
        print("[DPLL] Running DPLL Procedure on : " + str(P))
    sat = DPLL_a(P)
    if sat:
        if debug:
            print("========================= SAT =========================")
        return sat
    if debug:
        print("======================= UNSAT =======================")
    return sat

def DPLL_a(P):
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
            l = next(iter(p))
            if debug:
                print("[DPLL_a] Unit Propagation of : " + str(l) + " on : " + str(copyP))
            copyP = propagate(l, copyP)
            if debug:
                print("[DPLL_a] Result of Unit Propagation : " + str(copyP))
    P = copyP
    if debug:
        print("[DPLL_a] Post-Unit Propagation : " + str(P))
    for p in P: # Pure-Literal Assignment
        for l in p:
            if pure(l, P):
                if debug:
                    print("[DPLL_a] " + str(l) + " is pure, .: propagating l")
                copyP = propagate(l, copyP)
    P = copyP
    if debug:
        print("[DPLL_a] Post-Pure-Literal Assignment : " + str(P))
    if P == set() or frozenset() in P:
        return DPLL_a(P) # This is going to return SAT (yay!) or UNSAT (oh no! :( )
    # Make a choice and return the branched result on that choice
    choice = choose_literal(P)
    left = propagate(choice, P)
    right = propagate(neg(choice), P)
    if debug:
        print("[DPLL_a] Branching - " + str(left) + " : " + str(right))
    return DPLL_a(propagate(choice, P)) or DPLL_a(propagate(neg(choice), P))

def pure(l, P):
    '''
        Given a literal, l, and a set of clauses, P,
        return whether l is pure or not - i.e. if l
        occurs only in the given polarity.
    '''
    for c in P:
        if neg(l) in c:
            return False
    return True

def choose_literal(P):
    '''
        Given a set of clauses, P, chooses a literal to
        branch on.
    '''
    choice = next(iter(next(iter(P))))
    if debug:
        print("[choose_literal] choice : " + str(choice))
    return choice

def propagate(l, P):
    '''
        Propagate the interpretation, l = T through
        the clauses in the set P. Return the new
        set, with any simplifications etc.
    '''
    ret_val = set()
    for c in P: 
        if neg(l) in c:
            if debug:
                print("[propagate] " + str(neg(l)) + " in " + str(c))
            ret_val.add(cpywo(c, neg(l))) # Remove this because it can never be true :) 
            if debug:
                print("[propagate] ret_val : " + str(ret_val))
        elif l not in c:
            if debug:
                print("[propagate] " + str(l) + " not in " + str(c))
            ret_val.add(c) # Only add the clause if it isn't now true!
            if debug:
                print("[propagate] ret_val : " + str(ret_val))
    if debug:
        print("[propagate] result : " + str(ret_val))
    return ret_val 
        

