import sys

import parser
import cnf
import res
import dpll

import time

args = sys.argv

def get_time():
    return time.time() * 1000

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
    if flag == "cmp":
        start_time = get_time()
        print("========================= MAIN LOOP =========================")
        res.res(expr)
        timestep = get_time() - start_time
        print("=============== TIME TAKEN : " + str(timestep) + " ===============")
        start_time = get_time() 
        print("========================= DPLL =========================")
        dpll.DPLL(cnf.clause_nf(parser.parse(expr)))
        timestep = get_time() - start_time
        print("=============== TIME TAKEN : " + str(timestep) + " ===============")
        return True

satcheck()
