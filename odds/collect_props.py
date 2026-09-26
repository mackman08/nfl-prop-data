import csv
import os
import re

from curl_cffi import requests as cffi_requests
from oddswrap import OddsClient


OUTPUT_FILE = "odds/nfl_player_props_latest.csv"

BOOKS = ["draftkings", "fanduel"]

FD_EVENT_URL = "https://sbapi.nj.sportsbook.fanduel.com/api/event-page"
FD_CONTENT_URL = "https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page"
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


# Check ALT markets before standard markets
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
        "Rush + Receiving Yards",
        "Rushing + Receiving Yards",
        "Rushing +",
        "Passing Yards",
        "Rushing Yards",
        "Receiving Yards",
        "Receptions",
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

    # Threshold markets
    # Example:
    # Derrick Henry 80+ Yards
    # Mark Andrews 2+ Receptions

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



def get_fd_event_ids():

    try:

        response = cffi_requests.get(
            FD_CONTENT_URL,
            params={
                "page": "CUSTOM",
                "customPageId": "nfl",
                "_ak": FD_API_KEY,
            },
            impersonate="chrome120",
            headers={"Accept": "application/json"},
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        events = (
            data
            .get("attachments", {})
            .get("events", {})
        )

        return [
            str(event_id)
            for event_id, event in events.items()
            if " @ " in str(event.get("name", ""))
        ]

    except Exception as e:

        print(
            "WARNING: FD event discovery failed:",
            e
        )

        return []


def get_fd_standard_market_rows(event_id, tab):

    rows = []

    try:

        response = cffi_requests.get(
            FD_EVENT_URL,
            params={
                "eventId": event_id,
                "tab": tab,
                "_ak": FD_API_KEY,
            },
            impersonate="chrome120",
            headers={"Accept": "application/json"},
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        events = (
            data
            .get("attachments", {})
            .get("events", {})
        )

        event = events.get(
            str(event_id),
            {}
        )

        game = event.get("name")

        markets = (
            data
            .get("attachments", {})
            .get("markets", {})
        )

        for market in markets.values():

            market_name = str(
                market.get(
                    "marketName",
                    ""
                )
            )

            if market_name == "Passing Yards":
                normalized_market = "Passing Yards"

            elif market_name == "Receiving Yards":
                normalized_market = "Receiving Yards"

            elif market_name in [
                "Total Receptions",
                "Receptions",
            ]:
                normalized_market = "Receptions"

            elif market_name == "Rushing Yards":
                normalized_market = "Rushing Yards"

            elif market_name in [
                "Rush + Receiving Yards",
                "Rush + Rec Yds",
            ]:
                normalized_market = (
                    "Rush + Receiving Yards"
                )

            else:
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

                if re.search(
                    r"\s+Over$",
                    runner_name,
                    re.IGNORECASE
                ):
                    side = "over"

                elif re.search(
                    r"\s+Under$",
                    runner_name,
                    re.IGNORECASE
                ):
                    side = "under"

                else:
                    continue

                player = re.sub(
                    r"\s+(Over|Under)$",
                    "",
                    runner_name,
                    flags=re.IGNORECASE
                ).strip()

                odds = (
                    runner
                    .get(
                        "winRunnerOdds",
                        {}
                    )
                    .get(
                        "americanDisplayOdds",
                        {}
                    )
                    .get(
                        "americanOdds"
                    )
                )

                line = runner.get(
                    "handicap"
                )

                if (
                    not player
                    or line is None
                    or odds is None
                ):
                    continue

                rows.append({
                    "player": player,
                    "market": normalized_market,
                    "line": line,
                    "over_odds": (
                        odds
                        if side == "over"
                        else None
                    ),
                    "under_odds": (
                        odds
                        if side == "under"
                        else None
                    ),
                    "sportsbook": "FanDuel",
                    "game": game,
                    "event_id": str(event_id),
                })

    except Exception as e:

        print(
            "WARNING: FD standard tab failed:",
            event_id,
            tab,
            e
        )

    return rows



def diagnose_fanduel_event():

    event_ids = get_fd_event_ids()

    if not event_ids:

        print(
            "FD DIAGNOSTIC: no NFL events found"
        )

        return

    event_id = event_ids[0]

    print()
    print(
        "FD DIAGNOSTIC EVENT:",
        event_id
    )

    try:

        response = cffi_requests.get(
            FD_EVENT_URL,
            params={
                "eventId": event_id,
                "tab": "popular",
                "_ak": FD_API_KEY,
            },
            impersonate="chrome120",
            headers={"Accept": "application/json"},
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        print(
            "FD DIAGNOSTIC TOP-LEVEL KEYS:",
            sorted(data.keys())
        )

        attachments = data.get(
            "attachments",
            {}
        )

        print(
            "FD DIAGNOSTIC ATTACHMENT KEYS:",
            sorted(attachments.keys())
        )

        available_tabs = (
            data.get("availableTabs")
            or attachments.get("availableTabs")
            or data.get("event", {}).get("availableTabs")
        )

        print(
            "FD DIAGNOSTIC AVAILABLE TABS:",
            available_tabs
        )

        markets = attachments.get(
            "markets",
            {}
        )

        market_names = sorted(
            set(
                str(
                    market.get(
                        "marketName",
                        ""
                    )
                )
                for market in markets.values()
                if market.get("marketName")
            )
        )

        print(
            "FD DIAGNOSTIC MARKET COUNT:",
            len(market_names)
        )

        for name in market_names:

            if any(
                keyword.lower() in name.lower()
                for keyword in [
                    "passing",
                    "receiv",
                    "rush",
                    "reception",
                ]
            ):

                print(
                    "FD DIAGNOSTIC PROP MARKET:",
                    name
                )

    except Exception as e:

        print(
            "WARNING: FD diagnostic failed:",
            e
        )


def collect_fanduel_standard_tabs():

    rows = []

    event_ids = get_fd_event_ids()

    print(
        "FD standard events:",
        len(event_ids)
    )

    for tab in [
        "passing-props",
        "receiving-props",
        "rushing-props",
    ]:

        print(
            "FD standard tab:",
            tab
        )

        for event_id in event_ids:

            rows.extend(
                get_fd_standard_market_rows(
                    event_id,
                    tab
                )
            )

    return rows



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

    event_ids = get_fd_event_ids()

    print(
        "FD raw events:",
        len(event_ids)
    )

    for event_id in event_ids:

        try:

            response = cffi_requests.get(
                FD_EVENT_URL,
                params={
                    "eventId": event_id,
                    "tab": "popular",
                    "_ak": FD_API_KEY,
                },
                impersonate="chrome120",
                headers={"Accept": "application/json"},
                timeout=15,
            )

            response.raise_for_status()

            data = response.json()

            events = (
                data
                .get("attachments", {})
                .get("events", {})
            )

            event = events.get(
                str(event_id),
                {}
            )

            game = event.get(
                "name"
            )

            markets = (
                data
                .get("attachments", {})
                .get("markets", {})
            )

            for market in markets.values():

                market_name = str(
                    market.get(
                        "marketName",
                        ""
                    )
                ).strip()

                normalized_market = None

                # Standard markets
                if market_name.endswith(
                    " - Passing Yds"
                ):
                    normalized_market = (
                        "Passing Yards"
                    )

                elif market_name.endswith(
                    " - Receiving Yds"
                ):
                    normalized_market = (
                        "Receiving Yards"
                    )

                elif market_name.endswith(
                    " - Total Receptions"
                ):
                    normalized_market = (
                        "Receptions"
                    )

                elif market_name.endswith(
                    " - Rushing Yds"
                ):
                    normalized_market = (
                        "Rushing Yards"
                    )

                # Alternate markets
                elif market_name.endswith(
                    " - Alt Passing Yds"
                ):
                    normalized_market = (
                        "Alt Passing Yards"
                    )

                elif market_name.endswith(
                    " - Alt Receiving Yds"
                ):
                    normalized_market = (
                        "Alt Receiving Yards"
                    )

                elif market_name.endswith(
                    " - Alt Receptions"
                ):
                    normalized_market = (
                        "Alt Receptions"
                    )

                elif market_name.endswith(
                    " - Alt Rushing Yds"
                ):
                    normalized_market = (
                        "Alt Rushing Yards"
                    )

                elif market_name.endswith(
                    " - Rush + Rec Yds"
                ):
                    normalized_market = (
                        "Rush + Receiving Yards"
                    )

                elif market_name.endswith(
                    " - Alt Rush + Rec Yds"
                ):
                    normalized_market = (
                        "Alt Rush + Receiving Yards"
                    )

                if normalized_market is None:
                    continue

                # Explicitly exclude anything that is not
                # a player prop we want.
                if any(
                    excluded in market_name
                    for excluded in [
                        "Passing TDs",
                        "Drive 1",
                        "Game Specials",
                        "Most Passing Yards",
                        "Most Rushing Yards",
                    ]
                ):
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

                    if re.search(
                        r"\\s+Over$",
                        runner_name,
                        re.IGNORECASE
                    ):
                        side = "over"

                    elif re.search(
                        r"\\s+Under$",
                        runner_name,
                        re.IGNORECASE
                    ):
                        side = "under"

                    else:
                        # Alternate ladder rows may be
                        # represented as player + threshold.
                        side = "over"

                    player = re.sub(
                        r"\\s+(Over|Under)$",
                        "",
                        runner_name,
                        flags=re.IGNORECASE
                    ).strip()

                    odds = (
                        runner
                        .get(
                            "winRunnerOdds",
                            {}
                        )
                        .get(
                            "americanDisplayOdds",
                            {}
                        )
                        .get(
                            "americanOdds"
                        )
                    )

                    line = runner.get(
                        "handicap"
                    )

                    if (
                        not player
                        or line is None
                        or odds is None
                    ):
                        continue

                    rows.append({
                        "player": player,
                        "market": normalized_market,
                        "line": line,
                        "over_odds": (
                            odds
                            if side == "over"
                            else None
                        ),
                        "under_odds": (
                            odds
                            if side == "under"
                            else None
                        ),
                        "sportsbook": "FanDuel",
                        "game": game,
                        "event_id": str(event_id),
                    })

        except Exception as e:

            print(
                "WARNING: FD raw event failed:",
                event_id,
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

        # Alternate/threshold rows already contain
        # their complete price information.

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
