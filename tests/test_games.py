import datetime

from parse.export import format_game
from parse.games import process_string

ASDET = """
Competition: MLS Cup Playoffs
Season: 2010
1/15/2014; Seattle Sounders; 1-0 (asdet); Real Salt Lake; Real Salt Lake; John Referee, Ramon Linesman, Dirk Assistant; 25000
Zach Scott (unassisted) 95;
"""

def test_asdet_game():
    games, goals, misconduct, appearances, rosters = process_string(ASDET)
    g = games[0]
    assert g['competition'] == 'MLS Cup Playoffs'
    assert g['season'] == '2010'
    assert g['date'] == datetime.datetime(2014, 1, 15)
    assert g['team1'] == 'Seattle Sounders'
    assert g['team2'] == 'Real Salt Lake'
    assert g['home_team'] == 'Real Salt Lake'
    assert g['team1_score'] == 1
    assert g['team2_score'] == 0
    assert g['minutes'] == 95


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
    assert g['competition'] == 'Major League Soccer'
    assert g['season'] == '2010'
    assert g['date'] == datetime.datetime(2010, 12, 10)
    assert g['team1'] == 'Seattle Sounders'
    assert g['team2'] == 'Real Salt Lake'
    assert g['home_team'] == 'Real Salt Lake'
    assert g['team1_score'] == 3
    assert g['team2_score'] == 1
    assert g['attendance'] == 25000
    assert g['location'] == ''
    assert g['referee'] == 'John Referee'
    assert g['linesmen'] == ['Ramon Linesman', 'Dirk Assistant']
    assert g['sources'] == ['Imagination']
    assert g['notes'] == 'This game never happened.'



def test_basic_goals():
    games, goals, misconduct, appearances, rosters = process_string(BASIC)
    assert goals[0]['goal'] == 'Fredy Montero'
    assert goals[0]['assists'] == ['unassisted']
    #assert goals[0]['unassisted'] == True
    assert goals[0]['date'] == datetime.datetime(2010, 12, 10)
    assert goals[0]['minute'] == 2
    assert goals[0]['team'] == 'Seattle Sounders'

    assert goals[1]['goal'] == 'Fredy Montero'
    assert goals[1]['assists'] == ['Osvaldo Alonso']
    assert goals[1]['minute'] == 8

    assert goals[2]['goal'] == 'Kasey Keller'
    assert goals[2]['assists'] == ['pk']
    assert goals[2]['minute'] == 18

    assert goals[3]['goal'] == 'Own Goal'
    assert goals[3]['assists'] == ['Fredy Montero']
    assert goals[3]['team'] == 'Real Salt Lake'
                        

def test_basic_lineups():
    games, goals, misconduct, appearances, rosters = process_string(BASIC)
    assert len(appearances) == 8
    assert [e['name'] for e in appearances] == ['Kasey Keller', 'Osvaldo Alonso', 'Lamar Neagle', 'Fredy Montero', 'Nick Rimando', 'Chris Schuler', 'Kyle Beckerman', 'Jason Kreis']
    assert appearances[0]['on'] == 0
    assert appearances[0]['off'] == 90
    assert appearances[0]['team'] == 'Seattle Sounders'


    assert appearances[5]['name'] == 'Chris Schuler'
    assert appearances[6]['name'] == 'Kyle Beckerman'
    assert appearances[7]['name'] == 'Jason Kreis'

    assert appearances[5]['on'] == 0
    assert appearances[6]['on'] == 30
    assert appearances[7]['on'] == 60

    assert appearances[5]['off'] == 30
    assert appearances[6]['off'] == 60
    assert appearances[7]['off'] == 90




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
    assert g['competition'] == 'U.S. Open Cup'
    assert g['season'] == '1936'
    assert g['group'] == 'Pittsburgh Sector'
    assert g['team1'] == 'Curry Silver Tops'
    assert g['team2'] == 'Kodak Park FC'
    assert g['home_team'] == None
    assert g['team1_score'] == None
    assert g['team2_score'] == None
    assert g['team1_result'] == 'w'
    assert g['team2_result'] == 'l'
    assert g['attendance'] == None
    assert g['location'] == 'Pittsburgh, PA'
    assert g['referee'] == None
    assert g['linesmen'] == []
    assert g['forfeit'] == True
    assert g['sources'] == ['http://www.soccerstats.us/games/555']

    assert g['notes'] == ''


HEADER_ORDER = """
Competition: Olympic Games
Season: 2012
Round: Preliminary
Group: A
7/26/2012; Great Britain; 1-1; Senegal; Old Trafford
"""


# Known bug; see ROADMAP.md.
def test_group_header_does_not_clear_round():
    """Group: clears round, so a Round: written above it is lost."""
    games, goals, misconduct, appearances, rosters = process_string(HEADER_ORDER)
    g = games[0]
    assert g['group'] == 'A'
    assert g['round'] == 'Preliminary'


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
    assert g['competition'] == 'Panamerican Cup'
    assert g['season'] == '1961'
    assert g['round'] == 'Final'
    assert g['team1'] == 'Boca Juniors'
    assert g['team2'] == 'Los Angeles Kickers'
    assert g['home_team'] == None
    assert g['team1_score'] == 2
    assert g['team2_score'] == 1
    #assert g['team1_result'] == 'w'
    #assert g['team2_result'] == 'l'
    assert g['attendance'] == 80000
    assert g['location'] == 'Estadio Azteca'
    assert g['referee'] == 'Andor Dorogi'
    assert g['linesmen'] == []
    assert g['sources'] == []
    assert g['notes'] == ''

    assert len(misconduct) == 2

    r1 = misconduct[0]
    assert r1['name'] == 'Antonio Rattin'
    assert r1['team'] == 'Boca Juniors'
    assert r1['minute'] == None
    assert r1['type'] == 'red'

    print(misconduct)

    r2 = misconduct[1]
    assert r2['name'] == 'Eberhard Herz'
    assert r2['team'] == 'Los Angeles Kickers'
    assert r2['minute'] == 68
    assert r2['type'] == 'red'


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
    assert g['competition'] == 'Ancient Soccer'
    assert g['season'] == '-750'
    assert g['team1'] == 'Reuben'
    assert g['team2'] == 'Simeon'
    assert g['home_team'] == None
    assert g['team1_score'] == None
    assert g['team2_score'] == None
    assert g['team1_result'] == 'w'
    assert g['team2_result'] == 'l'
    assert g['location'] == 'Jahaza'
    assert g['sources'] == ['The Bible']


    g1 = games[1]
    assert g1['team1'] == 'Levi'
    assert g1['team2'] == 'Gad'
    assert g1['team1_score'] == None
    assert g1['team2_score'] == None
    assert g1['team1_result'] == 't'
    assert g1['team2_result'] == 't'
    assert g1['sources'] == ['The Bible']

    g2 = games[2]
    assert g2['team1'] == 'Benjamin'
    assert g2['team2'] == 'Issachar'
    assert g2['team1_score'] == None
    assert g2['team2_score'] == None
    assert g2['team1_result'] == None
    assert g2['team2_result'] == None
    assert g2['sources'] == ['The Bible']

    g3 = games[3]
    assert g3['team1'] == 'Asher'
    assert g3['team2'] == 'Zebulun'
    assert g3['team1_score'] == None
    assert g3['team2_score'] == None
    assert g3['team1_result'] == None
    assert g3['team2_result'] == None
    assert g3['sources'] == ['The Bible']


BLOCKSOURCE_UNSET = """
BlockSource: The Bible
Competition: Ancient Soccer
Season: -750
; Reuben; W-L; Simeon; Jahaza

BlockSource:
; Levi; T-T; Gad; Jazer
; Benjamin; W-L; Issachar; Jericho
Source: The Almanac
"""


def test_blocksource_unset():
    """A BlockSource with no value stops the previous one carrying forward."""
    games = process_string(BLOCKSOURCE_UNSET)[0]

    assert games[0]['team1'] == 'Reuben'
    assert games[0]['sources'] == ['The Bible']

    assert games[1]['team1'] == 'Levi'
    assert games[1]['sources'] == []

    assert games[2]['team1'] == 'Benjamin'
    assert games[2]['sources'] == ['The Almanac']


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
    assert g1['competition'] == 'International Soccer League'
    assert g1['season'] == '1963'
    assert g1['team1'] == 'Preussen Munster'
    assert g1['team2'] == 'SC Recife'
    assert g1['team1_score'] == 4
    assert g1['team2_score'] == 2
    assert g1['minutes'] == 50

    g2 = games[1]
    assert g2['competition'] == 'MLS Cup Playoffs'
    assert g2['season'] == '2003'
    assert g2['team1'] == 'DC United'
    assert g2['team2'] == 'New England Revolution'
    assert g2['team1_score'] == 0
    assert g2['team2_score'] == 0
    assert g2['minutes'] == 120


    g3 = games[2]
    assert g3['team1'] == 'FC Dallas'
    assert g3['team2'] == 'Chicago Fire'
    assert g3['minutes'] == 98


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
    assert g1['competition'] == 'MLS Cup Playoffs'
    assert g1['season'] == '1996'
    assert g1['team1'] == 'Los Angeles Galaxy'
    assert g1['team2'] == 'DC United'
    assert g1['team1_score'] == 2
    assert g1['team2_score'] == 3
    #assert g1['minutes'] == 94
    assert g1['video'] == 'http://www.youtube.com/watch?v=AyRVWDgxovY'



LINEUPS = """
Competition: USL First Division
Season: 2004

10/20/1996; Charleston Battery; 1-0; Rochester Rhinos
Charleston Battery: John Wilson [Nothing], Paul Conway, 12-Osvaldo Alonso
"""

def test_lineups():
    games, goals, misconduct, appearances, rosters = process_string(LINEUPS)
    g1 = games[0]
    assert g1['competition'] == 'USL First Division'
    assert g1['season'] == '2004'
    assert g1['team1'] == 'Charleston Battery'
    assert g1['team2'] == 'Rochester Rhinos'
    assert g1['team1_score'] == 1
    assert g1['team2_score'] == 0
    assert appearances[0]['name'] == 'John Wilson'
    assert appearances[1]['name'] == 'Paul Conway'
    assert appearances[2]['name'] == 'Osvaldo Alonso'


HOME_TEAM = """
Competition: Major League Soccer
Season: 2010
12/10/2010; Seattle Sounders; 3-1; Real Salt Lake; Real Salt Lake
12/11/2010; Chicago Fire; 1-1; Toronto FC; home
12/12/2010; DC United; 0-2; Columbus Crew; away
12/13/2010; LA Galaxy; 2-0; Chivas USA; neutral
12/14/2010; Portland Timbers; 1-0; Colorado Rapids; Providence Park
"""


def test_home_team_designators():
    """A team name, 'home' and 'away' set home_team and leave location empty."""
    games, goals, misconduct, appearances, rosters = process_string(HOME_TEAM)

    named, home, away, neutral, venue = games

    assert named['home_team'] == 'Real Salt Lake'
    assert named['location'] == ''

    assert home['home_team'] == 'Chicago Fire'
    assert home['location'] == ''

    assert away['home_team'] == 'Columbus Crew'
    assert away['location'] == ''

    # 'neutral' is still left in location; see ROADMAP.md.
    assert neutral['neutral'] == True
    assert neutral['home_team'] == None

    assert venue['location'] == 'Providence Park'
    assert venue['home_team'] == None


def test_home_team_export_round_trip():
    """Clearing location is lossless: the exporter falls back to home_team."""
    games, goals, misconduct, appearances, rosters = process_string(HOME_TEAM)

    assert format_game(games[0]) == (
        '12/10/2010; Seattle Sounders; 3-1; Real Salt Lake; Real Salt Lake')
    assert format_game(games[4]) == (
        '12/14/2010; Portland Timbers; 1-0; Colorado Rapids; Providence Park')



HOME_LINE = """
Competition: Major League Soccer
Season: 2025
2/22/2025; LAFC; 1-0; Minnesota United; BMO Stadium; Guido Gonzales Jr.; 22000
Home: LAFC
Source: https://stats-api.mlssoccer.com/matches/MLS-MAT-0009BE

2/23/2025; Inter Miami; 2-2; NYC FC; Chase Stadium
Home: NYC FC

2/24/2025; Atlanta United; 3-2; CF Montreal; Mercedes-Benz Stadium
"""


def test_home_line_names_the_home_side_alongside_a_venue():
    games, goals, misconduct, appearances, rosters = process_string(HOME_LINE)
    first, second, third = games

    assert first['home_team'] == 'LAFC'
    assert first['location'] == 'BMO Stadium'
    assert first['neutral'] is False
    assert first['sources'][-1] == 'https://stats-api.mlssoccer.com/matches/MLS-MAT-0009BE'

    # The line names whichever side the source says, not the first listed.
    assert second['home_team'] == 'NYC FC'

    # Without the line, a venue alone still says nothing about home.
    assert third['home_team'] is None


def test_home_line_naming_neither_side_is_a_data_warning(monkeypatch):
    import pdb
    hits = []
    monkeypatch.setattr(pdb, 'set_trace', lambda: hits.append(1))
    text = HOME_LINE.replace('Home: LAFC', 'Home: Seattle Sounders')
    games = process_string(text)[0]
    assert hits == [1]
    assert games[0]['home_team'] is None


def test_home_line_export_round_trip():
    games = process_string(HOME_LINE)[0]
    assert format_game(games[0]) == (
        '02/22/2025; LAFC; 1-0; Minnesota United; BMO Stadium; Guido Gonzales Jr.; 22000'
        '\nHome: LAFC')
    # A home team that already sits in the location slot needs no extra line.
    named = process_string(HOME_TEAM)[0][0]
    assert 'Home:' not in format_game(named)
