from parse.stats import StatsProcessor, process_name


def run(text, **kwargs):
    """Feed a fixture through a processor line by line."""
    sp = StatsProcessor(**kwargs)
    for line in text.strip().split('\n'):
        sp.process_line(line)
    return sp


BASIC = """
Competition: Major League Soccer
Season: 1998
Key: name; games; goals; assists
* a comment

Ante Razov; 30; 10; 9
Roman Kosecki; 25; 9; 9
"""


def test_process_name_reorders():
    assert process_name('Ralph, Damani') == 'Damani Ralph'
    assert process_name('Williams, Andy') == 'Andy Williams'


def test_process_name_without_comma_is_unchanged():
    assert process_name('Ante Razov') == 'Ante Razov'


def test_process_name_mapping():
    """A handful of malformed source names are corrected by lookup."""
    assert process_name('Kolba, JR., Thoms') == 'Thomas Kolba Jr.'
    assert process_name('Novas, Lomonaca, Ignacio') == 'Ignacio Novas'


def test_process_name_assumes_one_comma():
    """split(',', 1) means a second comma stays in the first name."""
    assert process_name('Smith, Bob, Jr') == 'Bob, Jr Smith'


def test_basic_stats():
    data = run(BASIC).data
    assert len(data) == 2

    d = data[0]
    assert d['name'] == 'Ante Razov'
    assert d['competition'] == 'Major League Soccer'
    assert d['season'] == '1998'
    assert data[1]['name'] == 'Roman Kosecki'


def test_coerces_numbers():
    d = run(BASIC).data[0]
    assert d['games_played'] == 30
    assert 'games' not in d
    assert d['goals'] == 10
    assert d['assists'] == 9


def test_missing_and_unknown_values():
    """'' and '-' count as zero; '?' is unknown."""
    d = run('Key: name; goals; assists\nBob; -; ').data[0]
    assert d['goals'] == 0
    assert d['assists'] == 0
    assert run('Key: name; goals\nBob; ?').data[0]['goals'] == None


def test_preprocess_removes_nbsp_and_stars():
    """NASL stats mark players with a star; scrapes carry non-breaking spaces."""
    d = run('Key: name; goals\nB\xa0ob*; 3').data[0]
    assert d['name'] == 'Bob'


def test_year_becomes_season():
    """The 1996-2012 file carries season as a column rather than a header."""
    assert run('Key: name; year\nBob; 1998').data[0]['season'] == '1998'


def test_name_title_transform():
    assert run('Transform: name-title\nKey: name\nante razov').data[0]['name'] == 'Ante Razov'


def test_format_name_reorders_last_first():
    d = run('Key: name; goals\nRalph, Damani; 3', format_name=True).data[0]
    assert d['name'] == 'Damani Ralph'


def test_alternate_delimiter():
    d = run('Key: name, goals\nBob, 3', delimiter=',').data[0]
    assert d['name'] == 'Bob'
    assert d['goals'] == 3


def test_skips_blank_and_comment_lines():
    assert len(run(BASIC).data) == 2


def test_strips_team_and_field_values():
    d = run('Team: Chicago Fire\nKey: name; nation\nBob; USA').data[0]
    assert d['team'] == 'Chicago Fire'
    assert d['nation'] == 'USA'
