# ROADMAP.md — Development Roadmap

Open work only; completed items are removed as they land (see git history).

`tests/test_games.py::test_forfeit` fails on purpose — it encodes the Group/Round item
below. Don't relax the assertion; it goes green when the parser is fixed.

---

## Parser Correctness

- [ ] `Group:` header wipes `Round:` (`parse/games.py:257`) — both orderings appear in the corpus; covered by `test_forfeit`
- [ ] `neutral` left in the location field (`parse/games.py:715`) — can't just clear it, `format_game` never writes `g['neutral']`
- [ ] 14 live `pdb.set_trace()` calls in `parse/games.py` — halt batch runs; skip or raise per the 2026-07 cleanup commits
- [ ] Unrecognized lines fall through to the goal-list parser (`parse/games.py:447`) — section headers like `1. round` land in goal objects

- [ ] `RosterProcessor` references an undefined `name` (`parse/rosters.py:155`) — every player line raises `NameError`, so v1 is dead
- [ ] `fix_roster_name` only capitalizes after a space (`parse/rosters.py:59`) — gives `O'brien`, `Jean-pierre`, and lowercases accented initials via `char_dict`
- [ ] `RosterProcessor3` doesn't strip `Team:` or `BlockSource:` (`parse/rosters.py:258,277`) — unlike `Competition:`/`Season:`, so values keep a leading space

## Goal Normalization

- [ ] No `penalty` / `own_goal` / `own_goal_player` / `unassisted` fields — `pk` and own-goal scorers sit in `assists` as raw strings

## Test Coverage

- [ ] No tests for `parse/stats.py`
- [ ] No tests for `parse/transactions.py`
- [ ] No tests for `parse/export.py`
- [ ] No export/round-trip tests beyond `test_home_team_export_round_trip`
- [ ] Shootout parsing untested
- [ ] Standings has one test against one fixture — no alternate delimiters, `Region:`/`Zone:` headers, or malformed rows
