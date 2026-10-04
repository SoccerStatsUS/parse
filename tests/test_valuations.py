import pytest

from parse.valuations import process_valuations


FORBES = """
Competition: Major League Soccer
Publisher: Forbes
Season: 2018
Published: 2018-11-14
Revenue season: 2017
Source: https://a.example https://b.example
* a comment
Key: rank; team; value; revenue; operating income

1; Atlanta United; 330000000; 47000000; -2000000
4; LAFC; 305000000; ; 
"""

SPORTICO = """
Competition: Major League Soccer
Publisher: Sportico
Season: 2021
Source: https://c.example
Key: rank; team; value

1; Los Angeles FC; 860000000
"""


def run(tmp_path, text):
    (tmp_path / 'list').write_text(text)
    return process_valuations('list', str(tmp_path))


def test_full_row(tmp_path):
    assert run(tmp_path, FORBES)[0] == {
        'team': 'Atlanta United', 'rank': 1, 'value': 330000000, 'revenue': 47000000,
        'operating_income': -2000000, 'competition': 'Major League Soccer', 'publisher': 'Forbes',
        'season': '2018', 'published': '2018-11-14', 'revenue_season': '2017',
        'sources': ['https://a.example', 'https://b.example'],
    }


def test_figures_not_given_are_none(tmp_path):
    row = run(tmp_path, FORBES)[1]
    assert row['revenue'] is None and row['operating_income'] is None


def test_a_list_without_revenue_columns(tmp_path):
    (row,) = run(tmp_path, SPORTICO)
    assert row['revenue'] is None and row['operating_income'] is None
    assert row['published'] is None and row['revenue_season'] is None


def test_wrong_field_count_names_the_line(tmp_path):
    with pytest.raises(ValueError, match=r'list:9'):
        run(tmp_path, SPORTICO + "2; LA Galaxy\n")
