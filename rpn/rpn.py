#!/usr/bin/python3

__author__      = 'Gabriel Cordier'
__copyright__   = 'Logilab'
__credits__     = ['Laetitia Fraioli']
__version__     = '0.0.1'
__email__       = 'admin@gcordier.eu'
__status__      = 'Development'


from json   import load
from math   import sqrt, nan
from string import ascii_letters, digits

UNDEFINED = ''
ARITY   = 'arity'
VALUE   = 'value'
N       = 'N'
MAX     = 'MAX'
MIN     = 'MIN'
PROJ    = 'PROJ'
SQRT    = 'SQRT'

ALPHABET         = digits + ascii_letters + '+-'
UNARY_OPERATORS  = [SQRT]
BINARY_OPERATORS = ['+', '-', '*','/', '**', '^']
N_ARY_OPERATORS  = [MAX, MIN,PROJ]

def get_arity(s, check=True):
    '''
        Returns the arity of an operator. 
        Bear in mind that constant are 0-ary operators.
        
        check is an optional boolean that specifies how we look for 
        unexpected constants i.e constants that are denoted with 
        symbols other than: digits, ascii lettters, '+', '-'.
        It defaults to True, which means that any illegal symbol 
        (e.g '√', ∏, @, %) yields nan.
    '''
    
    if s in BINARY_OPERATORS:
        arity = 2
    elif s in N_ARY_OPERATORS:
        arity = N
    else:
        if s in UNARY_OPERATORS:
            arity = 1
        
        # At this point, str(s) then denotes a 0-ary operator, 
        # i.e a constant…
        # … Unless str(s) contains an illegal symbol.
        
        # If check…
        elif check:
            if all(e in ALPHABET for e in str(s)):
                arity = 0
            else:
                arity = nan 
        
        # If not (safe when s is necessarily an int,e.g. as a routine 
        # product).
        else:
            arity = 0
    return arity
    
def as_dict(s, check=True):
    '''
        Given a term, as_dict returns a dictionary {arity, value} 
        that captures in a human-readable fashion the so provided 
        information. 
    '''
    arity = get_arity(s, check)
    
    r = {ARITY: arity, VALUE: s}
    
    if arity is 0: #i.e it's a constant.
        r[VALUE] = float(s)
        
        if r[VALUE] == int(s): 
            r[VALUE] = int(s)
    
    return r

# From now on, the term vector denotes list of dictionaries 
# {arityvalue} (see above).

def compute_zero_ary(x, i):
    '''
        Given a vector x, gets the i-th value, namely x[i-1][value].
        
        In other words, provided constants(s) 
            x[0][value], …, x[i-1][value], 
        the current function returns x[i-1][value], the i-th value.
        Such specs encompass the following pattern and its 
        iterations: 
            'a b … z' (as a, b … z are constants): the right operator 
        is the constant z. The result is then z.
        For instance, 2 2 + 3 3 * = 4 9 = 9.
        
    '''
    return x[i-1][VALUE]
    
def compute_unary(x, i):
    '''
        If x[i] depicts a 1-ary operator T, then T is passed 
            x[i-1][value].
        The so obtained result is returned. 
        If not, nan is returned.
    '''
    
    r = nan
    if x[i][VALUE] == SQRT:
        r = sqrt(x[i-1][VALUE])
    return r

def compute_binary(x, i):
    '''
        If x[i] (i > 2) depicts a binary operator T (e.g +, *, **), 
        then x[i-2][value] T x[i-1][value] is returned. 
        Otherwise, nan is returned.
        
        For instance, if T is the power operation **, then 
            
            x[i-2][value] ** x[i-1][value] 
        
        shall be returned.
        Bear in mind the terms ordering (by decreasing indexes), 
        since T may be noncommutative (like **).
        
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
        r = a/b
    else:
        pass
    
    return r
    
def compute_n_ary(x, i):
    '''
        If x[i] (i > 0) depicts a n-ary operator (n = 1, 2, 3, …) T, 
        then T is passed (x[i-1][value], …, x[0][value]). 
        The so obtained result is returned.
    '''
    
    r = nan
    
    if x[i][VALUE] == MAX:
        r = max(t[VALUE] for t in x[:i])
    
    # Two other n-ary operators:
    # 1. MIN, MAX's counterpart
    if x[i][VALUE] == MIN:
        r = min(t[VALUE] for t in x[:i])
    
    # 2. PROJ. Given a vector, returns the fist component's value.
    elif x[i][VALUE] == PROJ:
        return x[0][VALUE]
    return r

# 
def get_computation_method(x):
    '''
        Given a vector x whose length is at least 1, first gets the 
        index i of the first nondegenerate operator. Next, returns 
        the relevant computation method and such index i.
    '''
    
    len_x = len(x)
    
    # The default, i.e. the no-operator-found case.
    c     = compute_zero_ary 
    
    # Let us discover the first operator.
    for i in range(len_x):
        if x[i][ARITY] is 0:    # i.e not a (nondegenerate) operator.
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
    
    # As anounced, returns the computation method and the index i.
    # Remark that the specs of computation_zero_ary force i to be 
    # len(x) whether all tested x[0][value], x[len(x)-1][value] 
    # denotes constant(s).
    return c, i + (i == len_x -1  and x[i][ARITY] is 0)

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
        
        len_x_initial = len(x)  # no repeated calls of len.
        
        if len_x_initial is 0:  # Not allowed.
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
                
                # Else, 
                # First take the extreme left part of the vector x,
                # which will be parsed later.
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
            # If r was not reset to non, i.e nothing wrong happened:
            if r is UNDEFINED:  
                r = x[0][VALUE] 
    return r

# END


