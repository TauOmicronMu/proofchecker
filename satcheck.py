import sys

import parser
import cnf
import res

args = sys.argv

def satcheck():
    if len(args) != 2:
        print("Wrong arg length! Usage: python3 satcheck <expression>")
        return
    res.res(args[1])

satcheck()
