import re

'''
FOLLOWS THE FOLLOWING PSEUDOCODE: 

CONVERT(φ):   // returns a CNF formula equivalent to φ

// Any syntactically valid propositional formula φ must fall into
// exactly one of the following 7 cases (that is, it is an instanceof
// one of the 7 subclasses of Formula).

If φ is a variable, then:
   return φ.
   // this is a CNF formula consisting of 1 clause that contains 1 literal

If φ has the form P ^ Q, then:
   CONVERT(P) must have the form P1 ^ P2 ^ ... ^ Pm, and
   CONVERT(Q) must have the form Q1 ^ Q2 ^ ... ^ Qn,
   where all the Pi and Qi are disjunctions of literals.
   So return P1 ^ P2 ^ ... ^ Pm ^ Q1 ^ Q2 ^ ... ^ Qn.

If φ has the form P v Q, then:
   CONVERT(P) must have the form P1 ^ P2 ^ ... ^ Pm, and
   CONVERT(Q) must have the form Q1 ^ Q2 ^ ... ^ Qn,
   where all the Pi and Qi are dijunctions of literals.
   So we need a CNF formula equivalent to
      (P1 ^ P2 ^ ... ^ Pm) v (Q1 ^ Q2 ^ ... ^ Qn).
   So return (P1 v Q1) ^ (P1 v Q2) ^ ... ^ (P1 v Qn)
           ^ (P2 v Q1) ^ (P2 v Q2) ^ ... ^ (P2 v Qn)
             ...
           ^ (Pm v Q1) ^ (Pm v Q2) ^ ... ^ (Pm v Qn)

If φ has the form ~(...), then:
  If φ has the form ~A for some variable A, then return φ.
  If φ has the form ~(~P), then return CONVERT(P).           // double negation
  If φ has the form ~(P ^ Q), then return CONVERT(~P v ~Q).  // de Morgan's Law
  If φ has the form ~(P v Q), then return CONVERT(~P ^ ~Q).  // de Morgan's Law

If φ has the form P -> Q, then:
  Return CONVERT(~P v Q).   // equivalent

If φ has the form P <-> Q, then:
  Return CONVERT((P ^ Q) v (~P ^ ~Q)).

If φ has the form P xor Q, then:
  Return CONVERT((P ^ ~Q) v (~P ^ Q)).

'''
def cnf(exp):
    # If exp is a variable then just return exp.
    var_r = re.compile('\-?[a-zA-Z0-9]{1}')
    if(len(var_r.findall(exp)) == 1):
        return exp  

    # If exp is in the form P & Q, return P1 & P2 & ... & Pm & Q1 & Q2 & ... & Qm
        

    # If exp is in the form P V Q, return all permutations of the combination of Px and Qx 
    # i.e. (P1 V Q1) & (P1 V Q2) & ... & (P1 V Qn)
    #    & (P2 V Q1) & (P2 V Q2) & ... & (P2 V Qn) etc.
    
    # If exp is in the form ~(...) :
    #    - if exp is in the form ~A,   return exp
    #    - if exp is in the form ~(~A) return cnf(A)
    #    - if exp is in the form ~(P & Q) return cnf(~P V ~Q) [deMorgan's]
    #    - if exp is in the form ~(P V Q) return cnf(~P & ~Q) [deMorgan's] 
    
    # If exp is in the form P -> Q, return cnf(~P V Q) [equivalence]

    # If exp is in the form P = Q, return cnf((P & Q) V (~P & ~Q))
