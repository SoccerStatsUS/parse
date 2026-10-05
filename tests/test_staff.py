import pytest

from parse.staff import process_staff


STAFF = """
Organization: United States Soccer Federation
* a comment
Key: year; name; role; pay; related; other; sources

2024; Mauricio Pochettino; Mnt Head Coach; 5016917; 0; 11788; https://a.example
"""

REPORTED = """
Organization: Major League Soccer
Coverage: reported
Key: year; name; role; pay; related; other; sources

2014; Don Garber; Commissioner; 5000000; ; ; https://b.example
"""


def run(tmp_path, text):
    (tmp_path / 'org').write_text(text)
    return process_staff('org', str(tmp_path))


def test_full_row(tmp_path):
    assert run(tmp_path, STAFF)[0] == {
        'year': 2024, 'name': 'Mauricio Pochettino', 'role': 'Mnt Head Coach', 'pay': 5016917,
        'related': 0, 'other': 11788, 'sources': ['https://a.example'],
        'organization': 'United States Soccer Federation', 'coverage': 'full',
    }


def test_a_reported_figure_leaves_the_rest_empty(tmp_path):
    row = run(tmp_path, REPORTED)[0]
    assert row['coverage'] == 'reported' and row['related'] is None and row['other'] is None


def test_a_short_line_names_the_line(tmp_path):
    with pytest.raises(ValueError, match=':6:'):
        run(tmp_path, STAFF.replace('Mnt Head Coach;', 'Mnt Head Coach'))
