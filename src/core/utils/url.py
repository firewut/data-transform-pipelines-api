"""
https://stackoverflow.com/questions/1793261/how-to-join-components-of-a-path-when-you-are-constructing-a-url-in-python
"""


def urljoin(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """

    url = "/".join(map(lambda x: str(x).rstrip('/'), args))
    if '/' in args[-1]:
        url += '/'
    if '/' not in args[0]:
        url = '/' + url

    url = url.replace('//', '/')

    return url
