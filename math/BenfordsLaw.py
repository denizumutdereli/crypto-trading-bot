import math

class BenfordsLaw():

    def __init__(self):
       self.compute()

    def compute(self):
        # We will analyse the first n Fibonacci numbers
        n = 500
        # The first 2 numbers of the series are 1, 1
        a = b = 1
        # fd is a list such that fd[d] is the number of Fibonacci numbers up to n
        # which start with the digit d. Note that none start with 0!
        fd = [None,2,0,0,0,0,0,0,0,0]

        # Loop over the 3rd, 4th, ..., nth Fibonacci numbers
        for i in range(3,n+1):
            # This is the propagation step: generate the current Fibonacci number, a,
            # as the sum of the last two numbers (a+b), and store the old value of a
            # as b (the old value of b is forgotten).
            a, b = a+b, a
            # The first digit of a
            d = int(a/10**(int(math.log10(a))))
            fd[d] += 1

        # The digits 1,2,3,4,5,6,7,8,9
        digits = range(1,10)
        benford = [None]
        for d in digits:
            # Normalize fd by dividing by n so it represents a probability
            fd[d] /= n
            # Use Benford's Law to predict the frequency of first digit d
            benford.append(math.log10((d+1)/d))

        # Output a table of the predicted and observed distribution of first digits
        print('-'*27)
        print('Digit  Predicted   Observed')
        print('-'*27)
        for d in digits:
            print('  {:1d}       {:5.3f}      {:5.3f}'.format(d, benford[d], fd[d]))
        print('-'*27)

BenfordsLaw()