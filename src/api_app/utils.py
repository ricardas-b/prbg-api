import numpy

from rest_framework.views import exception_handler



def levenshtein_distance(substring, string):
    ''' Levenshtein distance is a string metric for measuring the difference
        between two sequences. Levenshtein distance between two words is the
        minimum number of single-character edits (insertions, deletions or
        substitutions) required to change one word into the other '''

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

    return int(distances[len(substring)][len(string)])


# TODO: Consider other string similarity metrics, e.g. "Damerau–Levenshtein distance", etc.


def custom_exception_handler(exc, context):
    ''' Custom exception handler that overwrites payload of NotFound response
        of DRF '''
    
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {'message': 'Resource not found'}

    return response
