import datetime

from parse.rosters import (
    RosterProcessor,
    RosterProcessor2,
    RosterProcessor3,
    filter_brackets,
    fix_roster_name,
)


def run(processor, text):
    """Feed a fixture through a processor line by line."""
    for line in text.strip().split('\n'):
        processor.process_line(line)
    return processor


def test_filter_brackets():
    assert filter_brackets('Jaime Moreno') == 'Jaime Moreno'
    assert filter_brackets('Ben Olsen [captain]') == 'Ben Olsen '
    assert filter_brackets('[Rochester] Doug Miller') == ' Doug Miller'
    assert filter_brackets('') == ''


def test_filter_brackets_docstring_example():
    s = 'Doug Miller [Rochester Rhinos] (Josh Wolff [Project-40] 78)'
    assert filter_brackets(s) == 'Doug Miller  (Josh Wolff  78)'


def test_fix_roster_name():
    assert fix_roster_name('JAIME MORENO') == 'Jaime Moreno'
    assert fix_roster_name('jaime moreno') == 'Jaime Moreno'
    assert fix_roster_name('Jaime') == 'Jaime'


def test_fix_roster_name_quoted_nickname():
    """A leading quote is skipped so the letter after it is capitalized."""
    assert fix_roster_name('JUAN "HARRY" HAYES') == 'Juan "Harry" Hayes'


ROSTER2 = """
Competition: Major League Soccer
Season: 2010
* a comment line

DC United: Jaime Moreno, Ben Olsen, Eddie Pope
Seattle Sounders: Kasey Keller, Osvaldo Alonso
"""


def test_roster2_basic():
    rosters = run(RosterProcessor2(), ROSTER2).rosters
    assert len(rosters) == 5

    first = rosters[0]
    assert first['competition'] == 'Major League Soccer'
    assert first['season'] == '2010'
    assert first['team'] == 'DC United'
    assert first['name'] == 'Jaime Moreno'

    assert [r['name'] for r in rosters[:3]] == [
        'Jaime Moreno', 'Ben Olsen', 'Eddie Pope']
    assert rosters[3]['team'] == 'Seattle Sounders'
    assert rosters[4]['name'] == 'Osvaldo Alonso'


def test_roster2_strips_brackets():
    rosters = run(RosterProcessor2(), 'DC United: Ben Olsen [captain], Eddie Pope').rosters
    assert [r['name'] for r in rosters] == ['Ben Olsen', 'Eddie Pope']


ROSTER3 = """
Competition: Major League Soccer
Season: 2010
Team: DC United
Key: name; games; goals; height; weight; birthdate
Jaime Moreno; 30; 12; 5-9; 165; 1/19/1974
"""


def test_roster3_basic():
    data = run(RosterProcessor3(), ROSTER3).data
    assert len(data) == 1

    d = data[0]
    assert d['name'] == 'Jaime Moreno'
    assert d['competition'] == 'Major League Soccer'
    assert d['season'] == '2010'


def test_roster3_coerces_numbers():
    """games is renamed to games_played; height becomes inches."""
    d = run(RosterProcessor3(), ROSTER3).data[0]
    assert d['games_played'] == 30
    assert 'games' not in d
    assert d['goals'] == 12
    assert d['height'] == 69
    assert d['weight'] == 165
    assert d['birthdate'] == datetime.datetime(1974, 1, 19)


def test_roster3_missing_values():
    """'-' and '' count as zero; '?' is unknown."""
    d = run(RosterProcessor3(), 'Key: name; goals; assists\nBob; -; ?').data[0]
    assert d['goals'] == 0
    assert d['assists'] == None


def test_roster3_year_becomes_season():
    d = run(RosterProcessor3(), 'Key: name; year\nBob; 1996').data[0]
    assert d['season'] == '1996'
    assert 'year' not in d


def test_roster3_name_title_transform():
    text = 'Transform: name-title\nKey: name\njaime moreno'
    assert run(RosterProcessor3(), text).data[0]['name'] == 'Jaime Moreno'


def test_roster3_alternate_delimiter():
    d = run(RosterProcessor3(delimiter=','), 'Key: name, goals\nBob, 3').data[0]
    assert d['name'] == 'Bob'
    assert d['goals'] == 3


def test_roster3_skips_blank_and_comment_lines():
    data = run(RosterProcessor3(), 'Key: name\n\n* a comment\nBob').data
    assert [d['name'] for d in data] == ['Bob']


def test_roster3_row_shorter_than_key():
    """zip() truncates, so a missing trailing field is simply absent."""
    d = run(RosterProcessor3(), 'Key: name; goals; assists\nBob; 3').data[0]
    assert d['goals'] == 3
    assert 'assists' not in d


# --- Known bugs. These fail on purpose; see ROADMAP.md. ---

def test_fix_roster_name_accented_initial():
    """char_dict is applied after capitalize(), undoing it for accented initials."""
    assert fix_roster_name('ÁNGEL') == 'Ángel'


def test_roster3_strips_team_and_source():
    """Team: and BlockSource: are not stripped, unlike Competition: and Season:."""
    text = 'BlockSource: rsssf.com\nTeam: DC United\nKey: name\nBob'
    d = run(RosterProcessor3(), text).data[0]
    assert d['team'] == 'DC United'
    assert d['source'] == 'rsssf.com'


def test_roster1_reads_a_player_line():
    """RosterProcessor references an undefined `name`, so every player line raises."""
    text = 'Competition: Major League Soccer\nSeason: 2010\nTeam: DC United\n10 Jaime Moreno'
    rosters = run(RosterProcessor(), text).rosters
    assert [r['name'] for r in rosters] == ['Jaime Moreno']
