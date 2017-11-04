import pandas as pd
import numpy as np
# False = 0


class Node:
    def __init__(self, board):
        self.prob_table = {}
        self.vars = list(board.keys())
        self.board = board
        self.variable_values = [0, 1]

    # builds the probability table the long way by having each node run through the table to get it's probability
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


# function to create a copy of the dictionary to pass
def up(e, date):
    copy = e.copy()
    copy.update(date)
    return copy


# grabs the requested probability by how the nodes are ordered in the tuple
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


# returns for the given value as true or not
def normalize(dist, poss):
    if poss:
        return dist[1] / (dist[0] + dist[1])
    return dist[0] / (dist[0] + dist[1])


def log_likelihood(bn, name):
    df = pd.read_csv(name)
    like = 0
    for i in range(len(df)):
        like += np.log(enumerate_all(['A', 'B', 'C', 'D', 'E'], {'A': df['A'][i], 'B': df['B'][i], 'C': df['C'][i], 'D': df['D'][i], 'E': df['E'][i]}, bn))
    return like


def parameters(bn):
    counts = 0
    for words in bn.prob_table:
        counts += len(bn.prob_table[words])
    return counts


def main():
    # bn = Node({'H': [], 'W': [], 'E': ['H'], 'V': ['E', 'W']})
    # bn = Node({'B': [], 'F': [], 'G': ['B', 'F'], 'S': ['B', 'F']})
    # bn = Node({"A": [], "B": [], "C": ["A"], "D": ["B"], "E": ["C", "D"]})
    # bn = Node({"A": [], "B": [], "C": ["A", "B"], "D": ["C"], "E": ["C"]})
    bn = Node({"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"], "E": []})
    bn.prob_table = bn.build_network('data3.csv')
    print(parameters(bn))
    # print(enumeration_ask('V', {'H': 1}, bn, 1))
    # print(enumerate_all(['H', 'W', 'E', 'V'], {'H': 1, 'W': 1, 'E': 1, 'V': 0}, bn))
    # print(log_likelihood(bn, 'data3.csv'))

if __name__ == '__main__':
    main()
