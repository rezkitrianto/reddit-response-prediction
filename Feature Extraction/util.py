import unicodedata


def convert(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
