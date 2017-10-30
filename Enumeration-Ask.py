from math import isclose
from collections import deque
import pandas as pd


def main():
    bn = build_network('data1.csv', 'bn1.json')
    enumerate_all('Good Engine', {'High Mileage': True}, bn)

if __name__ == '__main__':
    main()

def build_network(name, json):
    prob_table = {}
    count = 0
    count_not = 0
    df = pd.read_csv(name)
    for word in json:
        if len(word) == 0:
            for i in range(len(df)):
                if df[word][i] == 'TRUE':
                    count += 1
                else:
                    count_not += 1
            prob_table.update({word: tuple((count, count_not))})
        if len(word) == 1:
            for i in range(len(df)):
                if df[word][i] == 'TRUE':
                    count += 1
                else:
                    count_not += 1
            prob_table.update({word: tuple((count, count_not))})
        if len(word) == 2:
            for i in range(len(df)):
                if df[word][i] == 'TRUE':
                    count += 1
                else:
                    count_not += 1
            prob_table.update({word: tuple((count, count_not))})
    return prob_table

def enumeration_ask(X, e, bn):
    assert X not in e, "Query variable must be distinct from evidence"
    Q = ProbDist(X)
    for xi in bn.variable_values(X):
        Q[xi] = enumerate_all(bn.variables, extend(e, X, xi), bn)
    return Q.normalize()


def enumerate_all(variables, e, bn):
    if not variables:
        return 1.0
    Y, rest = variables[0], variables[1:]
    Ynode = bn.variable_node(Y)
    if Y in e:
        return Ynode.p(e[Y], e) * enumerate_all(rest, e, bn)
    else:
        return sum(Ynode.p(y, e) * enumerate_all(rest, extend(e, Y, y), bn)
                   for y in bn.variable_values(Y))


def normalize(dist):
    """Multiply each number by a constant such that the sum is 1.0"""
    if isinstance(dist, dict):
        total = sum(dist.values())
        for key in dist:
            dist[key] = dist[key] / total
            assert 0 <= dist[key] <= 1, "Probabilities must be between 0 and 1."
        return dist
    total = sum(dist)
    return [(n / total) for n in dist]


def extend(s, var, val):
    """Copy the substitution s and extend it by setting var to val; return copy."""
    s2 = s.copy()
    s2[var] = val
    return s2


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        """Return true if numbers a and b are close to each other."""
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class ProbDist:
    """A discrete probability distribution. You name the random variable
    in the constructor, then assign and query probability of values.
    #>>> P = ProbDist('Flip'); P['H'], P['T'] = 0.25, 0.75; P['H']
    0.25
    #>>> P = ProbDist('X', {'lo': 125, 'med': 375, 'hi': 500})
    #>>> P['lo'], P['med'], P['hi']
    (0.125, 0.375, 0.5)
    """

    def __init__(self, varname='?', freqs=None):
        """If freqs is given, it is a dictionary of values - frequency pairs,
        then ProbDist is normalized."""
        self.prob = {}
        self.varname = varname
        self.values = []
        if freqs:
            for (v, p) in freqs.items():
                self[v] = p
            self.normalize()

    def __getitem__(self, val):
        """Given a value, return P(value)."""
        try:
            return self.prob[val]
        except KeyError:
            return 0

    def __setitem__(self, val, p):
        """Set P(val) = p."""
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def normalize(self):
        """Make sure the probabilities of all values sum to 1.
        Returns the normalized distribution.
        Raises a ZeroDivisionError if the sum of the values is 0."""
        total = sum(self.prob.values())
        if not isclose(total, 1.0):
            for val in self.prob:
                self.prob[val] /= total
        return self

    def show_approx(self, numfmt='{:.3g}'):
        """Show the probabilities rounded and sorted by key, for the
        sake of portable doctests."""
        return ', '.join([('{}: ' + numfmt).format(v, p)
                          for (v, p) in sorted(self.prob.items())])

    def __repr__(self):
        return "P({})".format(self.varname)


def topological(g):
    degrees = []
    x = []
    queue = deque()
    while len(queue) > 0:
        node = queue.pop()
        x += [node]
        for child in node:
            degrees[child] -= 1
            if degrees[child] == 0:
                queue.append([child])
    return x
