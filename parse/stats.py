#!/usr/local/bin/env python
# -*- coding: utf-8 -*-

import os
    
def process_name(s):

    if ',' not in s:
        return s

    mapping = {
        'Da Silva-Sarafim, Jr, Edivaldo': 'Da Silva-Sarafim Jr, Edivaldo',
        'Novas, Lomonaca, Ignacio': 'Novas, Ignacio',
        'Kato, Hajime,': 'Kato, Hajime',
        'Kolba, JR., Thoms': 'Kolba Jr., Thomas',
        'Fragoso-Gonzalez, Jr, Pedro': 'Fragoso-Gonzalez Jr, Pedro',
        }

    if s in mapping:
            s = mapping[s]

    #import pdb; pdb.set_trace()

    try:
        last, first = [e.strip() for e in s.split(',', 1)] # Assume no 2-comma names.    

    except:
        import pdb; pdb.set_trace()
    name = first + ' ' + last

    # What is this?
    if '*' in name:
        import pdb; pdb.set_trace()
    name = name.replace("*", "")

    # Clean and remove titles
    name = name.strip().title()

    return name


class StatsProcessor(object):
    

    def __init__(self, delimiter=';', format_name=False):
        self.delimiter = delimiter
        self.header = None
        self.competition = None
        self.season = None
        self.source = None
        self.team = None

        self.format_name = format_name

        self.data = []

        self.transforms = set()



    def preprocess_line(self, line):
        # Should probably just process these text files.
        line = line.replace('\xa0', '')
        line = line.replace('\xc2', '')
        
        # Remove *'s from nasl stats.
        line = line.replace("*", "")
        line = line.strip()
        return line



    def process_line(self, line):

        if not line or line.startswith('*'):
            return

        line = self.preprocess_line(line)

        if line.startswith('Key:'):
            h = line.split('Key:')[1]
            self.header = [e.strip() for e in h.split(self.delimiter)]
            return

        if line.startswith('Team:'):
            self.team = line.split('Team:')[1]
            return


        if line.startswith('Competition:'):
            self.competition = line.split('Competition:')[1].strip()
            return

        if line.startswith('Season:'):
            self.season = line.split('Season:')[1].strip()
            return

        if line.startswith('Transform:'):
            t = line.split('Transform:')[1].strip()
            self.transforms.add(t)
            return


        if line.startswith('BlockSource:'):
            self.source = line.split('BlockSource:')[1]
            return

        fields = line.split(self.delimiter)

        try:
            d = dict(zip(self.header, fields))
        except:
            import pdb; pdb.set_trace()

        #d = stat_fixes(d)


        if 'name' not in d:
            import pdb; pdb.set_trace()
            print ("missing name")
            return {}

        if not d['name']:
            import pdb; pdb.set_trace()
            print ("missing name")
            return {}

        if self.format_name:
            d['name'] = process_name(d['name'])

        if 'name-title' in self.transforms:
            d['name'] = d['name'].title()

        if not d.get('team'):
            d['team'] = self.team

        #if competition is not None:

        d['source'] = self.source

        if self.competition and not d.get('competition'):
            d['competition'] = self.competition

        if self.season and not d.get('season'):
            d['season'] = self.season

        if 'year' in d:
            d['season'] = d.pop('year').strip()

        if 'games' in d:
            d['games_played'] = d.pop('games')


        for k in 'games_played', 'games_started', 'minutes', 'goals', 'assists', 'shots', 'shots_on_goal', \
                'blocks', 'fouls_committed', 'fouls_suffered', 'offsides', 'pk_goals', 'pk_attempts', 'pks_drawn', \
                'pks_committed':


            if k in d:
                v = d[k]
                v = v.strip()

                if v in ('', '-'):
                    v = 0
                elif v == '?':
                    v = None
                else:
                    try:
                        v = int(v)
                    except ValueError:
                        import pdb; pdb.set_trace()
                        print(v)

                d[k] = v

        d['position'] = d['points'] = ''

        self.data.append(d)



def process_stats(fn, root, format_name=False, source=None, delimiter=";"):
    print(fn)
    sp = StatsProcessor(delimiter, format_name=format_name)
    path = os.path.join(root, fn)
    lines = open(path).read().strip().split('\n')    



    for line in lines:
        sp.process_line(line)

    return [e for e in sp.data if e]

