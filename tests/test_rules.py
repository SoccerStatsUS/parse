import pytest

from parse.rules import process_rules


RULES = """
Competition: Major League Soccer
* a comment
Key: season; salary budget; maximum charge; senior minimum; designated players; sources

2015; 3490000; 436250; 60000; 3; https://a.example https://b.example
2010; 2550000; ; 40000; ; https://c.example
"""


def run(tmp_path, text):
    (tmp_path / 'mls').write_text(text)
    return process_rules('mls', str(tmp_path))


def test_full_row(tmp_path):
    assert run(tmp_path, RULES)[0] == {
        'season': '2015', 'salary_budget': 3490000, 'maximum_charge': 436250,
        'senior_minimum': 60000, 'designated_players': 3,
        'sources': ['https://a.example', 'https://b.example'],
        'competition': 'Major League Soccer',
    }


def test_empty_fields_are_none(tmp_path):
    row = run(tmp_path, RULES)[1]
    assert row['maximum_charge'] is None and row['designated_players'] is None


def test_a_short_line_names_the_line(tmp_path):
    with pytest.raises(ValueError, match=':7:'):
        run(tmp_path, RULES.replace('2010; 2550000; ;', '2010; 2550000;'))
