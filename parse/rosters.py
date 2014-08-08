#!/usr/local/bin/env python
# -*- coding: utf-8 -*-


import os
import re

from soccerdata.settings import ROOT_DIR


def filter_brackets(s):
    """
    Remove data inside brackets in a string.
    eg Doug Miller [Rochester Rhinos] (Josh Wolff [Project-40] 78) -> Doug Miller (Josh Wolff 78)
    """
    t = ''
    bracketed = False
    for char in s:
        if char == '[':
            if bracketed == False:
                bracketed = True
            else:
                import pdb; pdb.set_trace()

        if char == ']':
            if bracketed == True:
                bracketed = False
            else:
                import pdb; pdb.set_trace()

        if bracketed == False and char not in '[]':
            t += char


    if bracketed:
        import pdb; pdb.set_trace()

    return t


 
def fix_roster_name(name):

    char_dict = {
        'Á': 'á',
        'Ã': 'ã',
        'Ó': 'ó',
        'É': 'é',
        'Ñ': 'ñ',
        'Ú': 'ú',
        'Í': 'í',
        'Ô': 'ô',
        }
    

    # Title doesn't work with abnormal characters.
    # Maybe coerce to unicode first?
    #name = unicode(name, 'utf-8')
    name_parts = name.split(' ')

    l = []
    for part in name_parts:
        part = part.lower()
        s = ''
        
        first_letter = True
        for char in part:
            if first_letter and char != '"':
                char = char.capitalize()
                first_letter = False

            char = char_dict.get(char, char)
            s += char
        l.append(s)

    return ' '.join(l)

        


def process_rosters(fn, root='soccerdata/data/rosters'):

    l = []

    p = os.path.join(ROOT_DIR, root, fn)
    f = open(p)

    rp = RosterProcessor()
    for line in f:
        rp.process_line(line)

    return rp.rosters
            


class RosterProcessor(object):
    
    def __init__(self):
        self.competition = None
        self.season = None
        self.team = None

        self.rosters = []

    def process_line(self, line):
        line = line.strip()
        if not line:
            return

        if line.startswith('*'):
            return

        if line.startswith('NOTE'):
            return

        if line.startswith("Coach"):
            return

        # Set the competition.
        if line.startswith("Competition:"):
            self.competition = line.split("Competition:")[1].strip()
            return

        if line.startswith("Season:"):
            self.season = line.split("Season:")[1].strip()
            return

        if line.startswith("Team:"):
            self.team = line.split("Team:")[1].strip()
            return


        # 
        else:
            m = re.match("\d+(.*)", line)
            if m:
                s = m.groups()[0]
            else:
                s = line

            fields = s.split('  ')
            player = fields[0].strip()


            player = player.title()

            if player in  ('-', ''):
                return

            if '-' in player:
                player = player.split('-')[0].strip()

            player = fix_roster_name(player)

            self.rosters.append({
                    'competition': self.competition,
                    'season': self.season,
                    'team': self.team,
                    'name': player,
                    })




def process_rosters2(fn=None, path=None):

    if fn is None and path is None:
        raise

    if path is None:
        path = os.path.join(ROOT_DIR, 'soccerdata/data/rosters/', fn)

    f = open(path)

    rp = RosterProcessor2()
    for line in f:
        rp.process_line(line)

    return rp.rosters
            


class RosterProcessor2(object):
    
    def __init__(self):
        self.competition = None
        self.season = None

        self.rosters = []

    def process_line(self, line):
        line = line.strip()
        if not line:
            return

        if line.startswith('*'):
            return


        # Set the competition.
        if line.startswith("Competition:"):
            self.competition = line.split("Competition:")[1].strip()
            return

        if line.startswith("Season:"):
            self.season = line.split("Season:")[1].strip()
            return



        else:
            try:
                team, players = filter_brackets(line).split(':', 1)
            except:
                import pdb; pdb.set_trace()

            for player in players.split(','):
                self.rosters.append({
                        'competition': self.competition,
                        'season': self.season,
                        'team': team.strip(),
                        'name': player.strip(),
                        })









class RosterProcessor3(object):
    

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


    def process_line(self, line):

        if not line or line.startswith('*'):
            return

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



def process_rosters3(fn, root, format_name=False, source=None, delimiter=";"):
    print(fn)
    sp = RosterProcessor3(delimiter, format_name=format_name)
    path = os.path.join(root, fn)
    lines = open(path).read().strip().split('\n')    

    for line in lines:
        sp.process_line(line)

    return [e for e in sp.data if e]

