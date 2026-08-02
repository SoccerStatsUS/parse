import datetime

from parse.transactions import TransactionProcessor, remove_pairs


def run(text, **kw):
    """Feed a fixture through a processor line by line."""
    tp = TransactionProcessor(**kw)
    for line in text.strip().split('\n'):
        tp.process_line(line)
    return tp


BASIC = """
Competition: Major League Soccer
Season: 1995
Key: date; type; person; team_to; team_from
* a comment

1/15/1997; sign; Jaime Moreno; DC United; Bolivia
"""


def test_remove_pairs():
    assert remove_pairs('Bob (on loan) Smith', '(', ')') == 'Bob  Smith'
    assert remove_pairs('Bob Smith', '(', ')') == 'Bob Smith'
    assert remove_pairs('Bob [x] Smith', '[', ']') == 'Bob  Smith'


def test_basic_transaction():
    data = run(BASIC).data
    assert len(data) == 1
    assert data[0]['date'] == datetime.datetime(1997, 1, 15)
    assert data[0]['sources'] == []


def test_skips_blank_and_comment_lines():
    assert len(run(BASIC).data) == 1


def test_missing_date_is_none():
    text = 'Key: date; type; person; team_to\n; allocation; Marcelo Balboa; Colorado Rapids'
    assert run(text).data[0]['date'] == None


TRADE = """
Key: date; type; person; team_to
7/3/1997; trade; Steve Rammel, Roy Wegerle; Colorado Rapids, DC United
"""


def test_trade_splits_into_one_row_per_player():
    """person and team_to are parallel comma-separated lists."""
    data = run(TRADE).data
    assert len(data) == 2
    assert [d['ttype'] for d in data] == ['trade', 'trade']
    assert [d['date'] for d in data] == [datetime.datetime(1997, 7, 3)] * 2
    assert [d['person'] for d in data] == ['Steve Rammel', 'Roy Wegerle']
    assert [d['team_to'] for d in data] == ['Colorado Rapids', 'DC United']


def test_trade_omits_team_from():
    """Unlike every other type, trade rows carry no team_from key at all."""
    assert 'team_from' not in run(TRADE).data[0]


def test_source_and_notes_attach_to_previous_row():
    text = 'Key: date; type; person\n; sign; Bob\nSource: rsssf.com\nNotes: a note'
    d = run(text).data[0]
    assert d['sources'] == ['rsssf.com']
    assert d['notes'] == 'a note'


def test_strips_field_values():
    """Nothing is stripped, so every field keeps the space after its delimiter."""
    d = run(BASIC).data[0]
    assert d['ttype'] == 'sign'
    assert d['person'] == 'Jaime Moreno'
    assert d['team_to'] == 'DC United'
    assert d['team_from'] == 'Bolivia'


def test_strips_blocksource():
    text = 'BlockSource: rsssf.com\nKey: date; type; person\n; sign; Bob'
    assert run(text).data[0]['sources'] == ['rsssf.com']


