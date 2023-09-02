#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# A recursive descent parser in C for simple arithemic expressions.
# The scanner is not separated from the parser. Each nonterminal corresponds
# to a function, the correspoding productions are shown as a comment at the
# header of the function. The grammar is modified to be predictive.

# tokens and corresponding values as returned by the scanner
# Question 7
EOI = 0     # end of input
VAR = 1     # \$[A-Za-z]*
TRUE = 2    # "True"
FALSE = 3   # "False"
OR = 4      # "or"
AND = 5     # "and"
NOT = 6     # "not"
EQ = 7      # "="
LP = 8      # "\("
RP = 9      # "\)"
ERR = 11    # error
    
# Question 8
# Grammar
# <expr> -> VAR <tail1> | {TRUE FALSE} <bin_expr> | LP <expr> RP <bin_expr> | NOT <factor> <bin_expr>
# <tail1> -> EQ <expr> <bin_expr> | <bin_expr>
# <bin_expr> ->  {AND OR} <expr> <bin_expr> | epsilon
# <factor> -> TRUE | FALSE | VAR | LP <expr> RP | NOT <factor>

import sys
debug = True

def show(indent,name,s,spp):
    if debug:
        print(indent+name+'("',end='');
        j = len(s)
        for i in range(spp,j):
            print(s[i],sep="",end="")
        print('")',end='\n')
        return
    else:
        return
#end show

def x(indent,name1,name2):
    if debug:
        print(indent+"returned to "+name1+" from "+name2)
    else:
        return
#end x



def EatWhiteSpace(s,spp):
    j = len(s)
    if spp >= j:
        return spp

    while s[spp] == ' ' or s[spp] == '\n':
        spp=spp+1
        if spp >= j:
            break
        
    return spp
#end EatWhiteSpace


# <expr> -> VAR <tail1> | {TRUE FALSE} <bin_expr>  | LP <expr> RP <bin_expr> | NOT <factor> <bin_expr>
# function expr ------------------------------------------------------------
def expr(s,spp,indent):
    show(indent,'expr',s,spp)
    indent1 = indent+' '

    token = LookAhead(s,spp)
    if token == VAR:
        spp = ConsumeToken(s,spp)
        res,spp = tail1(s,spp,indent1)
        x(indent1,"expr","tail1")
        return res,spp
    elif token == TRUE or token == FALSE:
        spp = ConsumeToken(s,spp)
        res,spp = bin_expr(s,spp,indent1)
        x(indent1,"expr","tail2")
        return res,spp
    elif token == LP:
        spp = ConsumeToken(s,spp)
        res,spp = expr(s,spp,indent1)
        x(indent1,"expr","expr")
        if not res:
            return False,spp
        token,spp = NextToken(s,spp)
        if token == RP:
            res,spp = bin_expr(s,spp,indent1)
            x(indent1,"expr","bin_expr")
            return res,spp
        else:
            return False,spp
    elif token == NOT:
        spp = ConsumeToken(s,spp)
        res,spp = factor(s,spp,indent1)
        x(indent1,"expr","factor")
        if not res:
            return False,spp
        res,spp = bin_expr(s,spp,indent1)
        x(indent1,"expr","tail2")
        return res,spp
    else:
        return False,spp
#end prog


# <tail1> -> EQ <expr> <bin_expr> | <bin_expr>
# function tail1 --------------------------------------------------------
def tail1(s,spp,indent):
    show(indent,'tail1',s,spp)
    indent1 = indent+' '

    token = LookAhead(s,spp)
    if token == EQ:
        spp = ConsumeToken(s,spp)
        res,spp = expr(s,spp,indent1)
        x(indent1,"tail1","expr")
        if not res:
            return False,spp
        res,spp = bin_expr(s,spp,indent1)
        x(indent1,"tail1","bin_expr")
        return res,spp
    
    else:
        res,spp = bin_expr(s,spp,indent1)
        x(indent1,"tail1","bin_expr")
        return res,spp

#end tail1

    

# <bin_expr> ->  {AND OR} <expr> <bin_expr> | epsilon
# function tail2 --------------------------------------------- 
def bin_expr(s,spp,indent):
    show(indent,'tail2',s,spp)
    indent1 = indent+' '

    token = LookAhead(s,spp)
    if token == AND or token == OR:

        spp = ConsumeToken(s,spp)
        res,spp = expr(s,spp,indent1)
        x(indent1,"bin_expr","expr")
        if not res:
            return False,spp
        res,spp = bin_expr(s,spp,indent1)
        x(indent1,"bin_expr","bin_expr")
        return res,spp
    else:
        return True,spp  #epsilon
#end tail2


# <factor> -> TRUE | FALSE | VAR | LP <expr> RP | NOT <factor>
# function factor --------------------------------------------- 
def factor(s,spp,indent):
    show(indent,'factor',s,spp)
    indent1 = indent+' '

    token,spp = NextToken(s,spp)
    if token == TRUE:
        return True,spp
    elif token == FALSE:
        return True,spp
    elif token == VAR:
        return True,spp
    elif token == LP:
        res,spp = expr(s,spp,indent1)
        x(indent1,"factor","expr")
        if not res:
            return False,spp
        token,spp = NextToken(s,spp);
        return (token == RP),spp
    elif token == NOT:
        res,spp = factor(s,spp,indent1)
        x(indent1,"factor","factor")
        
        return res,spp
    else:
        return False,spp
#end factor


# the scanner ####################################################
# function LookAhead ------------------------------------------- 
def LookAhead(s,spp):
    j = len(s);
    i = spp
    if i >= j:
        return EOI
    while s[i]==" " or s[i]=="\n":
        i = i+1
        if i >= j:
            return EOI

    if s[i] == '=':
        return EQ
    elif s[i:i+3] == "and":
        return AND
    elif s[i:i+2] == "or":
        return OR
    elif s[i:i+4] == "True":
        return TRUE
    elif s[i:i+5] == "False":
        return FALSE
    elif s[i:i+3] == "not":
        return NOT
    elif s[i] == "(":
        return LP
    elif s[i] == ")":
        return RP
    elif s[i] == "$":
        return VAR
    else:
        return ERR
#end LookAhead


# function NextToken --------------------------------------------- 
def NextToken(s,spp):
    spp1 = spp
    spp = EatWhiteSpace(s,spp)
    j = len(s)
    if spp >= j:
        return ERR,spp1

    if spp >= j:
        return EOI,spp
    elif s[spp] == '=':
        return EQ,spp+1
    elif s[spp:spp+3] == "and":
        return AND,spp+3
    elif s[spp:spp+2] == "or":
        return OR,spp+2
    elif s[spp:spp+4] == "True":
        return TRUE,spp+4
    elif s[spp:spp+5] == "False":
        return FALSE,spp+5
    elif s[spp] == "(":
        return LP,spp+1
    elif s[spp] == ")":
        return RP,spp+1
    elif s[spp:spp+3] == "not":
        return NOT,spp+3
    elif s[spp] == "$":
        run = True
        x = 1
        while run:
            if spp+x < j:
                if (ord(s[spp + x])>=ord('a') and ord(s[spp + x])<=ord('z')) or (ord(s[spp + x])>=ord('A') and ord(s[spp + x])<=ord('Z')):
                    x += 1
                else:
                    break
            else:
                break

        return VAR,spp+x

    else:
        return ERR,spp1
#end NextToken

#function ConsumeToken
def ConsumeToken(s,spp):
    token,spp = NextToken(s,spp)
    return spp
#end ConsumeToken




#main section
s = "$IvanEbos"
res,spp = expr(s,0,"");

spp = EatWhiteSpace(s,spp)
if spp < len(s):
    print("parse Error")
else:
    if res:
        print("parsing OK")
    else:
        print("parse Error")
#end main section
                