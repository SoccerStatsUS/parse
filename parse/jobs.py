import os
import re


ROLES = ('head', 'interim', 'assistant', 'gm')

# A date is as precise as its source: a day, a month or only a year.
DATE = re.compile(r'^\d{4}(-\d{2}(-\d{2})?)?$')


def process_jobs(fn, root):
    """
    Read a league's club jobs: a Competition header, a Key line naming the
    fields, then one row per person and stint in a job. start and end stay
    strings (YYYY-MM-DD, YYYY-MM or YYYY), an empty end is None (still in the
    job), and sources are split on whitespace.
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
        if d['role'] not in ROLES:
            raise ValueError("%s:%s: role %r is not one of %s" % (path, number, d['role'], ROLES))
        for k in ('start', 'end'):
            if d[k] is not None and not DATE.match(d[k]):
                raise ValueError("%s:%s: %s %r is not YYYY-MM-DD, YYYY-MM or YYYY" % (path, number, k, d[k]))
        d['title'] = d.get('title') or ''
        d['sources'] = (d.get('sources') or '').split()
        d['competition'] = competition
        data.append(d)

    return data
