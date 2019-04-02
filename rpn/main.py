#!/usr/bin/python3
#coding:utf-8

'''
    Loads rpn.py and eventually displays a famous numerical result, 
    computed from RPN expressions (see 
        https://en.wikipedia.org/wiki/Taxicab_number
    ) for further reading.
'''
from rpn import * 

__author__      = 'gitcordier'
__copyright__   = 'XXX'
__credits__     = ['lF']
__license__     = 'Nope'
__version__     = '0.0.1'
__email__       = ''
__status__      = 'Prototype'


E = '10 3 ** 9 3 ** +'
F = '12 3 ** 1 3 ** +'

def test():
    return compute(E) is compute(F)

R = compute(E)
S = compute(F)

print('Hello World!{}Did you know that {} = {} = {} ?'.format(
    '\n', E, F, S*(R==S)))

if __name__ == '__main__':
    import timeit
    N = 1000            # Number of iterations
    M = 1000000        # 10**6. Needed to convers s into µs.
    t = timeit.timeit('test()', setup='from __main__ import test', number = N)
    a = (M * t) / N     # Average time, in µs.
    print('Average computation time: {} µs .'.format(str(round(a, 1))))

# END

