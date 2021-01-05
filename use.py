import numpy as np
from cvxopt import matrix, solvers
solvers.options['glpk'] = {'tm_lim': 1000} # max timeout for glpk
from cvxopt_examples import LinProg

class TestMinimax():
    def test_0(self):
        """
        http://cvxopt.org/examples/tutorial/lp.html
        """
        lp = LinProg(verbose=False)
        A = matrix([ [-1.0, -1.0, 0.0, 1.0], [1.0, -1.0, -1.0, -2.0] ])
        b = matrix([ 1.0, -2.0, 0.0, 4.0 ])
        c = matrix([ 2.0, 1.0 ])
        sol = solvers.lp(c, A, b, solver="glpk")
        probs = sol["x"]
        print("test_0:\n{}".format(probs))

    def test_1(self):
        """
        https://www.cs.duke.edu/courses/fall12/cps270/lpandgames.pdf
        """
        lp = LinProg(verbose=False)
        A = [[0,-1,1],[1,0,-1],[-1,1,0]]
        sol = lp.maxmin(A=A, solver="glpk")
        probs = sol["x"]
        print("test_1:\n{}".format(probs))

    def test_2(self):
        """
        https://en.wikipedia.org/wiki/Minimax#Example
        """
        lp = LinProg(verbose=True)
        A = [[3,-2,2],[-1,0,4],[-4,-3,1]]
        sol = lp.maxmin(A=A, solver="glpk")
        probs = sol["x"]
        print("test_2:\n{}".format(probs))

    def test_ce_1(self):
        """
        Example p 28: https://www3.ul.ie/ramsey/Lectures/Operations_Research_2/gametheory4.pdf
        """
        A = [[2, 5], [0, 0],
                [0, 0], [5, 2]]
        A = np.array(A)
        lp = LinProg(verbose=True)
        sol = lp.ce(A=A, solver="glpk")
        probs = sol["x"]
        equil = probs[0] + probs[3]
        print("test_ce_1:\n{}".format(probs))

    def test_ce_2(self):
        """
        Example Chicken game: https://www.cs.rutgers.edu/~mlittman/topics/nips02/nips02/greenwald.ps
        """
        A = [[6, 6], [2, 7],
                [7, 2], [0, 0]]
        A = np.array(A)
        lp = LinProg(verbose=True)
        sol = lp.ce(A=A, solver="glpk")
        probs = sol["x"]
        print("test_ce_2:\n{}".format(probs))

    def test_ce_3(self):
        """
        Example Chicken game: https://www.cs.duke.edu/courses/fall16/compsci570/LPandGames.pdf
        """
        A = [[0, 0], [-1, 1],
                [1, -1], [-5, -5]]
        A = np.array(A)
        lp = LinProg(verbose=True)
        sol = lp.ce(A=A, solver="glpk")
        probs = sol["x"]
        print("test_ce_3:\n{}".format(probs))


if __name__ == "__main__":
    tt = TestMinimax()
    tt.test_0()
    tt.test_1()
    tt.test_2()
    tt.test_ce_1()
    tt.test_ce_2()
    tt.test_ce_3()