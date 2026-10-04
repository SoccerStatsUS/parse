import pytest

from parse.ownership import process_ownership


SALES = """
Competition: Major League Soccer
Key: club; year; seller; buyer; stake; price; valuation; note; sources

Chicago Fire; 2019; Andrew Hauptman; Joe Mansueto; 51%; 204000000; 400000000; ; https://a.example
Colorado Rapids; 2003; AEG; Kroenke Sports Enterprises; ; ; ; terms not found; https://b.example https://c.example
"""

FEES = """
Competition: Major League Soccer
Key: club; awarded; first season; fee; note; sources

San Diego FC; 2023; 2025; 500000000; ; https://d.example
"""


def run(tmp_path, text):
    (tmp_path / 'f').write_text(text)
    return process_ownership('f', str(tmp_path))


def test_sale(tmp_path):
    assert run(tmp_path, SALES)[0] == {
        'club': 'Chicago Fire', 'year': 2019, 'seller': 'Andrew Hauptman', 'buyer': 'Joe Mansueto',
        'stake': '51%', 'price': 204000000, 'valuation': 400000000, 'note': '',
        'sources': ['https://a.example'], 'competition': 'Major League Soccer',
    }


def test_missing_figures_are_none(tmp_path):
    row = run(tmp_path, SALES)[1]
    assert row['price'] is None and row['valuation'] is None and row['stake'] is None
    assert row['note'] == 'terms not found'
    assert len(row['sources']) == 2


def test_keys_with_spaces_become_underscores(tmp_path):
    (row,) = run(tmp_path, FEES)
    assert row['first_season'] == 2025 and row['fee'] == 500000000


def test_wrong_field_count_names_the_line(tmp_path):
    with pytest.raises(ValueError, match=r'f:6'):
        run(tmp_path, FEES + "Austin FC; 2019\n")
