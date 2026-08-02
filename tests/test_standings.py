from parse.standings import process_string

BASIC = """
Competition: Major League Soccer
Season: 2010
Group: Eastern Conference
Key: team; games; wins; ties; losses; points; goals_for; goals_against
Sporting Kansas City; 34; 13; 12; 9; 51; 50; 40
Philadelphia Union; 34; 11; 15; 8; 48; 44; 36			
"""

def test_basic_standings():
    standings = process_string(BASIC, ';')

    s = standings[0]
    assert s['competition'] == 'Major League Soccer'
    assert s['season'] == '2010'
    assert s['team'] == 'Sporting Kansas City'
    assert s['games'] == 34
    assert s['wins'] == 13
    assert s['ties'] == 12
    assert s['losses'] == 9
    assert s['points'] == 51
    assert s['goals_for'] == 50
    assert s['goals_against'] == 40


    s2 = standings[1]
    assert s2['competition'] == 'Major League Soccer'
    assert s2['season'] == '2010'
    assert s2['team'] == 'Philadelphia Union'
    assert s2['games'] == 34
    assert s2['wins'] == 11
    assert s2['ties'] == 15
    assert s2['losses'] == 8
    assert s2['points'] == 48
    assert s2['goals_for'] == 44
    assert s2['goals_against'] == 36

