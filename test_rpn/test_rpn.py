#!/usr/bin/python3

__author__      = 'Gabriel Cordier'
__copyright__   = 'Logilab'
__credits__     = ['Laetitia Fraioli']
__version__     = '0.0.1'
__email__       = 'admin@gcordier.eu'
__status__      = 'Development'

import math
import unittest

from itertools  import filterfalse
from json       import load, dump
from rpn.rpn    import *

POSTFIX         = 'pofix' #Portemanteau from 'postfix and 'Polish'.
COMFIRM, REFUTE = 'comfirm', 'refute'
KEYS            = ('number',    'rpn',    'result')
E, P, R         = ('expression', POSTFIX, 'result')
OUTPUTS_ERRORS  = 'test_rpn/outputs/output_{}_errors.json'
INPUTS_COMFIRM  = 'test_rpn/inputs/input_comfirm.json'
INPUTS_REFUTE   = 'test_rpn/inputs/input_refute.json'

class TestCaseRPN(unittest.TestCase):
    '''
        The Unittest class.
        We aim at comfirming some results and refuting other ones. 
    '''
    
    def compare(self, ex):
        '''Given an expression ex and a precomputed result R, compare 
            calls the solver then so obtain a results R'. Compare 
            returns True if R = R'.If not, it returns False. Our 
            convention about nan is that nan is identified with nan 
            ('a mistake is a mistake'). So, compare returns True 
        whether R and R' are nan.
        '''
        
        u, v, b = compute(ex[E][P]), ex[R], False
        
        if all(x in (nan, 'NaN') for x in (u, v)):
            b = True
        elif u == v:
            b = True
        return b
        
    def setUp(self):
        '''
            Our setUp method.
            Loads the correct results (to be comfirmed, then), and 
            the wrong ones (the ones that must be refused).
        '''
        
        self.comfirm_results = []
        self.refute_results  = []
        
        with open(INPUTS_COMFIRM, encoding='UTF-8') as c:   
            self.comfirm = load(c)
        with open(INPUTS_REFUTE, encoding='UTF-8') as r:
            self.refute = load(r)
    
    def proof_rpn(self, proof):
        '''
            hh
        '''
        if proof is COMFIRM:
            data    = self.comfirm 
            results = self.comfirm_results
            method  = filterfalse   # We are interested in what FAILS.
        elif proof is REFUTE:
            data    = self.refute
            results = self.refute_results
            method  = filter        # If it's True, then it's WRONG.
        else:
            pass
        
        def info(dct):
            '''
                Given a test result (dictionary-shaped), returns a 
                string that sum it up (sucess rate is given, so that 
                we know if our implementation is refused, or not.)
            '''
            
            def rate():
                '''
                    Computes the success rate of the current test. 
                '''
                
                len_data = len(data)
                
                if len(dct) is 0: # Which means: No failure.
                    r, b = 100, True
                elif len(dct) is len_data:
                    r, b = 0, False
                else:
                    r, b = round(100*((len_data-len(dct))/len_data), 2), False
                return r, b
                
            r, b = rate()
            
            return '\n'.join((
                'Success rate: {} % :'.format(r),
                'Implementation was {}refuted.'.format('not '*b)))
            
        output  = open(OUTPUTS_ERRORS.format(proof), 'w', encoding='UTF-8')
        
        results = list(method(self.compare, data))
        
        dct     = [dict(zip(KEYS, (i, results[i][E][P], results[i][R]))) 
                    for i in range(len(results))]
        
        dump(dct, output, ensure_ascii=False, indent=4)
        
        print(info(dct))
        
        output.close()
        
    def test_rpn_comfirm(self):
        '''
            Comfirmation test.
        '''
        
        return self.proof_rpn(COMFIRM)
        
    def test_rpn_refute(self):
        '''
            Refutation test.
        '''
        
        return self.proof_rpn(REFUTE)
    
    def tearDown(self):
        '''
            Up to now, does nothing, since all file objects are 
            already closed.
        '''
        pass
        
if __name__ == '__main__':
    unittest.main()


