from collections import deque
import pandas as pd
import itertools
import numpy as np
# False = 0


class Node:
    def __init__(self, board):
        self.prob_table = {}
        self.vars = list(board.keys())
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
                    if df[word][i] == False:
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
                    if df[word][i] == False and df[parents[0]][i] == False:
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
                    if df[word][i] == False and df[parents[0]][i] == False and df[parents[1]][i] == False:
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


def enumeration_ask(X, e, bn, poss):
    Q = [0, 0]
    for xi in bn.variable_values:
        e.update({X: xi})
        Q[xi] = enumerate_all(bn.vars, e, bn)
    return normalize(Q, poss)


def enumerate_all(variables, e, bn):
    if not variables:
        return 1.0
    Y, rest = variables[0], variables[1:]
    if Y in e:
        return get_prob(Y, bn, e.get(Y), e) * enumerate_all(rest, e, bn)
    else:
        return sum(get_prob(Y, bn, y, e) * enumerate_all(rest, up(e, {Y: y}), bn) for y in bn.variable_values)


def up(e, date):
    copy = e.copy()
    copy.update(date)
    return copy


def get_prob(node, bn, tf, e):
    if len(bn.board[node]) == 0:
        if tf:
            return bn.prob_table.get(node)[0]
        else:
            return bn.prob_table.get(node)[1]
    if len(bn.board[node]) == 1:
        parents = bn.board.get(node)
        if tf:
            if e[parents[0]]:
                return bn.prob_table.get(node)[0]
            else:
                return bn.prob_table.get(node)[1]
        else:
            if e[parents[0]]:
                return bn.prob_table.get(node)[2]
            else:
                return bn.prob_table.get(node)[3]
    if len(bn.board[node]) == 2:
        parents = bn.board.get(node)
        if tf:
            if e[parents[0]]:
                if e[parents[1]]:
                    return bn.prob_table.get(node)[0]
                else:
                    return bn.prob_table.get(node)[1]
            else:
                if e[parents[1]]:
                    return bn.prob_table.get(node)[2]
                else:
                    return bn.prob_table.get(node)[3]
        else:
            if e[parents[0]]:
                if e[parents[1]]:
                    return bn.prob_table.get(node)[4]
                else:
                    return bn.prob_table.get(node)[5]
            else:
                if e[parents[1]]:
                    return bn.prob_table.get(node)[6]
                else:
                    return bn.prob_table.get(node)[7]


def normalize(dist, poss):
    if poss:
        return dist[1] / (dist[0] + dist[1])
    return dist[0] / (dist[0] + dist[1])


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


def log_likelihood(bn):
    like = 0
    perm = ["".join(seq) for seq in itertools.product("01", repeat=5)]
    for i in range(len(perm)):
        like += enumerate_all(['A', 'B', 'C', 'D', 'E'], {'A': perm[i][0], 'B': perm[i][1], 'C': perm[i][2], 'D': perm[i][3], 'E': perm[i][4]}, bn)
    return np.log(like)


def main():
    # bn = Node({'H': [], 'W': [], 'E': ['H'], 'V': ['E', 'W']})
    # bn = Node({'H': [], 'W': [], 'E': ['H'], 'V': ['E', 'W']})
    bn = Node({"A": [], "B": ["D"], "C": ["A"], "D": ["B"], "E": ["C", "D"]})
    # bn = Node({"A": [], "B": [], "C": ["A", "B"], "D": ["C"], "E": ["C"]})
    # bn = Node({"A": [], "E": [], "B": ["A"], "C": ["A"], "D": ["B", "C"]})
    bn.prob_table = bn.build_network('data3.csv')
    # print(enumeration_ask('V', {'H': 1}, bn, 1))
    # print(enumerate_all(['H', 'W', 'E', 'V'], {'H': 1, 'W': 1, 'E': 1, 'V': 0}, bn))
    print(log_likelihood(bn))

if __name__ == '__main__':
    main()
