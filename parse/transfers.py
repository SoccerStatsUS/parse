import os


# Header lines that apply to every row beneath them.
HEADERS = ('Competition', 'Season')

NUMBERS = ('fee', 'ceiling')


def process_transfers(fn, root):
    """
    Read a season's transfers: Competition and Season headers, a Key line
    naming the fields, then one row per deal. Fees are integers, an empty field
    is None (an empty note or club is ''), and sources are split on whitespace.
    """
    path = os.path.join(root, fn)

    block = {'competition': None, 'season': None}
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

        d = {k: v or None for k, v in zip(key, fields)}
        for k in NUMBERS:
            if d.get(k) is not None:
                d[k] = int(d[k])
        if d['direction'] not in ('in', 'out', 'within'):
            raise ValueError("%s:%s: unknown direction %r" % (path, number, d['direction']))
        data.append({
            'name': d['player'],
            'from': d['from'] or '',
            'to': d['to'] or '',
            'direction': d['direction'],
            'fee': d['fee'],
            'ceiling': d['ceiling'],
            'currency': d['currency'] or 'USD',
            'kind': d['kind'],
            'reported': d['reported'],
            'sources': (d.get('sources') or '').split(),
            **block,
        })

    return data
