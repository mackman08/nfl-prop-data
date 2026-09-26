import csv
import os
from oddswrap import OddsClient

OUTPUT_FILE = "odds/nfl_player_props_latest.csv"
BOOKS = ["draftkings", "fanduel"]

DK_MARKETS = {
    "16571": "Rushing Yards",
    "16570": "Receiving Yards",
    "16821": "Receptions",
    "16569": "Passing Yards",
    "16572": "Rush + Receiving Yards",
}

FD_MARKETS = {
    "Rushing Yds": "Rushing Yards",
    "Alt Rushing Yds": "Alt Rushing Yards",
    "Receiving Yds": "Receiving Yards",
    "Alt Receiving Yds": "Alt Receiving Yards",
    "Total Receptions": "Receptions",
    "Alt Receptions": "Alt Receptions",
    "Passing Yds": "Passing Yards",
    "Alt Passing Yds": "Alt Passing Yards",
    "Rush + Rec Yds": "Rush + Receiving Yards",
    "Alt Rush + Rec Yds": "Alt Rush + Receiving Yards",
}


def collect_draftkings(client):
    rows = []

    categories = client.get_prop_categories(
        "nfl",
        book="draftkings"
    )

    for category in categories:

        if category.category_id not in [
            "1000",
            "1001",
            "1342"
        ]:
            continue

        subcategory_id = str(category.subcategory_id)
        subcategory_name = str(category.subcategory_name)

        market_name = None

        if subcategory_id in DK_MARKETS:
            market_name = DK_MARKETS[subcategory_id]

        elif (
            "Alt " in subcategory_name
            and (
                "Rushing Yards" in subcategory_name
                or "Receiving Yards" in subcategory_name
                or "Receptions" in subcategory_name
                or "Passing Yards" in subcategory_name
                or "Rush + Receiving Yards" in subcategory_name
            )
        ):
            market_name = subcategory_name

        if market_name is None:
            continue

        print("DK:", market_name)

        try:
            props = client.get_props(
                "nfl",
                category_id=category.category_id,
                subcategory_id=category.subcategory_id,
                book="draftkings"
            )

            for prop in props:
                rows.append({
                    "player": prop.player,
                    "market": market_name,
                    "line": prop.line,
                    "over_odds": prop.over_odds,
                    "under_odds": prop.under_odds,
                    "sportsbook": "DraftKings",
                    "game": prop.game,
                    "event_id": prop.event_id,
                })

        except Exception as e:
            print("WARNING: DK market failed:", market_name, e)

    return rows


def collect_fanduel(client):
    rows = []

    categories = client.get_prop_categories(
        "nfl",
        book="fanduel"
    )

    for category in categories:

        if category.category_id != "popular":
            continue

        name = str(category.subcategory_name)

        market_name = None

        for keyword, normalized in FD_MARKETS.items():
            if keyword in name:
                market_name = normalized
                break

        if market_name is None:
            continue

        if name in [
            "Most Rushing Yards",
            "Most Passing Yards",
            "Any Time Touchdown Scorer",
            "First Touchdown Scorer",
            "Last Touchdown Scorer",
        ]:
            continue

        print("FD:", name)

        try:
            props = client.get_props(
                "nfl",
                category_id="popular",
                subcategory_id=category.subcategory_id,
                book="fanduel"
            )

            for prop in props:
                rows.append({
                    "player": prop.player,
                    "market": market_name,
                    "line": prop.line,
                    "over_odds": prop.over_odds,
                    "under_odds": prop.under_odds,
                    "sportsbook": "FanDuel",
                    "game": prop.game,
                    "event_id": prop.event_id,
                })

        except Exception as e:
            print("WARNING: FD market failed:", name, e)

    return rows


def remove_duplicates(rows):
    unique = {}

    for row in rows:
        key = (
            row["player"],
            row["market"],
            row["line"],
            row["sportsbook"],
            row["game"]
        )

        unique[key] = row

    return list(unique.values())


def save_csv(rows):
    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    fields = [
        "player",
        "market",
        "line",
        "over_odds",
        "under_odds",
        "sportsbook",
        "game",
        "event_id"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fields
        )

        writer.writeheader()
        writer.writerows(rows)


def main():

    print("=" * 60)
    print("NFL PLAYER PROP COLLECTOR")
    print("DraftKings + FanDuel")
    print("Standard + Alternate Lines")
    print("=" * 60)

    client = OddsClient(
        books=BOOKS
    )

    rows = []

    print()
    print("Collecting DraftKings...")
    rows.extend(
        collect_draftkings(client)
    )

    print()
    print("Collecting FanDuel...")
    rows.extend(
        collect_fanduel(client)
    )

    rows = remove_duplicates(rows)

    save_csv(rows)

    print()
    print("=" * 60)
    print("COLLECTION COMPLETE")
    print("TOTAL PROPS:", len(rows))
    print("OUTPUT:", OUTPUT_FILE)
    print("=" * 60)


if __name__ == "__main__":
    main()

