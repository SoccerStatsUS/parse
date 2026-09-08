# ROADMAP.md — Development Roadmap

Open work only; completed items are removed as they land (see git history).

`tests/test_games.py::test_group_header_does_not_clear_round` fails on purpose — it encodes
the Group/Round item below. Don't relax the assertion; it goes green when the parser is fixed.

---

## Parser Correctness

- [ ] `Group:` header wipes `Round:` (`parse/games.py:257`) — 815 corpus sites are header blocks where both apply, 425 have games in between; covered by `test_group_header_does_not_clear_round`
- [ ] `neutral` left in the location field (`parse/games.py:715`) — can't just clear it, `format_game` never writes `g['neutral']`
- [ ] 16 live `pdb.set_trace()` calls in `parse/games.py` — halt batch runs; skip or raise per the 2026-07 cleanup commits
- [ ] Unrecognized lines fall through to the goal-list parser (`parse/games.py:455`) — section headers like `1. round` land in goal objects, and so does any lineup line whose team matches neither side of the current game
- [ ] A `*`-commented game line orphans its own detail lines (`parse/games.py:174`) — the comment check returns before `current_game` advances, so the goals, lineups, notes and source beneath it attach to the *previous* game. Only a lineup naming a team absent from that game warns, and then via the goal-list fallback; goals split cleanly and land silently. Corpus-wide there are 9 such blocks, 7 of them an orphaned `Source:` only. `usd1_data/data/games/asl/1929:396` was one and is fixed; it had given the 10/6/1929 game 12 goals against a recorded 6-2. `usd1_data/data/games/asl/1931:181` is still live — `Jimmy Slaven 56;` under a commented game line, no warning at all.

- [ ] Reformat `international_data/rosters/copa_america` for `RosterProcessor3` — no `Key:` line, so `load.py:1160` drops to pdb

- [ ] Undated transactions have no temporal anchor — 41 of 2892 rows (1995 allocations, 2013 retirements); `Season:` is parsed but never reaches the dict, and 6 dated rows contradict their file's season
- [ ] `usd1_data/data/transactions/mls/team/` is unformatted — `Team:`/`Date:` headers the parser doesn't know, 3 files key on `teams`, 5 have no `Key:`; 2018–2019 load nowhere
- [ ] DECIDE: should stats keep `position` and `points`? `parse/stats.py:174` blanks both unconditionally, discarding the real columns in the 2012 and 2016 files; the identical line sits commented out at `rosters.py:348`. Untested until decided
- [ ] Rewrite `Key:` lines in `usd1_data/data/stats/mls/2017`–`2019` — raw scrape headers yield 0 rows; ~1892 recoverable, then widen the `range(2012, 2017)` loop in `load.py`

## Goal Normalization

- [ ] No `penalty` / `own_goal` / `own_goal_player` / `unassisted` fields — `pk` and own-goal scorers sit in `assists` as raw strings

## Test Coverage

- [ ] No tests for `parse/export.py`
- [ ] No export/round-trip tests beyond `test_home_team_export_round_trip`
- [ ] Shootout parsing untested
- [ ] Standings has one test against one fixture — no alternate delimiters, `Region:`/`Zone:` headers, or malformed rows

## Deferred

- Three-team trades have no `team_from` — one row, and the file does not say which team sent whom
