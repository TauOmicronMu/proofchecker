import sys

import parser
import cnf
import res

args = sys.argv

def satcheck():
    if len(args) != 3:
        print("Wrong arg length! Usage: python3 cmdln <expression>")
        return
    flag = args[1]
    expr = args[2]
    if flag == "cnf":
        return cnf.clause_nf(expr)
    if flag == "res": 
        return res.res(expr)
    if flag == "dpll":
        return dpll.DPLL(cnf.clause_nf(parser.parse(expr)))
    res.res(args[1])

satcheck()
