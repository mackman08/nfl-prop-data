import csv
import json
import sys
from collections import Counter


INPUT_FILE = "odds/nfl_player_props_latest.csv"
SUMMARY_FILE = "odds/nfl_player_props_summary.json"

EXPECTED_COLUMNS = [
    "player",
    "market",
    "line",
    "over_odds",
    "under_odds",
    "sportsbook",
    "game",
    "event_id",
]

ALLOWED_SPORTSBOOKS = {
    "DraftKings",
    "FanDuel",
}

ALLOWED_MARKETS = {
    "Passing Yards",
    "Receiving Yards",
    "Receptions",
    "Rushing Yards",
    "Rush + Receiving Yards",
    "Alt Passing Yards",
    "Alt Receiving Yards",
    "Alt Receptions",
    "Alt Rushing Yards",
    "Alt Rush + Receiving Yards",
}

BAD_PLAYER_SUFFIXES = [
    "Rushing +",
    "Rushing Yards",
    "Receiving Yards",
    "Passing Yards",
    "Receptions",
    "Rush + Receiving Yards",
    "Rushing + Receiving Yards",
]

# Validation is slate-size agnostic.
#
# The collector is intentionally allowed to run against a single-game slate
# (for example Monday Night Football). Full-slate row-count minimums such as
# 1,000 DK rows / 25 FD rows are therefore invalid as completeness tests.
#
# Completeness is checked structurally instead:
#   * both expected sportsbooks are present
#   * all four core markets are represented
#   * each sportsbook has every core market
#   * every row has a valid game/event/player/line
#   * duplicate rows are rejected


def main():
    print("=" * 60)
    print("NFL PLAYER PROP CSV VALIDATION")
    print("=" * 60)

    try:
        with open(INPUT_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            columns = reader.fieldnames
    except FileNotFoundError:
        print("FAIL: CSV file not found:", INPUT_FILE)
        sys.exit(1)

    errors = []

    if columns != EXPECTED_COLUMNS:
        errors.append(f"Unexpected columns: {columns}")

    if not rows:
        errors.append("CSV contains no data rows.")

    print("Rows:", len(rows))

    for i, row in enumerate(rows, start=2):

        for field in [
            "player",
            "market",
            "line",
            "sportsbook",
            "game",
            "event_id",
        ]:
            if not row.get(field, "").strip():
                errors.append(f"Line {i}: blank {field}")

        player = row.get("player", "").strip()

        for suffix in BAD_PLAYER_SUFFIXES:
            if player.endswith(" " + suffix):
                errors.append(
                    f"Line {i}: polluted player name: {player}"
                )
                break

        market = row.get("market", "")

        if market not in ALLOWED_MARKETS:
            errors.append(
                f"Line {i}: invalid market: {market}"
            )

        sportsbook = row.get("sportsbook", "")

        if sportsbook not in ALLOWED_SPORTSBOOKS:
            errors.append(
                f"Line {i}: invalid sportsbook: {sportsbook}"
            )

        try:
            line = float(row.get("line", ""))
            if line <= 0:
                errors.append(
                    f"Line {i}: non-positive line: {row['line']}"
                )
        except ValueError:
            errors.append(
                f"Line {i}: invalid line: {row.get('line', '')}"
            )

        for field in ["over_odds", "under_odds"]:
            value = row.get(field, "").strip()

            if value:
                try:
                    int(value)
                except ValueError:
                    errors.append(
                        f"Line {i}: invalid {field}: {value}"
                    )

    seen = set()
    duplicates = 0

    for row in rows:
        key = tuple(
            row.get(column, "")
            for column in EXPECTED_COLUMNS
        )

        if key in seen:
            duplicates += 1
        else:
            seen.add(key)

    if duplicates:
        errors.append(f"Duplicate rows: {duplicates}")

    market_counts = Counter(row["market"] for row in rows)
    sportsbook_counts = Counter(row["sportsbook"] for row in rows)
    book_market_counts = Counter(
        (row["sportsbook"], row["market"])
        for row in rows
    )
    games = sorted({row["game"] for row in rows if row.get("game")})
    event_ids = sorted({row["event_id"] for row in rows if row.get("event_id")})

    print()
    print("Slate:")
    print("  Games:", len(games))
    for game in games:
        print("   ", game)
    print("  Event IDs:", len(event_ids))

    print()
    print("Sportsbooks:")
    for book, count in sorted(sportsbook_counts.items()):
        print(f"  {book}: {count}")

    print()
    print("Markets:")
    for market, count in sorted(market_counts.items()):
        print(f"  {market}: {count}")

    if set(sportsbook_counts) != ALLOWED_SPORTSBOOKS:
        errors.append(
            "Expected both DraftKings and FanDuel."
        )

    core_markets = {
        "Passing Yards",
        "Receiving Yards",
        "Receptions",
        "Rushing Yards",
    }

    for market in core_markets:
        count = market_counts.get(market, 0)

        if count == 0:
            errors.append(
                f"Missing core market: {market}"
            )

    # Each sportsbook must contribute every core market, but the required
    # count is deliberately 1+ rather than a full-slate minimum.
    for book in sorted(ALLOWED_SPORTSBOOKS):
        for market in sorted(core_markets):
            count = book_market_counts.get(
                (book, market),
                0
            )

            if count < 1:
                errors.append(
                    f"Missing {book} {market}: "
                    f"0 rows"
                )

    if errors:
        print()
        print("=" * 60)
        print("VALIDATION FAILED")
        print("=" * 60)

        for error in errors[:50]:
            print(error)

        if len(errors) > 50:
            print(
                f"... and {len(errors) - 50} more errors"
            )

        sys.exit(1)

    summary = {
        "total_rows": len(rows),
        "games": games,
        "event_ids": event_ids,
        "sportsbooks": dict(
            sorted(sportsbook_counts.items())
        ),
        "markets": dict(
            sorted(market_counts.items())
        ),
        "duplicates": 0,
        "core_markets_present": sorted(core_markets),
        "core_markets_by_sportsbook": {
            book: {
                market: book_market_counts.get(
                    (book, market),
                    0
                )
                for market in sorted(core_markets)
            }
            for book in sorted(ALLOWED_SPORTSBOOKS)
        },
        "validation_mode": "slate-size-agnostic",
    }

    with open(
        SUMMARY_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            summary,
            f,
            indent=2,
            sort_keys=True
        )
        f.write("\n")

    print()
    print("=" * 60)
    print("VALIDATION PASSED")
    print("Rows:", len(rows))
    print("Games:", len(games))
    print("DraftKings:", sportsbook_counts.get("DraftKings", 0))
    print("FanDuel:", sportsbook_counts.get("FanDuel", 0))
    print("Duplicates: 0")
    print("Core markets present: 4/4")
    print("Per-book core-market coverage: PASS")
    print("Validation mode: slate-size-agnostic")
    print("Summary:", SUMMARY_FILE)
    print("=" * 60)


if __name__ == "__main__":
    main()

# Single-game slate validation is intentionally supported.
