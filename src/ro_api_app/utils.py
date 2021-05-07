import numpy


def levenshtein_distance(substring, string):
    rows = len(substring) + 1
    cols = len(string) + 1
    distances = numpy.zeros((rows, cols))

    for r in range(rows):
        distances[r][0] = r

    for c in range(cols):
        distances[0][c] = c

    for r in range(1, rows):
        for c in range(1, cols):
            if substring[r-1] == string[c - 1]:
                distances[r][c] = distances[r-1][c-1]
            else:
                distances[r][c] = min(distances[r-1][c-1], distances[r-1][c], distances[r][c-1]) + 1

    return distances[len(substring)][len(string)]
