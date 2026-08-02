# ROADMAP.md — Development Roadmap

Open work only; completed items are removed as they land (see git history).

**Note:** `tests/test_games.py::test_forfeit` and `tests/test_games.py::test_basic_game`
fail on purpose — they encode the intended behavior described under Parser Correctness
below. Do not "fix" them by relaxing the assertions; they go green when the parser is
fixed. Current suite: 9 passing, 2 failing.

---

## Parser Correctness

- [ ] `Group:` header wipes `Round:` (`parse/games.py:257`) — the header hierarchy is
  Stage > Group > Round > Leg and each level clears the finer ones, but the corpus uses
  both orderings about equally, so a `Round:` written before its `Group:` is destroyed.
  A 2026-08 sweep found 1193 affected sites (vs 1355 in the safe Group-then-Round order);
  e.g. `international_data/games/world/olympics/2012:5` has `Round: Preliminary` followed
  by `Group: A` and loses "Preliminary". Fix is dropping `self.round =` from the
  assignment on line 257 — but that means a new `Group:` no longer resets a stale round,
  which some files may rely on. Covered by `test_forfeit`.

- [ ] Location field retains a team name (`parse/games.py:706`) — when the location field
  holds a team name the parser sets `home_team` but leaves `location` set to that same
  team name, so team names end up in venue data. The adjacent `home`/`away` branches
  (lines 709/711) clear `location` to `None`; this branch does not. Affects 6643 of 89796
  game lines with a location field. Note `test_basic_game` expects `''` while the
  home/away branches produce `None` — pick one when fixing.

## Goal Normalization

- [ ] Penalties and own goals are not normalized — `pk` lands in `assists` as a literal
  string, and for own goals the scoring player lands in `assists` with `goal` set to the
  sentinel `'Own Goal'`. There are no `penalty`, `own_goal`, `own_goal_player`, or
  `unassisted` fields. `test_basic_goals` originally asserted all four (alongside
  contradictory assertions of the actual behavior, plus commented-out
  `#assert goals[2]['penalty_kick']` lines); its assertions now match what the parser
  really does. Doing this properly means deciding whether `assists` stays raw and the
  flags are derived, or whether the flags are extracted and `assists` holds only real
  assists.

## Test Coverage

- [ ] No tests for `parse/stats.py`, `parse/rosters.py`, `parse/transactions.py`, or
  `parse/export.py` — only `games.py` and `standings.py` are covered
- [ ] No export/round-trip tests — `tests/games/export.py` was an empty skeleton from the
  2013 commit and was deleted in the pytest port
- [ ] Shootout parsing is untested (noted as a TODO in the original `MINUTES` fixture)
- [ ] Standings coverage is one test against one fixture; no tests for alternate
  delimiters, the `Region:`/`Zone:` group headers, or malformed rows

## Deferred

- Porting the suite back to a runner other than pytest — the 2013 suite used `nose`,
  which has been unmaintained since 2015 and does not import on Python 3.10+
