import os


NUMBERS = ('opened', 'cost', 'public')


def process_stadiums(fn, root):
    """
    Read a stadium file: a Competition header, a Key line naming the fields,
    then one row per stadium built or rebuilt. Years and amounts are integers,
    an empty field is None (an empty note is ''), and sources are split on
    whitespace.
    """
    path = os.path.join(root, fn)

    competition = None
    key = None
    data = []

    for number, line in enumerate(open(path), start=1):
        line = line.strip()

        if not line or line.startswith('*'):
            continue

        if line.startswith('Key:'):
            key = [e.strip() for e in line.split('Key:', 1)[1].split(';')]
            continue

        if line.startswith('Competition:'):
            competition = line.split(':', 1)[1].strip()
            continue

        fields = [e.strip() for e in line.split(';')]
        if key is None or len(fields) != len(key):
            raise ValueError("%s:%s: expected %s, got %r" % (path, number, key, line))

        d = {k: v or None for k, v in zip(key, fields)}
        for k in NUMBERS:
            if d.get(k) is not None:
                d[k] = int(d[k])
        d['note'] = d.get('note') or ''
        d['currency'] = d.get('currency') or 'USD'
        d['sources'] = (d.get('sources') or '').split()
        d['competition'] = competition
        data.append(d)

    return data
