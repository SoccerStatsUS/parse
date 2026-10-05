import os


NUMBERS = ('year', 'start', 'end', 'awarded', 'first season', 'price', 'valuation', 'fee', 'net worth')


def process_ownership(fn, root):
    """
    Read an ownership file (operators, sales, expansion fees or net worths): a Competition
    header, a Key line naming the fields, then one row per record. Years and
    amounts are integers, an empty field is None, the note is a string and the
    sources are split on whitespace. Keys with spaces become underscores.
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
        d['sources'] = (d.get('sources') or '').split()
        d['competition'] = competition
        data.append({k.replace(' ', '_'): v for k, v in d.items()})

    return data
