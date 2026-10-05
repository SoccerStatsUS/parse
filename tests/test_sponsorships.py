import pytest

from parse.sponsorships import process_sponsorships


DEALS = """
Competition: Major League Soccer
Kind: stadium naming rights
Key: club; sponsor; property; start; end; length; annual; total; currency; note; sources
* a comment

LAFC; BMO; BMO Stadium; 2023; 2032; ; 10000000; 100000000; USD; ten years; https://a.example https://b.example
Austin FC; Q2; Q2 Stadium; 2021; ; 15; ; ; USD; ; https://c.example
; Adidas; kit supplier; 2005; 2014; ; ; 150000000; USD; ; https://d.example
"""


def run(tmp_path, text):
    (tmp_path / 'deals').write_text(text)
    return process_sponsorships('deals', str(tmp_path))


def test_full_row(tmp_path):
    assert run(tmp_path, DEALS)[0] == {
        'club': 'LAFC', 'sponsor': 'BMO', 'property': 'BMO Stadium',
        'start': 2023, 'end': 2032, 'length': None, 'annual': 10000000, 'total': 100000000,
        'currency': 'USD', 'note': 'ten years',
        'sources': ['https://a.example', 'https://b.example'],
        'competition': 'Major League Soccer', 'kind': 'stadium naming rights',
    }


def test_empty_fields_are_none(tmp_path):
    row = run(tmp_path, DEALS)[1]
    assert row['end'] is None and row['annual'] is None and row['total'] is None
    assert row['note'] == ''
    assert row['length'] == 15


def test_a_league_deal_has_no_club(tmp_path):
    assert run(tmp_path, DEALS)[2]['club'] is None


def test_wrong_field_count_names_the_line(tmp_path):
    with pytest.raises(ValueError, match=r'deals:10'):
        run(tmp_path, DEALS + "LAFC; BMO; shirt; 2024\n")
