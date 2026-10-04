import os


# Header lines that apply to every row beneath them.
HEADERS = ('Competition', 'Season', 'Source', 'Period')


def process_salaries(fn, root):
    """
    Read a salary file: Competition, Season, Source and Period headers,
    a Key line naming the fields, then one row per player.

    Amounts stay strings so nothing passes through a float.
    """
    path = os.path.join(root, fn)

    block = {'competition': None, 'season': None, 'source': None, 'period': 'year'}
    key = None
    data = []

    for number, line in enumerate(open(path), start=1):
        line = line.strip()

        if not line or line.startswith('*'):
            continue

        if line.startswith('Key:'):
            key = [e.strip() for e in line.split('Key:', 1)[1].split(';')]
            continue

        header = line.split(':', 1)[0]
        if header in HEADERS:
            block[header.lower()] = line.split(':', 1)[1].strip()
            continue

        fields = [e.strip() for e in line.split(';')]
        if key is None or len(fields) != len(key):
            raise ValueError("%s:%s: expected %s, got %r" % (path, number, key, line))

        d = dict(zip(key, fields))
        data.append({
            'name': d['name'],
            'team': d.get('team') or None,
            'position': d.get('position', ''),
            'base': d['base'],
            'guaranteed': d.get('guaranteed') or None,
            **block,
        })

    return data
