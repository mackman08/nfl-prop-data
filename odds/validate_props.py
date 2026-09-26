import csv
import re
import sys
from collections import Counter


INPUT_FILE = "odds/nfl_player_props_latest.csv"

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


def fail(message):
    print("FAIL:", message)
    sys.exit(1)


def main():
    print("=" * 60)
    print("NFL PLAYER PROP CSV VALIDATION")
    print("=" * 60)

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames

    if columns != EXPECTED_COLUMNS:
        fail(f"Unexpected columns: {columns}")

    if not rows:
        fail("CSV contains no data rows.")

    print("Rows:", len(rows))

    # --------------------------------------------------------
    # Basic field validation
    # --------------------------------------------------------

    errors = []

    for i, row in enumerate(rows, start=2):

        if not row["player"].strip():
            errors.append(f"Line {i}: blank player")

        if not row["market"].strip():
            errors.append(f"Line {i}: blank market")

        if not row["line"].strip():
            errors.append(f"Line {i}: blank line")

        if not row["sportsbook"].strip():
            errors.append(f"Line {i}: blank sportsbook")

        if not row["game"].strip():
            errors.append(f"Line {i}: blank game")

        if not row["event_id"].strip():
            errors.append(f"Line {i}: blank event_id")

        # Player name pollution
        player = row["player"].strip()

        for suffix in BAD_PLAYER_SUFFIXES:

            if player.endswith(" " + suffix):
                errors.append(
                    f"Line {i}: polluted player name: {player}"
                )
                break

        # Market validation
        if row["market"] not in ALLOWED_MARKETS:
            errors.append(
                f"Line {i}: invalid market: {row['market']}"
            )

        # Sportsbook validation
        if row["sportsbook"] not in ALLOWED_SPORTSBOOKS:
            errors.append(
                f"Line {i}: invalid sportsbook: {row['sportsbook']}"
            )

        # Numeric line validation
        try:
            float(row["line"])
        except ValueError:
            errors.append(
                f"Line {i}: invalid line: {row['line']}"
            )

        # Odds validation
        for field in ["over_odds", "under_odds"]:

            value = row[field].strip()

            if value:
                try:
                    int(value)
                except ValueError:
                    errors.append(
                        f"Line {i}: invalid {field}: {value}"
                    )

    # --------------------------------------------------------
    # Duplicate validation
    # --------------------------------------------------------

    seen = set()
    duplicates = 0

    for row in rows:

        key = tuple(
            row[column]
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

    # --------------------------------------------------------
    # Market / sportsbook summary
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Structural sanity checks
    # --------------------------------------------------------

    if set(sportsbook_counts) != ALLOWED_SPORTSBOOKS:
        errors.append(
            "Expected both DraftKings and FanDuel."
        )

    if len(rows) < 1000:
        errors.append(
            f"Suspiciously few rows: {len(rows)}"
        )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

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

    print()
    print("=" * 60)
    print("VALIDATION PASSED")
    print("Rows:", len(rows))
    print("Duplicates: 0")
    print("Blank required fields: 0")
    print("Invalid markets: 0")
    print("Invalid sportsbooks: 0")
    print("Invalid player names: 0")
    print("Invalid numeric values: 0")
    print("=" * 60)


if __name__ == "__main__":
    main()
