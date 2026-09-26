import csv
import os
import re

from curl_cffi import requests as cffi_requests
from oddswrap import OddsClient


OUTPUT_FILE = "odds/nfl_player_props_latest.csv"

BOOKS = ["draftkings", "fanduel"]

FD_EVENT_URL = "https://sbapi.nj.sportsbook.fanduel.com/api/event-page"
FD_API_KEY = "FhMFpcPWXMeyZxOx"


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


# IMPORTANT:
# Check ALT markets before standard markets.
FD_MARKET_KEYWORDS = [
    ("Alt Rush + Rec Yds", "Alt Rush + Receiving Yards"),
    ("Alt Rushing Yds", "Alt Rushing Yards"),
    ("Alt Receiving Yds", "Alt Receiving Yards"),
    ("Alt Receptions", "Alt Receptions"),
    ("Alt Passing Yds", "Alt Passing Yards"),
    ("Rush + Rec Yds", "Rush + Receiving Yards"),
    ("Rushing Yds", "Rushing Yards"),
    ("Receiving Yds", "Receiving Yards"),
    ("Total Receptions", "Receptions"),
    ("Passing Yds", "Passing Yards"),
]


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

    # Standard Over / Under

    if player.endswith(" Over"):

        clean_player = player[:-5].strip()

        return clean_player, None, "over"

    if player.endswith(" Under"):

        clean_player = player[:-6].strip()

        return clean_player, None, "under"

    # Threshold markets such as:
    # "Derrick Henry 80+ Yards"
    # "Mark Andrews 2+ Receptions"

    match = re.match(
        r"^(.*?)\s+(\d+(?:\.\d+)?)\+\s+(Yards|Receptions)$",
        player
    )

    if match:

        clean_player = match.group(1).strip()

        threshold = float(
            match.group(2)
        )

        return (
            clean_player,
            threshold,
            "threshold"
        )

    return player, None, None


# ============================================================
# FANDUEL RAW EVENT LOOKUP
# ============================================================

def get_fd_market_runner(
    event_id,
    market_name,
    player_name
):

    try:

        response = cffi_requests.get(
            FD_EVENT_URL,
            params={
                "eventId": event_id,
                "tab": "popular",
                "_ak": FD_API_KEY,
            },
            impersonate="chrome120",
            headers={
                "Accept": "application/json"
            },
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        markets = (
            data
            .get("attachments", {})
            .get("markets", {})
        )

        for market in markets.values():

            if market.get(
                "marketName"
            ) != market_name:
                continue

            for runner in market.get(
                "runners",
                []
            ):

                if not runner.get(
                    "isPlayerSelection"
                ):
                    continue

                runner_name = str(
                    runner.get(
                        "runnerName",
                        ""
                    )
                ).strip()

                clean_runner = re.sub(
                    r"\s+(Over|Under)$",
                    "",
                    runner_name,
                    flags=re.IGNORECASE
                ).strip()

                if (
                    clean_runner.lower()
                    != player_name.lower()
                ):
                    continue

                return {
                    "line": runner.get(
                        "handicap"
                    ),
                    "runner_name": runner_name,
                }

    except Exception as e:

        print(
            "WARNING: FD raw lookup failed:",
            event_id,
            market_name,
            player_name,
            e
        )

    return None


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

        if subcategory_id in DK_MARKETS:

            market_name = DK_MARKETS[
                subcategory_id
            ]

        elif (
            "Alt " in subcategory_name
            and (
                "Rushing Yards" in subcategory_name
                or "Receiving Yards" in subcategory_name
                or "Receptions" in subcategory_name
                or "Passing Yards" in subcategory_name
                or "Rush + Receiving Yards"
                in subcategory_name
            )
        ):

            market_name = subcategory_name

        if market_name is None:
            continue

        print(
            "DK:",
            market_name
        )

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

        # Explicit exclusions

        if name in [
            "Most Rushing Yards",
            "Most Passing Yards",
            "Any Time Touchdown Scorer",
            "First Touchdown Scorer",
            "Last Touchdown Scorer",
        ]:
            continue

        market_name = None

        for keyword, normalized in (
            FD_MARKET_KEYWORDS
        ):

            if keyword in name:

                market_name = normalized
                break

        if market_name is None:
            continue

        print(
            "FD:",
            name
        )

        try:

            props = client.get_props(
                "nfl",
                category_id="popular",
                subcategory_id=category.subcategory_id,
                book="fanduel"
            )

            for prop in props:

                original_player = str(
                    prop.player
                ).strip()

                (
                    clean_player,
                    parsed_line,
                    prop_type
                ) = normalize_fd_prop(
                    original_player,
                    market_name
                )

                # ------------------------------------------------
                # STANDARD O/U
                # ------------------------------------------------

                line = prop.line

                # OddsWrap currently returns None for standard
                # FanDuel O/U lines.
                #
                # Retrieve the actual FanDuel runner handicap.

                if line is None:

                    raw_prop = (
                        get_fd_market_runner(
                            prop.event_id,
                            prop.market,
                            clean_player
                        )
                    )

                    if raw_prop:

                        line = raw_prop.get(
                            "line"
                        )

                # ------------------------------------------------
                # DETERMINE OVER / UNDER
                # ------------------------------------------------

                side = None

                if re.search(
                    r"\s+Over$",
                    original_player,
                    re.IGNORECASE
                ):

                    side = "over"

                elif re.search(
                    r"\s+Under$",
                    original_player,
                    re.IGNORECASE
                ):

                    side = "under"

                # ------------------------------------------------
                # STANDARD O/U MARKET
                # ------------------------------------------------

                if (
                    prop_type in [
                        "over",
                        "under"
                    ]
                    and line is not None
                ):

                    rows.append({
                        "player": clean_player,
                        "market": market_name,
                        "line": line,
                        "over_odds": (
                            prop.over_odds
                            if side == "over"
                            else None
                        ),
                        "under_odds": (
                            prop.over_odds
                            if side == "under"
                            else None
                        ),
                        "sportsbook": "FanDuel",
                        "game": prop.game,
                        "event_id": prop.event_id,
                    })

                # ------------------------------------------------
                # THRESHOLD / ALT MARKET
                # ------------------------------------------------

                elif prop_type == "threshold":

                    line = parsed_line

                    if market_name == "Receptions":

                        output_market = (
                            "Alt Receptions"
                        )

                    else:

                        output_market = (
                            market_name
                        )

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

        except Exception as e:

            print(
                "WARNING: FD market failed:",
                name,
                e
            )

    return rows


# ============================================================
# PAIR FANDUEL OVER / UNDER
# ============================================================

def pair_fanduel_sides(rows):

    paired = {}
    passthrough = []

    for row in rows:

        if row["sportsbook"] != "FanDuel":

            passthrough.append(row)
            continue

        # Threshold/alternate rows already contain their
        # complete price information.
        if (
            row["market"].startswith("Alt ")
            or (
                row["over_odds"] is not None
                and row["under_odds"] is not None
            )
        ):

            passthrough.append(row)
            continue

        key = (
            row["player"],
            row["market"],
            row["line"],
            row["game"],
            row["event_id"],
        )

        if key not in paired:

            paired[key] = row.copy()

        else:

            existing = paired[key]

            if (
                row["over_odds"] is not None
                and existing["over_odds"] is None
            ):

                existing["over_odds"] = (
                    row["over_odds"]
                )

            if (
                row["under_odds"] is not None
                and existing["under_odds"] is None
            ):

                existing["under_odds"] = (
                    row["under_odds"]
                )

    return (
        passthrough
        + list(paired.values())
    )


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

    print()
    print("Pairing FanDuel Over / Under...")

    rows = pair_fanduel_sides(
        rows
    )

    print()
    print("Removing duplicates...")

    rows = remove_duplicates(
        rows
    )

    save_csv(rows)

    print()
    print("=" * 60)
    print("COLLECTION COMPLETE")
    print("TOTAL PROPS:", len(rows))
    print("OUTPUT:", OUTPUT_FILE)
    print("=" * 60)


if __name__ == "__main__":
    main()
