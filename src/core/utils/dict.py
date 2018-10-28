"""
    https://stackoverflow.com/questions/31033549/nested-dictionary-value-from-key-path
"""


def dict_finder(dictionary, element):
    keys = element.split('.')
    rv = dictionary
    for key in keys:
        rv = rv[key]
    return rv
