import pytest

from parse.salaries import process_salaries


FULL = """
Competition: Major League Soccer
Season: 2007
Source: http://example.com/salaries: 2007
Key: team; name; position; base; guaranteed
* a comment

DC United; Nicholas Addlery; F; 36000.00; 36000.00
; David Monsalve; GK; 30000.00; 30000.00
"""

BARE = """
Competition: Major League Soccer
Season: 1996
Key: name; base

Marcelo Balboa; 175000
"""

WEEKLY = """
Competition: American Soccer League (1921-1933)
Season: 1925
Period: week
Key: team; name; base

Boston Wonder Workers; Alex McNab; 25
"""


def run(tmp_path, text):
    (tmp_path / 'salaries').write_text(text)
    return process_salaries('salaries', str(tmp_path))


def test_full_row(tmp_path):
    rows = run(tmp_path, FULL)
    assert rows[0] == {
        'name': 'Nicholas Addlery',
        'team': 'DC United',
        'position': 'F',
        'base': '36000.00',
        'guaranteed': '36000.00',
        'competition': 'Major League Soccer',
        'season': '2007',
        'source': 'http://example.com/salaries: 2007',
        'period': 'year',
        'coverage': 'full',
    }


def test_skips_blank_and_comment_lines(tmp_path):
    assert len(run(tmp_path, FULL)) == 2


def test_empty_team_is_none(tmp_path):
    assert run(tmp_path, FULL)[1]['team'] is None


def test_missing_columns(tmp_path):
    (row,) = run(tmp_path, BARE)
    assert row['team'] is None
    assert row['position'] == ''
    assert row['guaranteed'] is None
    assert row['source'] is None
    assert row['base'] == '175000'


def test_period_header(tmp_path):
    (row,) = run(tmp_path, WEEKLY)
    assert row['period'] == 'week'
    assert row['team'] == 'Boston Wonder Workers'


def test_wrong_field_count_names_the_line(tmp_path):
    with pytest.raises(ValueError, match=r'salaries:7'):
        run(tmp_path, BARE + "Carlos 44625 Mendes; 44625; 44625\n")


def test_coverage_defaults_to_full_and_reported_salaries_carry_their_own_source(tmp_path):
    (tmp_path / '1975').write_text(
        "Competition: North American Soccer League\nSeason: 1975\nCoverage: reported\nKey: team; name; base\n\n"
        "Source: https://a.example\nNew York Cosmos; Pelé; 1670000\n"
        "Source: https://b.example\nDallas Tornado; Kyle Rote Jr.; 7000\n")
    rows = process_salaries('1975', str(tmp_path))
    assert [(r['name'], r['source'], r['coverage']) for r in rows] == [
        ('Pelé', 'https://a.example', 'reported'), ('Kyle Rote Jr.', 'https://b.example', 'reported')]
