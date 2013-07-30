from nose.tools import *
import datetime

from aldo.parse.standings import process_string

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
    assert_equal(s['competition'], 'Major League Soccer')
    assert_equal(s['season'], '2010')
    assert_equal(s['team'], 'Sporting Kansas City')
    assert_equal(s['games'], 34)
    assert_equal(s['wins'], 13)
    assert_equal(s['ties'], 12)
    assert_equal(s['losses'], 9)
    assert_equal(s['points'], 51)
    assert_equal(s['goals_for'], 50)
    assert_equal(s['goals_against'], 40)


    s2 = standings[1]
    assert_equal(s2['competition'], 'Major League Soccer')
    assert_equal(s2['season'], '2010')
    assert_equal(s2['team'], 'Philadelphia Union')
    assert_equal(s2['games'], 34)
    assert_equal(s2['wins'], 11)
    assert_equal(s2['ties'], 15)
    assert_equal(s2['losses'], 8)
    assert_equal(s2['points'], 48)
    assert_equal(s2['goals_for'], 44)
    assert_equal(s2['goals_against'], 36)

