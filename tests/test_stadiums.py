import pytest

from parse.stadiums import process_stadiums


STADIUMS = """
Competition: Major League Soccer
* a comment
Key: club; stadium; opened; kind; cost; public; currency; note; sources

Philadelphia Union; Subaru Park; 2010; built; 120000000; 77000000; USD; county and state; https://a.example https://b.example
Toronto FC; BMO Field; 2007; built; 62900000; ; CAD; ; https://c.example
"""


def run(tmp_path, text):
    (tmp_path / 'mls').write_text(text)
    return process_stadiums('mls', str(tmp_path))


def test_full_row(tmp_path):
    assert run(tmp_path, STADIUMS)[0] == {
        'club': 'Philadelphia Union', 'stadium': 'Subaru Park', 'opened': 2010, 'kind': 'built',
        'cost': 120000000, 'public': 77000000, 'currency': 'USD', 'note': 'county and state',
        'sources': ['https://a.example', 'https://b.example'], 'competition': 'Major League Soccer',
    }


def test_missing_public_money_is_none_not_zero(tmp_path):
    row = run(tmp_path, STADIUMS)[1]
    assert row['public'] is None and row['currency'] == 'CAD' and row['note'] == ''


def test_a_short_line_names_the_line(tmp_path):
    with pytest.raises(ValueError, match=':6:'):
        run(tmp_path, STADIUMS.replace('2010; built;', '2010 built;'))
