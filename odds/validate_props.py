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

MIN_TOTAL_ROWS = 1000
MIN_DK_ROWS = 1000
MIN_FD_ROWS = 25


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
        errors.append(
            f"Duplicate rows: {duplicates}"
        )

    market_counts = Counter(
        row["market"]
        for row in rows
    )

    sportsbook_counts = Counter(
        row["sportsbook"]
        for row in rows
    )

    print()
    print("Sportsbooks:")

    for book, count in sorted(
        sportsbook_counts.items()
    ):
        print(f"  {book}: {count}")

    print()
    print("Markets:")

    for market, count in sorted(
        market_counts.items()
    ):
        print(f"  {market}: {count}")

    if set(sportsbook_counts) != ALLOWED_SPORTSBOOKS:
        errors.append(
            "Expected both DraftKings and FanDuel."
        )

    dk_rows = sportsbook_counts.get(
        "DraftKings",
        0
    )

    fd_rows = sportsbook_counts.get(
        "FanDuel",
        0
    )

    if len(rows) < MIN_TOTAL_ROWS:
        errors.append(
            f"Suspiciously few total rows: {len(rows)} "
            f"(minimum {MIN_TOTAL_ROWS})"
        )

    if dk_rows < MIN_DK_ROWS:
        errors.append(
            f"Suspiciously few DraftKings rows: {dk_rows} "
            f"(minimum {MIN_DK_ROWS})"
        )

    if fd_rows < MIN_FD_ROWS:
        errors.append(
            f"Suspiciously few FanDuel rows: {fd_rows} "
            f"(minimum {MIN_FD_ROWS})"
        )

    core_markets = {
        "Passing Yards",
        "Receiving Yards",
        "Receptions",
        "Rushing Yards",
    }

    for market in core_markets:

        count = market_counts.get(
            market,
            0
        )

        if count == 0:
            errors.append(
                f"Missing core market: {market}"
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
        "sportsbooks": dict(
            sorted(sportsbook_counts.items())
        ),
        "markets": dict(
            sorted(market_counts.items())
        ),
        "duplicates": 0,
        "core_markets_present": sorted(core_markets),
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
    print("DraftKings:", dk_rows)
    print("FanDuel:", fd_rows)
    print("Summary:", SUMMARY_FILE)
    print("=" * 60)


if __name__ == "__main__":
    main()
