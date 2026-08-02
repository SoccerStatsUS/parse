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

- [ ] Reformat `international_data/rosters/copa_america` for `RosterProcessor3` — no `Key:` line, so `load.py:1160` drops to pdb

- [ ] Undated transactions have no temporal anchor — 41 of 2892 rows (1995 allocations, 2013 retirements); `Season:` is parsed but never reaches the dict, and 6 dated rows contradict their file's season
- [ ] `usd1_data/data/transactions/mls/team/` is unformatted — `Team:`/`Date:` headers the parser doesn't know, 3 files key on `teams`, 5 have no `Key:`; 2018–2019 load nowhere
- [ ] `StatsProcessor` strips nothing (`parse/stats.py:106,84,103`) — same fix already applied to rosters and transactions; leaves tabs in the 2017 stats file
- [ ] `d['position'] = d['points'] = ''` clobbers real columns (`parse/stats.py:174`) — the identical line is commented out in `rosters.py`
- [ ] Rewrite `Key:` lines in `usd1_data/data/stats/mls/2017`–`2019` — raw scrape headers yield 0 rows; ~1892 recoverable, then widen the `range(2012, 2017)` loop in `load.py`
- [ ] Trade rows omit `team_from` (`parse/transactions.py:146`) — other types carry it as `None`; no source file has the column and 3-team trades make it underivable

## Goal Normalization

- [ ] No `penalty` / `own_goal` / `own_goal_player` / `unassisted` fields — `pk` and own-goal scorers sit in `assists` as raw strings

## Test Coverage

- [ ] No tests for `parse/export.py`
- [ ] No export/round-trip tests beyond `test_home_team_export_round_trip`
- [ ] Shootout parsing untested
- [ ] Standings has one test against one fixture — no alternate delimiters, `Region:`/`Zone:` headers, or malformed rows
