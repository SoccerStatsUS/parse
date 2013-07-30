from collections import defaultdict

# Need to remove overlapping games in individual collections, then remove them in combination.
# Export games to standard format.
# Incorporate comments, rounds, groups, red cards.


def format_game(g):
    s = ''
    date_string = g['date'].strftime("%m/%d/%Y")

    if g.get('stadium'):
        location_string = g['stadium']
    elif g.get('location'):
        location_string = g['location']
    elif g.get('home_team'):
        location_string = g['home_team']
    else:
        location_string = ''

    referee_string = ''
    if g.get('referee'):
        referee_string += g['referee']

        # This should actually be linesmen.
        
        if g.get('linesman1'):
            referee_string += ', %s' % g['linesman1']

        if g.get('linesman2'):
            referee_string += ', %s' % g['linesman2']

        if g.get('linesman3'):
            referee_string += ', %s' % g['linesman3']

    score_string = "%s-%s" % (g['team1_score'], g['team2_score'])
    s = "%s; %s; %s; %s; %s" % (date_string, g['team1'], score_string, g['team2'], location_string)

    if referee_string:
        s += "; %s" % referee_string

    if g['attendance']:
        s += '; %s' % g['attendance']

    return s


def format_goal(goal):
    s = goal['goal']
    if goal.get('assists'):
        assists = ' :: '.join(goal['assists'])
        s += ' (%s)' % assists
    
    if goal['minute']:
        s += ' %s' % goal['minute']

    return s


def format_goals(game, goal_dict):
    team1_goals = goal_dict[(game['team1'], game['date'])]
    team2_goals = goal_dict[(game['team2'], game['date'])]

    if not team1_goals and not team2_goals:
        return ''

    team1_string = ', '.join([format_goal(g) for g in team1_goals])
    team2_string = ', '.join([format_goal(g) for g in team2_goals])
    s = '%s; %s' % (team1_string, team2_string)
    return s
        
        
def format_lineup(game, lineup_dict):
    pass


def format_source(game, block_source):
    if block_source:
        return ''

    if game.get('source'):
        return "Source: %s" % game['source']

    if game.get('sources'):
        return "Source: %s" % game['sources'][-1]


def format_misc(game):
    s = ''
    if game.get('minigame'):
        s += 'Minigame\n'

    return s


        
def format_chunk(game, goal_dict, lineup_dict, block_source):
    s = format_game(game)
    goal_string = format_goals(game, goal_dict)
    if goal_string:
        s += "\n%s" % goal_string

    lineup_string = format_lineup(game, lineup_dict)
    if lineup_string:
        s += "\n%s" % lineup_string

    source_string = format_source(game, block_source)
    if source_string:
        s += "\n%s" % source_string
        
    misc_string = format_misc(game)
    if misc_string:
        s += "\n%s" % misc_string

    s += '\n'

    return s

    


def export_data(games_coll, goals_coll, lineups_coll, fouls_coll=None, block_source=''):
    game_dict = {}
    goals = defaultdict(list)
    lineups = defaultdict(list)

    for game in games_coll.find():
        key = (game['team1'], game['team2'], game['date'], game.get('minigame'))
        game_dict[key] = game

    for goal in goals_coll.find():
        key = (goal['team'], goal['date'])
        goals[key].append(goal)

    for lineup in lineups_coll.find():
        key = (lineup['team'], lineup['date'])
        lineups[key].append(lineup)


    game_list = sorted([e for e in games_coll.find()], key=lambda d: (d['competition'], d['season'], d['date']))


    competition = season = None



    #f = open(fn)

    if block_source:
        print('Block Source: %s' % block_source)


    for game in game_list:


        c = game['competition']
        s = game['season']

        if c != competition:
            competition = c
            print("\nCompetition: %s" % c)
            
        if s != season:
            season = s
            print("\nSeason: %s\n" % s)
            

        print(format_chunk(game, goals, lineups, block_source))

    import pdb; pdb.set_trace()
    x = 5
        

    
