import os


# Header lines that apply to every row beneath them.
HEADERS = ('Competition',)

# Every field but the season and the sources is a dollar amount or a count.
TEXT = ('season', 'sources')


def process_rules(fn, root):
    """
    Read a league's roster rules: a Competition header, a Key line naming the
    fields, then one row per season. Amounts and counts are integers, an empty
    field is None, and the sources are split on whitespace. Field names keep
    their spaces as underscores: 'salary budget' is salary_budget.
    """
    path = os.path.join(root, fn)

    block = {'competition': None}
    key = None
    data = []

    for number, line in enumerate(open(path), start=1):
        line = line.strip()

        if not line or line.startswith('*'):
            continue

        if line.startswith('Key:'):
            key = [e.strip().replace(' ', '_') for e in line.split('Key:', 1)[1].split(';')]
            continue

        header = line.split(':', 1)[0]
        if header in HEADERS:
            block[header.lower()] = line.split(':', 1)[1].strip()
            continue

        fields = [e.strip() for e in line.split(';')]
        if key is None or len(fields) != len(key):
            raise ValueError("%s:%s: expected %s, got %r" % (path, number, key, line))

        d = {k: v or None for k, v in zip(key, fields)}
        for k in key:
            if k not in TEXT and d[k] is not None:
                d[k] = int(d[k])
        d['sources'] = (d.get('sources') or '').split()
        data.append({**d, **block})

    return data
