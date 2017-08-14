

# Placeholder for transaction processing


# Should handle:
# 1. literal transactions (sign; Jermain Defoe; Toronto FC; Tottenham Hotspur)
# 2. drafts (7; Clint Dempsey; New England Revolution; Furman
# 3. job lists (Dave Dir; head coach; FC Dallas; 1996; 2001)
# 4. anything else?


# should use keys.

import datetime
import os



# This should probably be in utils.
def remove_pairs(text, start, end):
    """
    Removes pairs like (hello) or [whatever]
    """
    s = ""
    include = True
    for char in text:
        if char == start:
            include = False

        if include:
            s += char
        
        if char == end:
            include = True

    return s





class TransactionProcessor(object):
    

    def __init__(self, delimiter=';'):
        self.delimiter = delimiter
        self.header = None
        self.competition = None
        self.season = None
        self.source = None

        self.data = []
        self.previous_item = None


    def process_line(self, line):

        if not line or line.startswith('*'):
            return

        tag_data = lambda l, t: l.split(t, 1)[1].strip()

        line = line.strip()

        if line.startswith('Key:'):
            h = line.split('Key:')[1]
            self.header = [e.strip() for e in h.split(self.delimiter)]
            return

        if line.startswith('Competition:'):
            self.competition = line.split('Competition:')[1].strip()
            return

        if line.startswith('Season:'):
            self.season = line.split('Season:')[1].strip()
            return

        if line.startswith('BlockSource:'):
            self.source = line.split('BlockSource:')[1]
            return

        if line.startswith("Source:"):
            self.current_transaction['sources'].append(tag_data(line, "Source:"))
            return

        if line.startswith("Notes:"):
            self.current_transaction['notes'] = tag_data(line, "Notes:")
            return


        fields = line.split(self.delimiter)

        try:
            d = dict(zip(self.header, fields))
        except:
            import pdb; pdb.set_trace()

        if self.source:
            sources = [self.source]
        else:
            sources = []

        if 'date' in d and d['date'].strip():
            try:
                month, day, year = d['date'].split('/')
            except:
                import pdb; pdb.set_trace()
            dt = datetime.datetime(int(year), int(month), int(day))
        else:
            dt = None




        if d['type'].strip() != 'trade':

            if 'person' not in d:
                import pdb; pdb.set_trace()

            d2 = {
                'date': dt,
                'ttype': d['type'],
                'person': d['person'],
                'team_to': d.get('team_to'),
                'team_from': d.get('team_from'),
                'sources': sources,
            }

            self.current_transaction = d2
            self.data.append(d2)

        else:
            items = d['person'].split(',')

            try:
                teams = d['team_to'].split(',')
            except:
                import pdb; pdb.set_trace()

            if len(items) != len(teams):
                import pdb; pdb.set_trace()

            units = zip(items, teams)
            
            l = [{'date': dt, 'ttype': 'trade', 'person': p, 'team_to': t, 'sources': sources} for (p,t) in units]

            self.current_transaction = l[-1]
            self.data.extend(l)


def process_transactions(fn, root, delimiter=";"):
    sp = TransactionProcessor(delimiter)

    path = os.path.join(root, fn)
    lines = open(path).read().strip().split('\n')    

    for line in lines:
        sp.process_line(line)

    return [e for e in sp.data if e]

