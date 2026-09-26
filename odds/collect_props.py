import csv
import os
import re
from oddswrap import OddsClient


OUTPUT_FILE = "odds/nfl_player_props_latest.csv"

BOOKS = ["draftkings", "fanduel"]


# ============================================================
# MARKETS WE WANT
# ============================================================

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


# ============================================================
# NORMALIZE DRAFTKINGS PLAYER NAME
# ============================================================

def normalize_dk_player(player, market):

    if not player:
        return player

    suffixes = [
        "Passing Yards",
        "Rushing Yards",
        "Receiving Yards",
        "Receptions",
        "Rush + Receiving Yards",
    ]

    cleaned = player.strip()

    for suffix in suffixes:

        if cleaned.endswith(" " + suffix):

            cleaned = cleaned[
                :-len(suffix) - 1
            ].strip()

            break

    return cleaned


# ============================================================
# NORMALIZE FANDUEL PLAYER / LINE
# ============================================================

def normalize_fd_prop(player, market):

    if not player:
        return player, None, None

    player = player.strip()

    # --------------------------------------------------------
    # Standard Over / Under
    # --------------------------------------------------------

    if player.endswith(" Over"):

        clean_player = player[:-5].strip()

        return clean_player, None, "over"

    if player.endswith(" Under"):

        clean_player = player[:-6].strip()

        return clean_player, None, "under"

    # --------------------------------------------------------
    # Threshold markets
    #
    # Examples:
    #
    # Derrick Henry 80+ Yards
    # CeeDee Lamb 7+ Receptions
    # Dak Prescott 275+ Yards
    #
    # --------------------------------------------------------

    match = re.match(
        r"^(.*?)\s+(\d+(?:\.\d+)?)\+\s+(Yards|Receptions)$",
        player
    )

    if match:

        clean_player = match.group(1).strip()

        threshold = float(
            match.group(2)
        )

        stat_type = match.group(3)

        # Receptions
        if stat_type == "Receptions":

            return (
                clean_player,
                threshold,
                "threshold"
            )

        # Yards
        return (
            clean_player,
            threshold,
            "threshold"
        )

    return player, None, None


# ============================================================
# DRAFTKINGS COLLECTOR
# ============================================================

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

        subcategory_id = str(
            category.subcategory_id
        )

        subcategory_name = str(
            category.subcategory_name
        )

        market_name = None

        # Standard market
        if subcategory_id in DK_MARKETS:

            market_name = DK_MARKETS[
                subcategory_id
            ]

        # Alternate market
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

                player = normalize_dk_player(
                    prop.player,
                    market_name
                )

                rows.append({
                    "player": player,
                    "market": market_name,
                    "line": prop.line,
                    "over_odds": prop.over_odds,
                    "under_odds": prop.under_odds,
                    "sportsbook": "DraftKings",
                    "game": prop.game,
                    "event_id": prop.event_id,
                })

        except Exception as e:

            print(
                "WARNING: DK market failed:",
                market_name,
                e
            )

    return rows


# ============================================================
# FANDUEL COLLECTOR
# ============================================================

def collect_fanduel(client):

    rows = []

    categories = client.get_prop_categories(
        "nfl",
        book="fanduel"
    )

    for category in categories:

        if category.category_id != "popular":
            continue

        name = str(
            category.subcategory_name
        )

        # ----------------------------------------------------
        # Ignore unrelated markets
        # ----------------------------------------------------

        if name in [
            "Most Rushing Yards",
            "Most Passing Yards",
            "Any Time Touchdown Scorer",
            "First Touchdown Scorer",
            "Last Touchdown Scorer",
        ]:
            continue

        # ----------------------------------------------------
        # Identify normal FanDuel market
        # ----------------------------------------------------

        market_name = None

        for keyword, normalized in FD_MARKETS.items():

            if keyword in name:

                market_name = normalized
                break

        # ----------------------------------------------------
        # Handle threshold markets
        #
        # FanDuel can expose these as player-specific
        # subcategories such as:
        #
        # "Derrick Henry - Rushing Yds"
        #
        # and the returned PlayerProp may contain:
        #
        # "Derrick Henry 80+ Yards"
        #
        # ----------------------------------------------------

        if market_name is None:

            if "Rushing Yds" in name:
                market_name = "Rushing Yards"

            elif "Receiving Yds" in name:
                market_name = "Receiving Yards"

            elif "Receptions" in name:
                market_name = "Receptions"

            elif "Passing Yds" in name:
                market_name = "Passing Yards"

        if market_name is None:
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

                player = str(
                    prop.player
                )

                clean_player, parsed_line, prop_type = (
                    normalize_fd_prop(
                        player,
                        market_name
                    )
                )

                # ------------------------------------------------
                # Threshold / ladder market
                # ------------------------------------------------

                if prop_type == "threshold":

                    line = parsed_line

                    # Preserve the normalized market.
                    # Mark alternate thresholds explicitly
                    # for reception markets.
                    if market_name == "Receptions":
                        output_market = "Alt Receptions"

                    else:
                        output_market = market_name

                    rows.append({
                        "player": clean_player,
                        "market": output_market,
                        "line": line,
                        "over_odds": prop.over_odds,
                        "under_odds": prop.under_odds,
                        "sportsbook": "FanDuel",
                        "game": prop.game,
                        "event_id": prop.event_id,
                    })

                # ------------------------------------------------
                # Standard Over
                # ------------------------------------------------

                elif prop_type == "over":

                    rows.append({
                        "player": clean_player,
                        "market": market_name,
                        "line": prop.line,
                        "over_odds": prop.over_odds,
                        "under_odds": prop.under_odds,
                        "sportsbook": "FanDuel",
                        "game": prop.game,
                        "event_id": prop.event_id,
                    })

                # ------------------------------------------------
                # Standard Under
                # ------------------------------------------------

                elif prop_type == "under":

                    rows.append({
                        "player": clean_player,
                        "market": market_name,
                        "line": prop.line,
                        "over_odds": prop.over_odds,
                        "under_odds": prop.under_odds,
                        "sportsbook": "FanDuel",
                        "game": prop.game,
                        "event_id": prop.event_id,
                    })

        except Exception as e:

            print(
                "WARNING: FD market failed:",
                name,
                e
            )

    return rows


# ============================================================
# REMOVE EXACT DUPLICATES
# ============================================================

def remove_duplicates(rows):

    unique = {}

    for row in rows:

        key = (
            row["player"],
            row["market"],
            row["line"],
            row["over_odds"],
            row["under_odds"],
            row["sportsbook"],
            row["game"],
        )

        unique[key] = row

    return list(
        unique.values()
    )


# ============================================================
# SAVE CSV
# ============================================================

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
        "event_id",
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


# ============================================================
# MAIN
# ============================================================

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
