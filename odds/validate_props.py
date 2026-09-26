import csv
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

    # --------------------------------------------------------
    # Schema
    # --------------------------------------------------------

    if columns != EXPECTED_COLUMNS:
        errors.append(f"Unexpected columns: {columns}")

    if not rows:
        errors.append("CSV contains no data rows.")

    print("Rows:", len(rows))

    # --------------------------------------------------------
    # Row validation
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Duplicate validation
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Coverage summary
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
    # Coverage / partial-response protection
    # --------------------------------------------------------

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

    # Each core market should have meaningful coverage.
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
    print("DraftKings:", dk_rows)
    print("FanDuel:", fd_rows)
    print("Duplicates: 0")
    print("Core markets present: 4/4")
    print("=" * 60)


if __name__ == "__main__":
    main()
