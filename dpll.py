import parser
import cnf

from res import *

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
    if consistent_literals(P):
        return True
    if frozenset() in P:
        return False
    for p in P:
            

    pass // TODO: Implement this :D 
