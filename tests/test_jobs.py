import pytest

from parse.jobs import process_jobs


JOBS = """
Competition: Major League Soccer
* a comment
Key: club; name; role; title; start; end; sources

* Chicago Fire
Chicago Fire; Bob Bradley; head; Head Coach; 1997-10-30; 2002-12; https://a.example https://b.example
Chicago Fire; Peter Wilt; gm; General Manager; 1997; ; https://c.example
"""


def run(tmp_path, text):
    (tmp_path / 'mls').write_text(text)
    return process_jobs('mls', str(tmp_path))


def test_full_row(tmp_path):
    assert run(tmp_path, JOBS)[0] == {
        'club': 'Chicago Fire', 'name': 'Bob Bradley', 'role': 'head', 'title': 'Head Coach',
        'start': '1997-10-30', 'end': '2002-12',
        'sources': ['https://a.example', 'https://b.example'], 'competition': 'Major League Soccer',
    }


def test_an_empty_end_is_still_in_the_job(tmp_path):
    row = run(tmp_path, JOBS)[1]
    assert row['start'] == '1997' and row['end'] is None


def test_a_short_line_names_the_line(tmp_path):
    with pytest.raises(ValueError, match=':7:'):
        run(tmp_path, JOBS.replace('head; Head Coach;', 'head Head Coach;'))


def test_an_unknown_role_raises(tmp_path):
    with pytest.raises(ValueError, match='coach'):
        run(tmp_path, JOBS.replace('; head;', '; coach;'))


def test_a_date_in_another_format_raises(tmp_path):
    with pytest.raises(ValueError, match='10/30/1997'):
        run(tmp_path, JOBS.replace('1997-10-30', '10/30/1997'))
