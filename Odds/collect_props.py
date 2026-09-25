import csv
import json
import os
import sys
from datetime import datetime, timezone

# OddsWrap
try:
    from oddswrap import Odds
except ImportError:
    print("ERROR: oddswrap is not installed.")
    sys.exit(1)


OUTPUT_FILE = "nfl_player_props_latest.csv"

SPORTSBOOKS = {
    "draftkings",
    "fanduel",
}


def normalize(value):
    if value is None:
        return ""
    return str(value).strip()


def main():
    print("Starting NFL player-prop collection...")
    print("Sportsbooks: DraftKings + FanDuel")

    odds = Odds()

    # Get NFL player props
    props = odds.player_props(
        sport="nfl",
        sportsbooks=list(SPORTSBOOKS)
    )

    rows = []

    for prop in props:
        sportsbook = normalize(getattr(prop, "sportsbook", ""))

        if sportsbook.lower() not in SPORTSBOOKS:
            continue

        rows.append({
            "game_date": normalize(getattr(prop, "game_date", "")),
            "player": normalize(getattr(prop, "player", "")),
            "team": normalize(getattr(prop, "team", "")),
            "opponent": normalize(getattr(prop, "opponent", "")),
            "market": normalize(getattr(prop, "market", "")),
            "line": normalize(getattr(prop, "line", "")),
            "over_odds": normalize(getattr(prop, "over_odds", "")),
            "under_odds": normalize(getattr(prop, "under_odds", "")),
            "sportsbook": sportsbook,
        })

    # Remove duplicate rows
    unique_rows = []
    seen = set()

    for row in rows:
        key = tuple(row.values())

        if key not in seen:
            seen.add(key)
            unique_rows.append(row)

    fieldnames = [
        "game_date",
        "player",
        "team",
        "opponent",
        "market",
        "line",
        "over_odds",
        "under_odds",
        "sportsbook",
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_rows)

    print(f"Collected {len(unique_rows)} player-prop rows.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
