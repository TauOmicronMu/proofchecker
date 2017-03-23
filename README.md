# Proofchecker
Logic to CNF converter and SAT checker written for the 2nd year Computer Science Reasoning module.

### Logical Expression Format
All expressions should be given in the following form:
##### UnOps :
The unary operators are as follows (precedence decreasing downwards). NB: unary operators have higher precedence than any binary operators.
```
    - : Negation
```
##### BinOps :
The accepted binary operators are as follows (precedence decreasing downwards)
```
    &  : Conjunction
    |  : Disjunction
    -> : Implication
   <-> : Equality
```

## Usage
###### Convert a logical expression to Clause NF
``` 
bash satcheck.sh cnf <expression>
```
###### Use propositional resolution for SAT checking
```
bash satcheck.sh res <expression>
```
###### Use DPLL for SAT checking
```
bash satcheck.sh dpll <expression>
```
###### Use both propositional resolution and DPLL for SAT checking and calculate the time taken for each
```
bash satcheck.sh cmp <expression>
```

## Output
**All** output will be in the output.txt file. 


