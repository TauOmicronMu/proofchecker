import re

import parser

debug = True

def cnf(exp):
    lit_r = re.compile('\-?[a-zA-Z0-9]{1}')

    # If exp is a variable then just return exp.
    try:
        if(len(lit_r.findall(exp)) == 1):
            return exp
    except TypeError:
        pass # It isn't a literal, but we should just carry on


    # If exp is in the form P <-> Q, return cnf((P & Q) V (~P & ~Q))
    if(exp[0] == '='):
        if(debug):
            print("exp in form P <-> Q")
        return cnf(('|', ('&', exp[1], exp[2]), ('&', ('-', exp[1]), ('-', exp[2]))))


    # If exp is in the form P -> Q, return cnf(~P V Q) [equivalence]
    if(exp[0] == ':'):
        if(debug):
            print("exp in form P -> Q")
        return cnf(('|', ('-', exp[1]), exp[2]))

    # If exp is in the form ~(...) :
    #    - if exp is in the form ~(~P) return cnf(P) [Double Neg]
    #    - if exp is in the form ~(P & Q) return cnf(~P V ~Q) [deMorgan's]
    #    - if exp is in the form ~(P V Q) return cnf(~P & ~Q) [deMorgan's] 
    if(exp[0] == '-'):
        if(debug):
            print("exp in form ~(...)")
        try:
            if(len(lit_r.findall(exp)) == 1):
                return exp[1]
        except TypeError:
            pass # Not a literal, so carry on...
        if(exp[1][0] == '-'):
            if(debug):
                print("Double Neg!")
            return cnf(exp[1][1]) # [Double Neg]
        if(exp[1][0] == '&'):
            if(debug):
                print("Nand!")
            return cnf(('|', ('-', exp[1][1]), ('-', exp[1][2])))
        if(exp[1][0] == '|'): 
            if(debug):
                print("Nor!")
            return cnf(('&', ('-', exp[1][1]), ('-', exp[1][2])))

    # If exp is in the form P & (Q V R), return (P & Q) V (P & R) [distributivity]
    if(exp[0] == '&'):
        if(debug):
            print("exp in form P & Q")
        if(exp[1][0] == '&'): # (P V Q) & R
            return cnf(('|', ('&', exp[2], exp[1][1]), ('&', exp[2], exp[1][2])))
        if(exp[2][0] == '&'): # P & (Q V R)
            return cnf(('|', ('&', exp[1], exp[2][1]), ('&', exp[1], exp[2][2])))
        print(exp)
        print(exp[1])
        print(exp[1][1])
        return ('&', cnf(exp[1]), cnf(exp[2]))


    # If exp is in the form P V (Q & R), return (P V Q) & (P V R) [distributivity] 
    if(exp[0] == '|'):
        if(debug):
            print("exp in form P V Q")
        if(exp[1][0] == '|'): # (P & Q) V R
            return cnf(('&', ('|', exp[2], exp[1][1]), ('|', exp[2], exp[1][2])))
        if(exp[2][0] == '|'): # P V (Q & R)
            return cnf(('&', ('|', exp[1], exp[2][1]), ('|', exp[1], exp[2][2])))
        return exp


print(cnf(parser.parse("((A -> B) & (C -> D)) & (E -> F)")))
