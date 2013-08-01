#from nose.tools import *
import datetime

from aldo.parse.games import process_string

ASDET = """
Competition: MLS Cup Playoffs
Season: 2010
1/15/2014; Seattle Sounders; 1-0 (asdet); Real Salt Lake; Real Salt Lake; John Referee, Ramon Linesman, Dirk Assistant; 25000
Zach Scott (unassisted) 95;
"""

def test_asdet_game():
    games, goals, misconduct, appearances, rosters = process_string(BASIC)
    g = games[0]
    assert_equal(g['competition'], 'MLS Cup Playoffs')
    assert_equal(g['season'], '2010')
    assert_equal(g['date'], datetime.datetime(2014, 1, 15))
    assert_equal(g['team1'], 'Seattle Sounders')
    assert_equal(g['team2'], 'Real Salt Lake')
    assert_equal(g['home_team'], 'Real Salt Lake')
    assert_equal(g['team1_score'], 1)
    assert_equal(g['team2_score'], 0)
    assert_equal(g['minutes'], 95)


BASIC = """
Competition: Major League Soccer
Season: 2010
12/10/2010; Seattle Sounders; 3-1; Real Salt Lake; Real Salt Lake; John Referee, Ramon Linesman, Dirk Assistant; 25000
Fredy Montero (unassisted) 2, Fredy Montero (Osvaldo Alonso) 8, Kasey Keller (pk) 18; Own Goal (Fredy Montero) 
Seattle Sounders: Kasey Keller, Osvaldo Alonso, Lamar Neagle, Fredy Montero
Real Salt Lake: Nick Rimando, Chris Schuler (Kyle Beckerman 30, Jason Kreis 60)
Source: Imagination
Notes: This game never happened.
"""

def test_basic_game():
    games, goals, misconduct, appearances, rosters = process_string(BASIC)
    g = games[0]
    assert_equal(g['competition'], 'Major League Soccer')
    assert_equal(g['season'], '2010')
    assert_equal(g['date'], datetime.datetime(2010, 12, 10))
    assert_equal(g['team1'], 'Seattle Sounders')
    assert_equal(g['team2'], 'Real Salt Lake')
    assert_equal(g['home_team'], 'Real Salt Lake')
    assert_equal(g['team1_score'], 3)
    assert_equal(g['team2_score'], 1)
    assert_equal(g['attendance'], 25000)
    assert_equal(g['location'], '')
    assert_equal(g['referee'], 'John Referee')
    assert_equal(g['linesmen'], ['Ramon Linesman', 'Dirk Assistant'])
    assert_equal(g['sources'], ['Imagination'])
    assert_equal(g['notes'], 'This game never happened.')



def test_basic_goals():
    games, goals, misconduct, appearances, rosters = process_string(BASIC)
    assert_equal(goals[0]['goal'], 'Fredy Montero')
    assert_equal(goals[0]['assists'], ['unassisted'])
    #assert_equal(goals[0]['unassisted'], True)
    assert_equal(goals[0]['date'], datetime.datetime(2010, 12, 10))
    assert_equal(goals[0]['minute'], 2)
    assert_equal(goals[0]['team'], 'Seattle Sounders')

    assert_equal(goals[1]['goal'], 'Fredy Montero')
    assert_equal(goals[1]['assists'], ['Osvaldo Alonso'])
    assert_equal(goals[1]['minute'], 8)

    assert_equal(goals[2]['goal'], 'Kasey Keller')
    assert_equal(goals[2]['assists'], ['pk'])
    #assert_equal(goals[2]['penalty_kick'], True)

    g2 = goals[2]
    assert_equal(g2['assists'], [])
    assert_equal(g2['penalty'], True)

    assert_equal(goals[3]['goal'], 'Own Goal')
    assert_equal(goals[3]['assists'], ['Fredy Montero'])
    assert_equal(goals[3]['team'], 'Real Salt Lake')

    g3 = goals[3]
    assert_equal(g3['own_goal'], True)
    assert_equal(g3['assists'], [])
    assert_equal(g3['own_goal_player'], 'Fredy Montero')
                        

def test_basic_lineups():
    games, goals, misconduct, appearances, rosters = process_string(BASIC)
    assert_equal(len(appearances), 8)
    assert_equal([e['name'] for e in appearances], ['Kasey Keller', 'Osvaldo Alonso', 'Lamar Neagle', 'Fredy Montero', 'Nick Rimando', 'Chris Schuler', 'Kyle Beckerman', 'Jason Kreis'])
    assert_equal(appearances[0]['on'], 0)
    assert_equal(appearances[0]['off'], 90)
    assert_equal(appearances[0]['team'], 'Seattle Sounders')


    assert_equal(appearances[5]['name'], 'Chris Schuler')
    assert_equal(appearances[6]['name'], 'Kyle Beckerman')
    assert_equal(appearances[7]['name'], 'Jason Kreis')

    assert_equal(appearances[5]['on'], 0)
    assert_equal(appearances[6]['on'], 30)
    assert_equal(appearances[7]['on'], 60)

    assert_equal(appearances[5]['off'], 30)
    assert_equal(appearances[6]['off'], 60)
    assert_equal(appearances[7]['off'], 90)




FORFEIT = """
Competition: U.S. Open Cup
Season: 1936
Round: First Round
Group: Pittsburgh Sector
1/12/1936; Curry Silver Tops; W-L; Kodak Park FC; Pittsburgh, PA
Forfeit
Source: http://www.soccerstats.us/games/555
"""


def test_forfeit():
    games, goals, misconduct, appearances, rosters = process_string(FORFEIT)
    g = games[0]
    assert_equal(g['competition'], 'U.S. Open Cup')
    assert_equal(g['season'], '1936')
    assert_equal(g['round'], 'First Round')
    assert_equal(g['group'], 'Pittsburgh Sector')
    assert_equal(g['team1'], 'Curry Silver Tops')
    assert_equal(g['team2'], 'Kodak Park FC')
    assert_equal(g['home_team'], None)
    assert_equal(g['team1_score'], None)
    assert_equal(g['team2_score'], None)
    assert_equal(g['team1_result'], 'w')
    assert_equal(g['team2_result'], 'l')
    assert_equal(g['attendance'], None)
    assert_equal(g['location'], 'Pittsburgh, PA')
    assert_equal(g['referee'], None)
    assert_equal(g['linesmen'], [])
    assert_equal(g['forfeit'], True)
    assert_equal(g['sources'], ['http://www.soccerstats.us/games/555'])

    assert_equal(g['notes'], '')



RED_CARD = """
Competition: Panamerican Cup
Season: 1961
Round: Final
12/18/1961; Boca Juniors; 2-1; Los Angeles Kickers; Estadio Azteca; Andor Dorogi; 80000
Red Card: Antonio Rattin; Eberhard Herz 68
"""




def test_red_card():
    games, goals, misconduct, appearances, rosters = process_string(RED_CARD)
    g = games[0]
    assert_equal(g['competition'], 'Panamerican Cup')
    assert_equal(g['season'], '1961')
    assert_equal(g['round'], 'Final')
    assert_equal(g['team1'], 'Boca Juniors')
    assert_equal(g['team2'], 'Los Angeles Kickers')
    assert_equal(g['home_team'], None)
    assert_equal(g['team1_score'], 2)
    assert_equal(g['team2_score'], 1)
    #assert_equal(g['team1_result'], 'w')
    #assert_equal(g['team2_result'], 'l')
    assert_equal(g['attendance'], 80000)
    assert_equal(g['location'], 'Estadio Azteca')
    assert_equal(g['referee'], 'Andor Dorogi')
    assert_equal(g['linesmen'], [])
    assert_equal(g['sources'], [])
    assert_equal(g['notes'], '')

    assert_equal(len(misconduct), 2)

    r1 = misconduct[0]
    assert_equal(r1['name'], 'Antonio Rattin')
    assert_equal(r1['team'], 'Boca Juniors')
    assert_equal(r1['minute'], None)
    assert_equal(r1['type'], 'red')

    print(misconduct)

    r2 = misconduct[1]
    assert_equal(r2['name'], 'Eberhard Herz')
    assert_equal(r2['team'], 'Los Angeles Kickers')
    assert_equal(r2['minute'], 68)
    assert_equal(r2['type'], 'red')


BLOCKSOURCE = """
BlockSource: The Bible
Competition: Ancient Soccer
Season: -750
; Reuben; W-L; Simeon; Jahaza
; Levi; T-T; Gad; Jazer
; Benjamin; ?; Issachar; Jericho
; Asher; np; Zebulun; Sidon
"""


def test_blocksource():
    games, goals, misconduct, appearances, rosters = process_string(BLOCKSOURCE)
    g = games[0]
    assert_equal(g['competition'], 'Ancient Soccer')
    assert_equal(g['season'], '-750')
    assert_equal(g['team1'], 'Reuben')
    assert_equal(g['team2'], 'Simeon')
    assert_equal(g['home_team'], None)
    assert_equal(g['team1_score'], None)
    assert_equal(g['team2_score'], None)
    assert_equal(g['team1_result'], 'w')
    assert_equal(g['team2_result'], 'l')
    assert_equal(g['location'], 'Jahaza')
    assert_equal(g['sources'], ['The Bible'])


    g1 = games[1]
    assert_equal(g1['team1'], 'Levi')
    assert_equal(g1['team2'], 'Gad')
    assert_equal(g1['team1_score'], None)
    assert_equal(g1['team2_score'], None)
    assert_equal(g1['team1_result'], 't')
    assert_equal(g1['team2_result'], 't')
    assert_equal(g1['sources'], ['The Bible'])

    g2 = games[2]
    assert_equal(g2['team1'], 'Benjamin')
    assert_equal(g2['team2'], 'Issachar')
    assert_equal(g2['team1_score'], None)
    assert_equal(g2['team2_score'], None)
    assert_equal(g2['team1_result'], None)
    assert_equal(g2['team2_result'], None)
    assert_equal(g2['sources'], ['The Bible'])

    g3 = games[3]
    assert_equal(g3['team1'], 'Asher')
    assert_equal(g3['team2'], 'Zebulun')
    assert_equal(g3['team1_score'], None)
    assert_equal(g3['team2_score'], None)
    assert_equal(g3['team1_result'], None)
    assert_equal(g3['team2_result'], None)
    assert_equal(g3['sources'], ['The Bible'])



MINUTES = """
Competition: International Soccer League
Season: 1963
6/5/1963; Preussen Munster; 4-2; SC Recife; Downing Stadium
Minutes: 50


Competition: MLS Cup Playoffs
Season: 2003

10/10/2003; DC United; 0-0 (aet); New England Revolution; RFK Stadium
10/10/2003; FC Dallas; 1-0 (asdet); Chicago Fire; Dallas, TX
Jason Kreis 98;
"""

# Add shootout test.

def test_minutes():
    games, goals, misconduct, appearances, rosters = process_string(MINUTES)
    g1 = games[0]
    assert_equal(g1['competition'], 'International Soccer League')
    assert_equal(g1['season'], '1963')
    assert_equal(g1['team1'], 'Preussen Munster')
    assert_equal(g1['team2'], 'SC Recife')
    assert_equal(g1['team1_score'], 4)
    assert_equal(g1['team2_score'], 2)
    assert_equal(g1['minutes'], 50)

    g2 = games[1]
    assert_equal(g2['competition'], 'MLS Cup Playoffs')
    assert_equal(g2['season'], '2003')
    assert_equal(g2['team1'], 'DC United')
    assert_equal(g2['team2'], 'New England Revolution')
    assert_equal(g2['team1_score'], 0)
    assert_equal(g2['team2_score'], 0)
    assert_equal(g2['minutes'], 120)


    g3 = games[2]
    assert_equal(g3['team1'], 'FC Dallas')
    assert_equal(g3['team2'], 'Chicago Fire')
    assert_equal(g3['minutes'], 'asdet')


VIDEO = """
Competition: MLS Cup Playoffs
Round: Final
Season: 1996

10/20/1996; Los Angeles Galaxy; 2-3 (asdet); DC United; Foxboro Stadium; Esse Baharmast; 34643
Eduardo Hurtado (Mauricio Cienfuegos) 5, Chris Armas (unassisted) 56; Tony Sanneh (Marco Etcheverry) 73, Shawn Medved (unassisted) 81, Eddie Pope (Marco Etcheverry) 94
Los Angeles Galaxy: Jorge Campos, Mark Semioli, Robin Fraser, Greg Vanney, Arash Noamouz, Jorge Salcedo (Curt Onalfo 77), Chris Armas, Mauricio Cienfuegos, Cobi Jones, Harut Karapetyan (Ante Razov 76), Eduardo Hurtado
DC United: Mark Simpson, Clint Peay, Eddie Pope, Jeff Agoos, Mario Gori (Shawn Medved 70), Richie Williams, John Maessner (Tony Sanneh 59), John Harkes, Marco Etcheverry, Jaime Moreno, Raul Diaz Arce
Video: http://www.youtube.com/watch?v=AyRVWDgxovY
"""


def test_video():
    games, goals, misconduct, appearances, rosters = process_string(VIDEO)
    g1 = games[0]
    assert_equal(g1['competition'], 'MLS Cup Playoffs')
    assert_equal(g1['season'], '1996')
    assert_equal(g1['team1'], 'Los Angeles Galaxy')
    assert_equal(g1['team2'], 'DC United')
    assert_equal(g1['team1_score'], 2)
    assert_equal(g1['team2_score'], 3)
    #assert_equal(g1['minutes'], 94)
    assert_equal(g1['video'], 'http://www.youtube.com/watch?v=AyRVWDgxovY')



LINEUPS = """
Competition: USL First Division
Season: 2004

10/20/1996; Charleston Battery; 1-0; Rochester Rhinos
Charleston Battery: John Wilson [Nothing], Paul Conway, 12-Osvaldo Alonso
"""

def test_lineups():
    games, goals, misconduct, appearances, rosters = process_string(LINEUPS)
    g1 = games[0]
    assert_equal(g1['competition'], 'USL First Division')
    assert_equal(g1['season'], '2004')
    assert_equal(g1['team1'], 'Charleston Battery')
    assert_equal(g1['team2'], 'Rochester Rhinos')
    assert_equal(g1['team1_score'], 1)
    assert_equal(g1['team2_score'], 0)
    assert_equal(appearances[0]['name'], 'John Wilson')
    assert_equal(appearances[1]['name'], 'Paul Conway')
    assert_equal(appearances[2]['name'], 'Osvaldo Alonso')

