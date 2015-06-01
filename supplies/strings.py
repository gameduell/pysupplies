import re

__author__ = 'wabu'
__all__ = ['splitcamel, uncamel, nameof, abbrev']


def uncamel(phrase, sep='-'):
    """
    converts camelcase phrase into seperated lower-case phrase

    Parameters
    ---
    phrase : str
        phrase to convert

    Examples
    ---
    >>> uncamel('HTTPRequestHeader')
        'http-request-header'
    >>> uncamel('StatusCode404', sep=' ')
        'status code 404'
    """
    return re.sub(r'((?<=[a-z])[A-Z0-9]|(?!^)[A-Z0-9](?=[a-z]))',
                  sep + r'\1', phrase).lower()


def splitcamel(phrase):
    return uncamel(phrase).split('-')


def nameof(obj, sep='-'):
    name = None
    if isinstance(obj, str):
        name = uncamel(obj)
    elif hasattr(obj, 'name'):
        return obj.name
    else:
        cls = obj if isinstance(obj, type) else type(obj)
        name = cls.__name__

    return re.sub(r' +', sep,  uncamel(name))


def abbrev(obj, n=None):
    name = re.sub(r'\W', '', nameof(obj))
    cons = re.findall('[bcdfghjklmnpqrstvwxyzBCDFGHIJKLMNPQRSTVWXYZ]', name)
    return ''.join(cons[:n])
