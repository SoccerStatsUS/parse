import os


# Header lines that apply to every row beneath them.
HEADERS = ('Competition', 'Kind')

NUMBERS = ('start', 'end', 'annual', 'total')


def process_sponsorships(fn, root):
    """
    Read a sponsorship file: Competition and Kind headers, a Key line naming
    the fields, then one row per deal. Empty fields are None; years and
    amounts are integers; sources are split on whitespace.
    """
    path = os.path.join(root, fn)

    block = {'competition': None, 'kind': None}
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
        d['sources'] = (d.get('sources') or '').split()
        d['note'] = d.get('note') or ''
        data.append({**d, **block})

    return data
