# Process standings files. 

# Excel style:
# Houston Stars	North American Soccer League	1968	Gulf Division	32	14	6	12	150	58	41			

# Wikipedia Style
# 3       Moctezuma       18      9       3       6       43      34      21


import codecs
import os


def int_or_none(e):
    """Coerce an item to an int, or return None."""
    # Could handle some stuff, like ' ', better.
    # Not sure whether to be more careful or more aggressive.
    if e:
        return int(e)

    return None


def process_excel_standings(p):
    """
    Load an old-style excel standings file.
    """
    # phasing this out in favor of significantly more 
    # flexible standings files.

    f = open(p)
    lines = f.read().split('\n')

    def process_line(line):
        line = line.strip()
        if not line:
            return {}

        fields = line.split("\t")

        goals_for = goals_against = None
        shootout_wins = shootout_losses = None

        if len(fields) < 8:
            import pdb; pdb.set_trace()
            print(fields)
            return {}

        if len(fields) == 8:
            team, competition, season, division, games, wins, ties, losses = fields
            points = None

        elif len(fields) == 9:
            team, competition, season, division, games, wins, ties, losses, points = fields

        else:
            team, competition, season, division, games, wins, ties, losses, points, goals_for, goals_against = fields[:11]

        # No data for these yet.
        if (competition, season) == ('National Premier Soccer League', '2008'):
            return {}

        if len(fields) == 12:
            shootout_wins = fields[11]
        if len(fields) == 13:
            shootout_wins, shootout_losses = fields[11:]
        
        try:
            games = int(games)
        except:
            import pdb; pdb.set_trace()

        return {
            'team': team,
            'competition': competition,
            'division': division,
            'season': season,
            'games': games,
            'wins': int(wins),
            'ties': int_or_none(ties),
            'losses': int(losses),
            'points': int_or_none(points),
            'goals_for': int_or_none(goals_for),
            'goals_against': int_or_none(goals_against),
            'shootout_wins': int_or_none(shootout_wins),
            'shootout_losses': int_or_none(shootout_losses),
            'final': True
            }
        
    l = [process_line(line) for line in lines]
    return [e for e in l if e]




def process_string(s, delimiter):
    """
    Process standings data received as a string.
    For testing.
    """
    lines = s.split('\n')
    return process_lines(lines, delimiter)

def process_standings_file(p, delimiter=';'):
    """
    Process standings data received as a file-like object.
    """
    with f as codecs.open(p, 'r', 'utf-8'):
        return process_lines(f, delimiter)


def process_lines(lines, delimiter):
    """
    Parse standings lines.
    """
    sp = StandingProcessor(delimiter)
    for line in lines:
        sp.process_line(line)
    return sp.standings


class StandingProcessor(object):
    """
    An object to feed lines of text to.
    Retains some simple state data.
    """

    def __init__(self, delimiter):
        self.delimiter = delimiter
        self.competition = None
        self.season = None
        self.group = ''
        self.key = None

        self.sources = []

        self.standings = []


    def process_line(self, line):
        """
        Figure out what kind of line we're dealing with
        and process it.
        """
        
        line = line.strip()
        if not line:
            return

        tag_data = lambda l, t: l.split(t, 1)[1].strip()

        
        if line.startswith("*"):
            return # is a comment.


        # Global data.

        if line.startswith('BlockSource:'):
            source = tag_data(line, "BlockSource:")
            if source:
                self.sources = [source]
            return

        if line.startswith("Competition:"):
            self.competition = tag_data(line, 'Competition:')
            self.group = ''
            return

        if line.startswith("Key"):
            # Consider aliasing some key data.
            # e.g. games -> games_played, draws -> ties
            self.key = [e.strip() for e in tag_data(line, 'Key:').split(self.delimiter)]
            return

        if line.startswith("Season:"):
            self.season = tag_data(line, 'Season:')
            self.group = ''
            return

        # Set the round.
        if line.startswith("Group"):
            self.group = tag_data(line, 'Group:')
            return

        # Should probably bring these back.
        if line.startswith("Round:"):
            #self.season = line.split("Season:")[1].strip()
            #self.group = ''
            return

        if line.startswith("Region:"):
            #self.season = line.split("Season:")[1].strip()
            #self.group = ''
            return


        # Not a known tag. 
        # We must be dealing with an actual standing.
        if line.strip():
            self.process_standings(line)


    def process_standings(self, line):
        """
        Process a line of standings.
        Just map a standings key to the parsed fields.
        """

        fields = line.split(self.delimiter)
        fields = [e.strip() for e in fields if e.strip()] # Should we really be removing empty fields like this?

        if self.key is None or len(self.key) != len(fields):
            # Pause if the key won't work.
            import pdb; pdb.set_trace() 

        d = dict(zip(self.key, fields))
        d.update({
                'competition': self.competition,
                'season': self.season,
                'group': self.group,
                'final': True,
                })

        for k in 'games', 'wins', 'ties', 'losses', 'points', 'goals_for', 'goals_against', 'shootout_wins', 'shootout_losses':
            if k in d:
                d[k] = int_or_none(d[k])

        self.standings.append(d)
