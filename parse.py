# For processing general format score/lineup data.

# These look something like
# 3/29/2008; FC Dallas; 3-1 (aet); Chivas Guadalajara; Laredo, TX; Alex Prus; 130000
# Ruben Luna 3, Ruben Luna 10, Hugo Sanchez 92; Chicharito 19
# FC Dallas: Matt Jordan, Chris Gbandi, Clarence Goodson, George John, Zach Loyd, Brek Shea, Oscar Pareja, Leonel Alvarez, Ronnie O'Brien, Jason Kreis, Carlos Ruiz

import datetime
import os
import re

#from utils import get_id


def process_string(s):
    lines = s.split('\n')
    return process_lines(lines)


def process_lines(lines):
    gp = GeneralProcessor()
    for line in lines:
        gp.process_line(line)

    return (gp.games, gp.goals, gp.misconduct, gp.appearances, gp.rosters)
        

def process_games_file(p):

    return process_file(p)

def process_file(p):
    f = open(p)
    return process_lines(f)


def process_name(s):
    """Clean up a player name. Remove possible leading numbers.
    e.g. '18-Tim Howard ' -> 'Tim Howard'"""
    s = s.strip()
    m = re.match("(\d+-)?(.*)", s)
    if m:
        return m.groups()[1].strip()
    else:
        return s


# This and filter_brackets seem quite similar.
def split_outside_parens(s, delimiters=','):
    """
    Eddie Pope, Josh Wolff (Clint Mathis 30, Landon Donovan 60) -> 
    ['Eddie Pope', 'Josh Wolff (Clint Mathis 30, Landon Donovan 60)']
    """
    in_paren = False
    l = []
    ns = ''

    for char in s:
        if char == '(':
            in_paren = True
        if char == ')':
            in_paren = False

        if char in delimiters and not in_paren:
            l.append(ns)
            ns = ''
        else:
            ns += char

    l.append(ns)
    return l


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


class GeneralProcessor(object):
    """
    A game processing class.
    Processes content as a set of lines.
    """

    DATE_RE = re.compile("(\d+)/([\d\?]+)/(\d+)")
    DATE_TIME_RE = re.compile("(\d+)/(\d+)/(\d+) (\d+)z")
    FLAGS = ["Minigame", "Forfeit", "Annulled", "Replay"] # Indoor

    def __init__(self):
        self.competition = None
        self.season = None
        self.round = ''
        self.group = ''
        self.sources = []

        self.current_game = None
        self.century = None # Manage dates like 3/23/10

        self.home_first = False

        self.date = None
        self.date_style = 'month first'

        # Data containers
        self.games = []
        self.goals = []
        self.misconduct = []
        self.appearances = []
        self.rosters = []

        self.transforms = set()


    def process_line(self, line):
        """
        Do a lot of processing.
        """
        
        line = line.strip()
        if not line:
            return


        tag_data = lambda l, t: l.split(t, 1)[1].strip()

        def process_simple_tag(line, tag, key):
            if line.startswith(tag):
                key = tag_data(line, tag)


        # Represents a comment.
        if line.startswith("*"):
            return

        if line.startswith('Transform:'):
            t = line.split('Transform:')[1].strip()
            self.transforms.add(t)
            return

        if line.startswith('Indoor'):
            return



        # Handle flag data like Forfeit, Minigame.
        for e in self.FLAGS:
            if line.startswith(e):
                self.current_game[e.lower()] = True
                return

        if line.startswith("Notes:"):
            self.current_game['notes'] = tag_data(line, "Notes:")
            return

        if line.strip() == 'home-first':
            self.home_first = True
            return

        if line.startswith("Date:"):
            d = line.split('Date:')[1].strip()
            if d and d.lower() != 'none':
                try:
                    month, day, year = [int(e) for e in d.split('/')]
                    self.date = datetime.datetime(year, month, day)
                except:
                    import pdb; pdb.set_trace()

            else:
                self.date = None

            return

        if line.startswith("Date-style"):
            self.date_style = tag_data(line, "Date-style:")
            return


        # Change the number of minutes.
        if line.startswith("Minutes:"):
            self.current_game['minutes'] = int(tag_data(line, 'Minutes:'))
            return

        # Set the competition.
        if line.startswith("Competition:"):
            self.competition = tag_data(line, "Competition:")
            self.round = self.group = self.zone = ''
            return

        if line.startswith("Season:"):
            self.season = tag_data(line, "Season:")
            self.round = self.group = self.zone = ''
            return

        # Set the round.
        if line.startswith("Round:"):
            self.round = tag_data(line, "Round:")
            if self.round.lower() == 'none':
                self.round = ''
                self.group = ''
            return

        if line.startswith("Group:"):
            self.group = tag_data(line, "Group:")
            if self.group.lower() == 'none':
                self.group = None
            return

        if line.startswith("Penalty kicks:"):
            # starting to implement
            data = tag_data(line, "Penalty kicks:")
            try:
                t1_pks, t2_pks = [int(e) for e in data.split('-')]
            except ValueError:
                try:
                    t1_kickers, t2_kickers = [e.split(',') for e in data.split(';')]
                except ValueError:
                    import pdb; pdb.set_trace()

            return



        # Zone should be group?
        if line.startswith("Zone:"):
            self.group = tag_data(line, "Zone:")
            if self.group.lower() == 'none':
                self.group = None
            return

        # Set the round.
        if line.startswith("Roster:"):
            self.process_roster(tag_data(line, "Roster:"))
            return

        if line.lower().startswith("substitutes not used:"):
            return

        if line.startswith('Subs:'):
            return

        if line.startswith("Source:"):
            self.current_game['sources'].append(tag_data(line, "Source:"))
            return

        if line.startswith("Video:"):
            self.current_game['video'] = tag_data(line, "Video:")
            return

        # Should probably be able to unset BlockSource with a blank?
        if line.startswith('BlockSource:'):
            source = tag_data(line, "BlockSource:")
            if source:
                self.sources = [source]
            return

        if line.startswith("Century"):
            self.century = int(tag_data(line, "Century:"))
            return

        if line.startswith("Cards:"):
            return

        if line.startswith("Red Card:"):
            s = tag_data(line, "Red Card:")
            self.misconduct.extend(self.process_misconduct(s))
            return 

        if line.startswith("Red Cards:"):
            s = tag_data(line, "Red Cards:")
            self.misconduct.extend(self.process_misconduct(s))
            return 


        if line.startswith("Yellow Cards:"):
            s = tag_data(line, "Yellow Cards:")
            self.misconduct.extend(self.process_misconduct(s))
            return 


        if line.startswith("Shootout Win"):
            self.current_game['shootout_winner'] = tag_data(line, "Shootout Win:")
            return


        fields = line.split(";")


        # This section should be completely unnecessary now with colon-delimiters removed.

        # Checking for Brooklyn FC: GK, DF
        # Trying to handle 1/25/1990; Brooklyn FC; 2 : 1; Queens Boys
        # and not have it mistaken for a team line because of the colon?
        # Seems unnecessary.
        skip_team = False
        if ';' in line and ':' in line:
            if line.index(';') < line.index(':'):
                skip_team = True

        if ":" in line and not skip_team:
            possible_team = line.split(":")[0]
            if self.current_game == None:
                import pdb; pdb.set_trace()
                
            if possible_team in (self.current_game['team1'], self.current_game['team2']):
                lineups = self.process_lineup(line)
                self.appearances.extend(lineups)
                return 

        # Why is this check necessary?
        if fields:

            # Game without a date.
            # Need to implement this.
            # Whoops - this kills a lot of valid game results. [why?]
            if line.startswith(";") and line.count(';') > 1:
                return self.process_game_fields(fields)

            # Need to implement datetime check here.
            time_string = fields[0].strip()
            mdt = self.DATE_RE.match(time_string)
            if mdt:
                return self.process_game_fields(fields)

            md = self.DATE_RE.match(time_string)
            if md:
                return self.process_game_fields(fields)
            try:
                year = int(time_string)
                return self.process_game_fields(fields)
            except ValueError:
                pass


            if fields[0].startswith('?'):
                return self.process_game_fields(fields)

        # If nothing else matches, we must have a goal list.
        # (This fallback behavior means errors tend to accumulate
        # inside goal objects.
        # eg given FC Dallas; Kevin Hartman, Jackson... we get a long list of goals.
        # [Overreported goals should be treated with more suspicion than underreported goals.
        try:
            team1_goals, team2_goals = line.split(";")
        except ValueError:
            print(line)
            import pdb; pdb.set_trace()
            raise

        self.process_goals(team1_goals, team2_goals)

        
    def process_misconduct(self, line):

        def process_item(team, s):
            m = re.match('(.*?)(\d+)', s)
            if m:
                name = m.groups()[0].strip()
                minute = int(m.groups()[1])
            else:
                name, minute = s.strip(), None

            return {
                'gid': self.current_game['gid'],
                'competition': self.competition,
                'date': self.current_game['date'],
                'season': self.season,
                'name': name,
                'minute': minute,
                'type': 'red',
                'team': team,
                }
            

        process_side = lambda t, l: [process_item(t, e) for e in l.split(',') if e.strip()]

        if ';' in line:
            t1m, t2m = line.split(';')
            t1, t2 = self.current_game['team1'], self.current_game['team2']
            l = process_side(t1, t1m)
            l.extend(process_side(t2, t2m))

        else:
            l = process_side(None, line)

        return l
        

    def process_roster(self, line):

        def process_players(s):
            l = []
            fields = s.split(',')
            for f in fields:
                player = f.split('(')[0]
                l.append({
                        'competition': self.competition,
                        'season': self.season,
                        'team': team,
                        'name': player,
                        })

            return l
            

        line = line.strip()
        if line.endswith('.'):
            line = line[:-1]

        fields = line.split(";")
        if len(fields) == 2:
            start = end = None
            team, players = fields

        elif len(fields) == 4:
            team, start, end, players = fields

        else:
            import pdb; pdb.set_trace()

        self.rosters.append(process_players(players))


    def process_game_fields(self, fields):
        # Game fields are of this form:
        # 1. Date
        # 2. Team1, score
        # 3. Team2, score

        team1_result = team2_result = None

        # Get the date and time.
        time_string = fields[0].strip()

        # Assume start time not included.
        start = None


        if fields[0].strip() == '':
            # This should usually just be None. Make sure to not accidentally set dates.
            d = self.date
            

        elif '?' in fields[0]:
            try:
                _, _, year = fields[0].split('/')
                day = month = None
                d = None
            except ValueError:
                print("? problem on date", fields[0])
                d = None

        else:
            # Try datetime first, if it doesn't work, try time.
            m = self.DATE_TIME_RE.match(time_string)
            if m:
                if self.date_style == 'day first':
                    day, month, year, start = m.groups()
                else: 
                    month, day, year, start = m.groups()
            else:
                try:
                    # Where is this?
                    if self.date_style == 'day first':
                        day, month, year = self.DATE_RE.match(time_string).groups()
                    else:
                        month, day, year = self.DATE_RE.match(time_string).groups()
                except:
                    year = int(time_string)
                    month = day = 1

            year = int(year)
            if year < 1800:
                import pdb; pdb.set_trace()
                year += self.century
            d = datetime.datetime(year, int(month), int(day))



        try:
            team1, score, team2 = fields[1:4]
        except:
            import pdb; pdb.set_trace()

        score = score.lower().strip()
        minutes = 90

        if '(aet)' in score:
            score = score.replace('(aet)', '')
            minutes = 120

        if '(asdet)' in score:
            score = score.replace('(asdet)', '')
            minutes = 'asdet'

        # Replace w/o with more explicit data.
        # (Still not sure exactly what it's supposed to mean)
        result_unknown = not_played = False

        if score == 'w/o':
            print("skipping: %s" % score)
            return

        # Parse score data.
        elif score == '?':
            team1_score = team2_score = None
            result_unknown = True

        elif score == 'v': 
            team1_score = team2_score = None

        elif score in ('n/p', 'np'):
            team1_score = team2_score = None
            not_played = True

        else:
            try:
                team1_score, team2_score = [e.strip() for e in score.split('-')]
            except:
                import pdb; pdb.set_trace()

            if team1_score in 'wlt':
                team1_result = team1_score
                team1_score = None
            else:
                try:
                    team1_score = int(team1_score)
                except:
                    import pdb; pdb.set_trace()


            if team2_score in 'wlt':
                team2_result = team2_score
                team2_score = None
            else:
                try:
                    team2_score = int(team2_score)
                except:
                    import pdb; pdb.set_trace()


        # Process ref, assistant refs, attendance, location.
        remaining = fields[4:]


        # Attendance is always the last item.
        if remaining:
            try:
                attendance = int(remaining[-1])
                remaining = remaining[:-1]
            except ValueError:
                attendance = None
        else:
            attendance = None


        location = ''
        referee = None

        if len(remaining) == 1:
            location = remaining[0].strip()

        elif len(remaining) == 2:
            location, referee = [e.strip() for e in remaining]

        linesmen = []
        if referee and ',' in referee:
            people = referee.split(',')
            referee = people[0].strip()
            linesmen = [e.strip() for e in people[1:]]

        if self.competition is None or self.season is None:
            import pdb; pdb.set_trace()

        
        # Home team management.
        # Should do this in normalization...
        team1 = team1.strip()
        team2 = team2.strip()
        location = location.strip()

        home_team, neutral = None, False

        if self.home_first and not location:
            home_team = team1

        if location in (team1, team2):
            home_team = location
        elif location.lower() == 'home':
            home_team = team1
        elif location.lower() == 'away':
            home_team = team2
        elif location.lower() == 'neutral':
            neutral = True

        g = {
            #'gid': get_id(),
            'competition': self.competition,
            'season': self.season,
            'round': self.round,
            'group': self.group,

            'date': d,

            'team1': team1,
            'team2': team2,
            'team1_score': team1_score,
            'team2_score': team2_score,
            'team1_result': team1_result,
            'team2_result': team2_result,
            'result_unknown': result_unknown,
            'not_played': not_played,

            'home_team': home_team,
            'shootout_winner': None,

            'location': location,
            'neutral': neutral,

            'referee': referee,
            'linesmen': linesmen,
            'attendance': attendance,
            'minigame': False,
            'forfeit': False,
            'sources': self.sources[:],
            'notes': '',
            'video': '',
            'minutes': minutes,

            }

        self.current_game = g
        self.games.append(g)


    def process_lineup(self, line):

        def process_appearance(s, team, order):
            s = filter_brackets(s)

            capts = ['(c)', '(capt)', '(capt.)', '(Capt.)', '(Capt)', '(cap)']
            for e in capts:
                s = s.replace(e, '')

            #s = s.replace('(c)', '').replace('(capt)', '').replace('(capt.)', '').replace('(capt.)', '')
            # Off should be "end", then normalized later.

            # Will implement captains later.
            s = s.replace('(c)', '')

            # Fuck. This is wrong. This is true of game plus/minus, but not appearance plus/minus.
            # Need to handle appearance minutes...
            # This is being used for determining the results of games.
            if team == self.current_game['team1']:
                goals_for, goals_against = self.current_game['team1_score'], self.current_game['team2_score']
            elif team == self.current_game['team2']:
                goals_for, goals_against = self.current_game['team2_score'], self.current_game['team1_score']
            else:
                import pdb; pdb.set_trace()


            base = {
                'gid': self.current_game['gid'],
                'team': team,
                'competition': self.competition,
                'date': self.current_game['date'],
                'season': self.season,
                'goals_for': goals_for,
                'goals_against': goals_against,
                'order': order,
                }


            # It should be possible to merge these into one.
            # It might even be possible to just remove the first half of the if clause.
            if '(' not in s:
                name = process_name(s)

                e = {
                    'name': name,
                    'on': 0,
                    'off': 90,
                    }
                e.update(base)
                return [e]

            else:
                try:
                    starter, subs = s.split("(")
                except:
                    import pdb; pdb.set_trace()
                subs = subs.replace(")", "")
                sub_items = subs.split(",")

                starter = process_name(starter)                

                l = [{ 'name': starter, 'on': 0 }]
                    
                for item in sub_items:
                    m = re.match("(.*)( \d+)", item)
                    if m:
                        sub, minute = m.groups()
                        minute = int(minute)
                        sub = process_name(sub)
                    else:
                        #print("No minute for sub %s" % s)
                        minute = None
                        sub = process_name(sub_items[0])

                    l[-1]['off'] = minute
                    l.append({'name': sub, 'on': minute})

                l[-1]['off'] = 90
                for e in l:
                    e.update(base)

                return l

        # Remove trailing marks.
        line = line.strip()
        if line[-1] in ('.', ','):
            line = line[:-1]

        team, players = line.split(":", 1)
        lineups = []

        # Need to separate separate fields to get spearate sections.
        for order, e in enumerate(split_outside_parens(players, ',;'), start=1):
            lineups.extend(process_appearance(e, team, order))

        return lineups


    def process_goals(self, team1_goals, team2_goals):
        """
        Process goals for both teams.
        """

        def process_item(s, team):
            s = s.strip()
            if not s:
                return {}

            m = re.match('(.*?)(\d+)', s)
            if m:
                remainder, minute = m.groups()
                minute = int(minute)
            else:
                remainder = s
                minute = None

            if '(' in remainder:
                goal, assists = remainder.split('(')
                assists = [e.strip() for e in assists.replace(')', '').split(',')]
                goal = goal.strip()

            else:
                goal = remainder.strip()
                assists = []

            if goal.strip() == '':
                import pdb; pdb.set_trace()

            if 'name-title' in self.transforms:
                goal = goal.title()
                assists = [e.title() for e in assists]

            return {
                'gid': self.current_game['gid'],
                'competition': self.competition,
                'date': self.current_game['date'],
                'season': self.season,
                'goal': goal,
                'assists': assists,
                'team': team,
                'minute': minute,
                }


        goals = []

        for e in split_outside_parens(team1_goals):
            try:
                goals.append(process_item(e, self.current_game['team1']))
            except:
                import pdb; pdb.set_trace()
 
        for e in split_outside_parens(team2_goals):
            goals.append(process_item(e, self.current_game['team2']))

        self.goals.extend([e for e in goals if e])

            

                    

        
        
if __name__ == "__main__":
    d = "/home/chris/www/soccerdata/data/general"
    for fn in os.listdir(d):
        p = os.path.join(d, fn)
        if os.path.isfile(p) and not fn.endswith("~"):
            print(process_general_file(fn))
    #print(process_general_file("harmarville.txt"))
    
