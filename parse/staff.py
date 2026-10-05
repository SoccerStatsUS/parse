import os


# Header lines that apply to every row beneath them.
HEADERS = ('Organization', 'Coverage')

NUMBERS = ('year', 'pay', 'related', 'other')


def process_staff(fn, root):
    """
    Read an organization's staff pay: Organization and Coverage headers (full
    for a public filing that lists everyone it must, reported for single press
    reports), a Key line, then one row per person and year. Amounts are
    integers, an empty field is None, and sources are split on whitespace.
    """
    path = os.path.join(root, fn)

    block = {'organization': None, 'coverage': 'full'}
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
        d['role'] = d.get('role') or ''
        d['sources'] = (d.get('sources') or '').split()
        data.append({**d, **block})

    return data
