# RPN

## What is implemented
Package rpn encloses an implementation of computation after the RPN (Reverse
Polish Notation, or 'postfixed notation') norm (
see http://codingdojo.org/kata/RPN/).

We aim at mimicking what a human does as it reads a RPN expression. 
For instance, '1 2 + 3 +' reads off '3 3 +', which means '3 + 3' in regular 
notation.
The algorithm is then iterative, straightforward, and naive: 
There are no stack-like abstractions, nor recursive calls.

Human-readable structures (namely, dictionaries) were preferred. 
In other words, figures like x[i][1] are discarded in favor of the more self-
explanatory x[i]['value'].

## Package Structure
### rpn
The core package is rpn, which encloses the routines script rpn.py.
When run, main.py loads rpn.py and eventually displays a famous numerical 
result, computed from RPN expressions (see 
https://en.wikipedia.org/wiki/Taxicab_number for further reading).

### test_rpn
test_rpn encloses test_rpn.py, which is a unittest script.
Two inputs are given: 
1. input_comfirm.json (in ./inputs): The results to comfirm.
2. input_refute.json (in ./inputs): The results to refute.
Those results are intentionally wrong. Any match is then an evidence that the 
implementation is flawed. Moreover, it may reveal where the bug is.

Symmetrically, two outputs are given: 
1. putput_comfirm_erros.json (in ./outputs): Keeps track of results that could
not be comfirmed.
2. output_refute_erros.json (in ./outputs): Keeps track of various misleadings.

## Math conventions
Let us stress that constants are indentified with constant (0-ary) operators. 
This means that whatsoever the parameter(s) a, b, c, … is(are), 
C(a, b, c, …) = C, provided a constant C.

In terms of RPN, this means that any list of constants '… Z … C B A' reads off
'A'.

## Code conventions
We wanted the if, elif pattern to emulate the switch one. So, this is why we 
wrote if, elif, …, elif, else. We believe that repeatedly writing 'else: pass'
is worth the clarity benefit: Sticking to this convention makes some room for
debugging and further improvements.

## TODOS
Enrich and organize the input json files. For example, enlist expressions and
all suitable operand permutations (could be done with itertools), in order to 
prove that the parsing is stable under such permutation (e.g ' 1 2 3 + + ' 
must be shown as equivalent to '1 3 2 + +', ' 2 1 3 + + ', and so on).


