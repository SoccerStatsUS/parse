import os


# Header lines that apply to every row beneath them.
HEADERS = {
    'Competition': 'competition',
    'Publisher': 'publisher',
    'Season': 'season',
    'Published': 'published',
    'Revenue season': 'revenue_season',
    'Source': 'sources',
}

NUMBERS = ('rank', 'value', 'revenue', 'operating income')


def process_valuations(fn, root):
    """
    Read a valuation list: headers naming the publisher and season, a Key line
    naming the fields, then one row per team. Amounts are integers, an empty
    field is None, and the sources are split on whitespace.
    """
    path = os.path.join(root, fn)

    block = dict.fromkeys(HEADERS.values())
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
            block[HEADERS[header]] = line.split(':', 1)[1].strip()
            continue

        fields = [e.strip() for e in line.split(';')]
        if key is None or len(fields) != len(key):
            raise ValueError("%s:%s: expected %s, got %r" % (path, number, key, line))

        d = {k: v or None for k, v in zip(key, fields)}
        for k in NUMBERS:
            if d.get(k) is not None:
                d[k] = int(d[k])
        data.append({
            'team': d['team'],
            'rank': d['rank'],
            'value': d['value'],
            'revenue': d.get('revenue'),
            'operating_income': d.get('operating income'),
            **block,
            'sources': (block['sources'] or '').split(),
        })

    return data
