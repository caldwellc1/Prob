from collections import deque
import pandas as pd


class Node():
    def __init__(self, board):
        self.prob_table = {}
        self.vars = board.keys()  # {'H', 'W', 'E', 'V'}
        self.board = board
        self.variable_values = [0, 1]

    def build_network(self, name):
        prob_table = {}

        df = pd.read_csv(name)
        for word in self.board:
            count = 0
            count_not = 0
            count_T_T = 0
            count_F_F = 0
            count_T_F = 0
            count_F_T = 0
            count_T_T_T = 0
            count_T_T_F = 0
            count_T_F_T = 0
            count_T_F_F = 0
            count_F_T_F = 0
            count_F_T_T = 0
            count_F_F_T = 0
            count_F_F_F = 0
            parents = self.board.get(word)
            if len(self.board.get(word)) == 0:
                for i in range(len(df)):
                    if df[word][i]:
                        count += 1
                    else:
                        count_not += 1
                count2 = count / (count + count_not)
                count_not2 = count_not / (count + count_not)
                prob_table.update({word: tuple((count2, count_not2))})
            if len(self.board.get(word)) == 1:
                for i in range(len(df)):
                    if df[word][i] and df[parents[0]][i]:
                        count_T_T += 1
                    if df[word][i] and df[parents[0]][i] == False:
                        count_T_F += 1
                    if df[word][i] == False and df[parents[0]][i]:
                        count_F_T += 1
                    else:
                        count_F_F += 1
                count_T_T2 = count_T_T / (count_T_T + count_F_T)
                count_T_F2 = count_T_F / (count_T_F + count_F_F)
                count_F_T2 = count_F_T / (count_F_T + count_T_T)
                count_F_F2 = count_F_F / (count_F_F + count_T_F)
                prob_table.update({word: tuple((count_T_T2, count_T_F2, count_F_T2, count_F_F2))})
            if len(self.board.get(word)) == 2:
                for i in range(len(df)):
                    if df[word][i] and df[parents[0]][i] and df[parents[1]][i]:
                        count_T_T_T += 1
                    if df[word][i] and df[parents[0]][i] and df[parents[1]][i] == False:
                        count_T_T_F += 1
                    if df[word][i] and df[parents[0]][i] == False and df[parents[1]][i]:
                        count_T_F_T += 1
                    if df[word][i] and df[parents[0]][i] == False and df[parents[1]][i] == False:
                        count_T_F_F += 1
                    if df[word][i] == False and df[parents[0]][i] and df[parents[1]][i]:
                        count_F_T_T += 1
                    if df[word][i] == False and df[parents[0]][i] and df[parents[1]][i] == False:
                        count_F_T_F += 1
                    if df[word][i] == False and df[parents[0]][i] == False and df[parents[1]][i]:
                        count_F_F_T += 1
                    else:
                        count_F_F_F += 1
                count_T_T_T2 = count_T_T_T / (count_T_T_T + count_F_T_T)
                count_T_T_F2 = count_T_T_F / (count_T_T_F + count_F_T_F)
                count_T_F_T2 = count_T_F_T / (count_T_F_T + count_F_F_T)
                count_T_F_F2 = count_T_F_F / (count_T_F_F + count_F_F_F)
                count_F_F_T2 = count_F_F_T / (count_F_F_T + count_T_F_T)
                count_F_T_F2 = count_F_T_F / (count_F_T_F + count_T_T_F)
                count_F_T_T2 = count_F_T_T / (count_F_T_T + count_T_T_T)
                count_F_F_F2 = count_F_F_F / (count_F_F_F + count_T_F_F)
                prob_table.update({word: tuple((count_T_T_T2, count_T_T_F2, count_T_F_T2, count_T_F_F2, count_F_T_T2, count_F_T_F2, count_F_F_T2, count_F_F_F2))})
        return prob_table


def enumeration_ask(X, e, bn):
    Q = [0, 0]
    for xi in bn.variable_values(X):
        e.update({X: xi})
        Q[xi] = enumerate_all(bn.variables, e, bn)
    return normalize(Q)


def enumerate_all(variables, e, bn):
    if not variables:
        return 1.0
    Y, rest = variables[0], variables[1:]
    Ynode = bn.variable_node(Y)
    if Y in e:
        return Ynode.p(e[Y], e) * enumerate_all(rest, e, bn)
    else:
        e.update({Y: y})
        return sum(Ynode.p(y, e) * enumerate_all(rest, e, bn)
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



def main():
    bn = Node({'H': [], 'E': ['H'], 'W': [], 'V': ['E', 'W']})
    bn.prob_table = bn.build_network('data1.csv')
    enumerate_all('E', {'H': 0}, bn)

if __name__ == '__main__':
    main()
