#!/usr/bin/python3
#coding:utf-8

'''
    Implements a RPN (Reverse Polish Notation) parser. 
'''

from json   import load
from math   import sqrt, nan
from string import digits

from rpn    import * 


__author__      = 'gitcordier'
__copyright__   = 'XXX'
__credits__     = ['lF']
__license__     = 'Nope'
__version__     = '0.0.1'
__email__       = ''
__status__      = 'Prototype'


ARITY           = 'arity'
VALUE           = 'value'
N               = 'N'
MAX             = 'MAX'
MIN             = 'MIN'
PROJ            = 'PROJ'
SQRT            = 'SQRT'
ALPHABET        = digits + '+-'
UNARY_OPERATORS = [SQRT]
BINARY_OPERATORS= ['+', '-', '*','/', '**', '^']
N_ARY_OPERATORS = [MAX, MIN,PROJ]
OPERATORS       = {
    1: UNARY_OPERATORS,
    2: BINARY_OPERATORS,
    N: N_ARY_OPERATORS
}
UNDEFINED       = ''

def as_dict(number_or_string, check=True):
    '''
        Given a term, as_dict returns a dictionary {arity, value} 
        that captures in a human-readable fashion the so provided 
        information. 
        
        check is an optional boolean that specifies how we look for 
        unexpected symbols i. other than digits, '+', '-'.
        It defaults to True, which means that any illegal symbol 
        (e.g '√', ∏, @, %) yields nan.
    '''
    
    value   = number_or_string
    arity   = UNDEFINED
    r ={ARITY: arity, VALUE: value}
    
    for k in OPERATORS:
        if number_or_string in OPERATORS[k]:
            r[ARITY] = k
            return  r
    if arity is UNDEFINED:
        # At this point, s then denotes a 0-ary operator, 
        # i.e.a constant…
        # … Unless str(s) contains an illegal symbol.
        
        # If check…
        if check:
            # TODO
            if all(e in ALPHABET for e in number_or_string):
                arity       = 0
                s_as_float  = float(number_or_string)
                s_as_int    = int(number_or_string)
            
                if s_as_float == s_as_int:
                     value = s_as_int
                else:
                     value = s_as_float
            
        # If not (safe when s is necessarily a number, 
        # e.g. as a routine output).
        else:
             arity, value = 0, number_or_string
    
    return {ARITY: arity, VALUE: value}
    
    

# From now on, the term vector denotes a list of dictionaries 
# {arityvalue} (see above).

def compute_zero_ary(x, i):
    '''
        Given a vector x, gets the i-th value, namely x[i-1][value].
        
        In other words, provided constants(s) 
            x[0][value], …, x[i-1][value], 
        the current function returns x[i-1][value], the i-th value.
        Such specs encompass the following pattern and its 
        iterations: 
            'a b … z' (as a, b … z are constants): The right operator 
        is the constant z. The result is then z.
        For instance, 2 2 + 3 3 * = 4 9 = 9.
        
    '''
    
    return x[i-1][VALUE]
    
def compute_unary(x, i):
    '''
        If x[i] depicts a 1-ary operator T, then x[i-1][value] is 
        passed to T. 
            .
        The so obtained result is returned. 
        If not, nan is returned.
    '''
    
    r = nan
    
    if x[i][VALUE] == SQRT:
        r = sqrt(x[i-1][VALUE])
    
    return r

def compute_binary(x, i):
    '''
        If x[i] (i > 1) depicts a binary operator T (e.g +, *, **), 
        then x[i-2][value] T x[i-1][value] is returned. 
        Otherwise, nan is returned.
        
        For instance, if T is the power operation **, then 
            
            x[i-2][value] ** x[i-1][value] 
        
        shall be returned.
        Beware the ordering (by decreasing indexes), since T may be 
        noncommutative (like **).
        
    '''
    
    r = nan
    a = x[i-2][VALUE]
    b = x[i-1][VALUE]
    c = x[i  ][VALUE]

    if c is '+':
        r = a + b 
    elif c is '-':
        r = a - b
    elif c is '*':
        r = a * b
    elif c in ['**', '^']:
        return a ** b
    elif c is '/':
        r = a / b
    else:
        pass
    
    return r
    
def compute_n_ary(x, i):
    '''
        If x[i] (i > 0) depicts a n-ary operator (n = 1, 2, 3, …) T, 
        then (x[i-1][value], …, x[0][value]) is passed to T. 
        The so obtained value is returned.
    '''
    
    r = nan
    
    # 1. MAX;
    # 2. MIN;
    # 3. PROJ. Given a vector, returns the fist component's value.
    if x[i][VALUE] == MAX:
        r = max(t[VALUE] for t in x[:i])
    elif x[i][VALUE] == MIN:
        r = min(t[VALUE] for t in x[:i])
    elif x[i][VALUE] == PROJ:
        return x[0][VALUE]
    else:
        pass
    
    return r

# 
def get_computation_method(x):
    '''
        Given a vector x whose length is at least 1, first gets the 
        index i of the first nondegenerate operator. Next, returns 
        the relevant computation method and such index i.
    '''
    
    # The default, i.e. the no-operator-found case.
    c = compute_zero_ary 
    
    # Let us discover the first operator.
    #for i in range(len(x)):
    
    for i in range(len(x)):
        if x[i][ARITY] is 0:    # i.e.not a (nondegenerate) operator.
            continue
        elif x[i][ARITY] is 1:  # Unary operator
            c = compute_unary
        elif x[i][ARITY] is 2:  # Binary operator
            c = compute_binary
        elif x[i][ARITY] is N:  # n-ary operator
            c = compute_n_ary
            x[i][ARITY] = i
        else:
            pass
        
        # An operator T of minimal arity k (k = 1, 2,…) that was found
        # at index i must be preceded by at least k constants 
        # (at index(es) 0, …, i-1, then).
        # This yields the following exit criterion:
        if i >= x[i][ARITY]:    # i.e. everything went fine.
            break
        else:                   # i.e. no chance that it's legal.
            return UNDEFINED, i 
        return c, i
    
    # As anounced, returns the computation method and the index i.
    # Remark that the specs of computation_zero_ary force i to be 
    # len(x) if all tested x[0][value], x[len(x)-1][value] 
    # are constant(s).
    return c, i + (i == len(x) -1  and x[i][ARITY] is 0)

def compute(expression):
    '''
        Given a rpn expression, returns its numerical value. 
        Encloses the very parsing routine.
    '''
    
    r = UNDEFINED
    
    if expression is UNDEFINED:
        r = nan
    else:
        # First, we turn the expression into a vector (see above).
        x = list(map(as_dict, expression.split(' ')))
        
        len_x_initial = len(x)
        
        if len_x_initial is 0:      # Not allowed.
            r = nan
        elif len_x_initial is 1:
                c, i = get_computation_method(x)
                
                if c is UNDEFINED:  # Illegal expression/character‡
                    r = nan
                else:               # Since x has length 1…
                    r = x[0][VALUE]
        else:
            while len(x) > 1:
                # TODO: Length of x can easily be computed on the fly.
                # The below calls 'len(x)' are then unnecessary.
                # Nevertheless, I doubt it's a footprint issue.
                # Check that for later versions.
                c, i = get_computation_method(x)
                
                if c is UNDEFINED:  # Illegal expression/character.
                    r = nan
                    break
                
                # TODO: Explain better what we do with x's slices.
                # Else, 
                # First take the extreme left part of the vector x.
                if i < len(x):
                    y = x[: i-x[i][ARITY]]
                else:
                    y =[]
                
                # Next, compute and append the result:
                y.extend([as_dict(c(x, i), check=False)])
                
                # Finally, concatenate the right part of the vector x.
                y.extend(x[i+1: ])
                x = y
                
                # And so on…
            #
            # If r was not reset to non, i.e.nothing wrong happened:
            if r is UNDEFINED:  
                r = x[0][VALUE] 
    return r

# END

