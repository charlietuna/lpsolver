#!/usr/bin/python
#
# Copyright (c) 2013 Charles Ying, All Rights Reserved.
#


def longest_sorted(a, b):
    if len(a) != len(b):
        return cmp(len(b), len(a))
    return cmp(a, b)


def boardhash(board):
    boardhash = {}
    for b in board:
        boardhash[b] = boardhash.get(b, 0) + 1
    return boardhash


def word_in_boardhash(bdhash, word):
    whash = {}
    for letter in word:
        whash[letter] = whash.get(letter, 0) + 1

    for key, value in whash.items():
        if key not in bdhash or bdhash[key] < value:
            return False
    return True


def hash_solver(board):
    dictionary = open("letterpress_alphabetical.txt").read().splitlines()
    bdhash = boardhash(board)
    valids = [ word for word in dictionary if word_in_boardhash(bdhash, word) ]
    return valids


def word_allmoves(bhash, subword):
    if len(subword) <= 1:
        return [ [move] for move in bhash[subword[0]] ]
    else:
        latermoves = word_allmoves(bhash, subword[1:])
        moves = []
        for move in bhash[subword[0]]:
            for latermove in latermoves:
                if move not in latermove:
                    completemove = [move] + latermove
                    moves.append(completemove)
        return moves


def gen_neighbors():
    nmap = {}
    for y in range(5):
        for x in range(5):
            neighbors = []
            if x > 0:
                neighbors += [(x - 1, y)]
            if x < 4:
                neighbors += [(x + 1, y)]
            if y > 0:
                neighbors += [(x, y - 1)]
            if y < 4:
                neighbors += [(x, y + 1)]

            ineighbors = [ point[0] + point[1] * 5 for point in neighbors ]
            nmap[x + y * 5] = tuple(ineighbors)
    return nmap

nmap = gen_neighbors()

# Neutral, my tile, my protected tile, opponent tile, opponent protected tile
blueteam = (0, 1, 2, 3, 4)
redteam = (0, 3, 4, 1, 2)


def isprotected(coloring, move, teamset):
    def isteam(a):
        return a == teamset[1] or a == teamset[2]

    if not isteam(coloring[move]):
        return False

    for neighbor in nmap[move]:
        if not isteam(coloring[neighbor]):
            return False
    return True


def new_colors(coloring, moves, teamset, otherteamset):
    nc = list(coloring)
    for move in moves:
        if nc[move] != teamset[4]:
            nc[move] = teamset[1]
    for i in range(len(nc)):
        if isprotected(nc, i, teamset):
            nc[i] = teamset[2]
        if (nc[i] == teamset[4]) and not isprotected(nc, i, otherteamset):
            nc[i] = teamset[3]
    return nc


def differ(coloring, newcoloring, teamset):
    diff = 0
    winning = True
    for c, nc in zip(coloring, newcoloring):
        if nc == 0:
            winning = False
        if nc == teamset[1] and c == 0:
            diff += 1
        if nc == teamset[1] and c == teamset[3]:
            diff += 2
        if nc == teamset[2] and c != teamset[2]:
            diff += 100
        if nc == teamset[3] and c == teamset[4]:
            diff += 100
    if winning:
        diff += 1000
    return diff


def scorer(bhash, word, coloring, myteam, theirteam):
    maxscore = -1
    maxmove = None
    maxcoloring = None
    for move in word_allmoves(bhash, word):
        newcoloring = new_colors(coloring, move, myteam, theirteam)
        newscore = differ(coloring, newcoloring, myteam)
        if newscore > maxscore:
            maxmove = move
            maxscore = newscore
            maxcoloring = newcoloring

    return maxscore, maxmove, maxcoloring


def prettymove(move):
    return [ (i % 5 + 1, i / 5 + 1) for i in move ]


def strcoloring(coloring):
    return "".join([ str(n) for n in coloring ])


if __name__ == "__main__":
    import sys
    board = sys.argv[1]
    coloring = sys.argv[2]

    coloring = [ int(c) for c in coloring ]

    valids = hash_solver(board)

    bhash = {}
    for b, i in zip(board, range(len(board))):
        bhash[b] = bhash.get(b, []) + [i]

    scores = {}
    moves = {}
    colorings = {}
    for valid in valids:
        scores[valid], moves[valid], colorings[valid] = scorer(bhash, valid, coloring, blueteam, redteam)

    highest_valids = sorted(valids, cmp=lambda x, y: cmp(scores[y], scores[x]))

    for valid in highest_valids[:10]:
        print valid, scores[valid], prettymove(moves[valid]), strcoloring(colorings[valid])

        nextscores = {}
        nextmoves = {}
        nextcolorings = {}

        nextvalids = [ v for v in valids if v != valid ]

        for nextvalid in nextvalids:
            nextscores[nextvalid], nextmoves[nextvalid], nextcolorings[nextvalid] = scorer(bhash, nextvalid, coloring, redteam, blueteam)

        highest_nextvalids = sorted(nextvalids, cmp=lambda x, y: cmp(nextscores[y], nextscores[x]))

        highvalid = highest_nextvalids[0]
        print "\t", highvalid, scores[highvalid], prettymove(moves[highvalid]), strcoloring(colorings[highvalid])





