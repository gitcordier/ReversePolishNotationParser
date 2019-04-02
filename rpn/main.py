from rpn import * 

e = '10 3 ** 9 3 ** +'
f = '12 3 ** 1 3 ** +'

def test():
    return compute(e) is compute(f)

r = compute(e)
s = compute(f)

print('Hello World!{}Did you know that {} = {} = {} ?'.format(
    '\n', e, f, s*(r==s)))

if __name__ == '__main__':
    import timeit
    t = timeit.timeit("test()", setup="from __main__ import test", number = 1000)
    print('Average computation time: {} µs .'.format(str(round(1000*t, 1))))
    
