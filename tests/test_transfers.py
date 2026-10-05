import pytest

from parse.transfers import process_transfers


SEASON = """
Competition: Major League Soccer
Season: 2025
* a comment
Key: direction; player; from; to; fee; ceiling; currency; kind; reported; sources

in; Emmanuel Latte Lath; Middlesbrough; Atlanta United; 22000000; ; USD; transfer; 2025-02-04; https://a.example
within; Jack McGlynn; Philadelphia Union; Houston Dynamo; 2100000; 3400000; USD; transfer; 2025-02-03; https://b.example https://c.example
out; Cade Cowell; San Jose Earthquakes; ; 5000000; ; ; bid; 2024-01-10; https://d.example
"""


def run(tmp_path, text):
    (tmp_path / 'season').write_text(text)
    return process_transfers('season', str(tmp_path))


def test_full_row(tmp_path):
    assert run(tmp_path, SEASON)[0] == {
        'name': 'Emmanuel Latte Lath', 'from': 'Middlesbrough', 'to': 'Atlanta United',
        'direction': 'in', 'fee': 22000000, 'ceiling': None, 'currency': 'USD',
        'kind': 'transfer', 'reported': '2025-02-04', 'sources': ['https://a.example'],
        'competition': 'Major League Soccer', 'season': '2025',
    }


def test_ceiling_and_several_sources(tmp_path):
    row = run(tmp_path, SEASON)[1]
    assert (row['fee'], row['ceiling']) == (2100000, 3400000)
    assert row['sources'] == ['https://b.example', 'https://c.example']


def test_a_bid_from_an_unnamed_club_defaults_currency(tmp_path):
    row = run(tmp_path, SEASON)[2]
    assert row['to'] == '' and row['currency'] == 'USD' and row['kind'] == 'bid'


def test_bad_lines_name_the_line(tmp_path):
    with pytest.raises(ValueError, match=':7:'):
        run(tmp_path, SEASON.replace('Atlanta United; 22000000', 'Atlanta United 22000000'))
    with pytest.raises(ValueError, match='unknown direction'):
        run(tmp_path, SEASON.replace('in; Emmanuel', 'loan; Emmanuel'))
