import csv
import os
from oddswrap import OddsClient


# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_FILE = "odds/nfl_player_props_latest.csv"

BOOKS = ["draftkings", "fanduel"]


# ============================================================
# DRAFTKINGS MARKETS
# ============================================================
#
# STANDARD MARKETS
#
# 16571 = Rushing Yards
# 16570 = Receiving Yards
# 16821 = Receptions
# 16569 = Passing Yards
#
# FUTURE MARKET
#
# 16572 = Rush + Receiving Yards
#
# We also collect alternate versions of these markets.
#
# ============================================================

DK_MARKETS = {
    "16571": "Rushing Yards",
    "16570": "Receiving Yards",
    "16821": "Receptions",
    "16569": "Passing Yards",
    "16572": "Rush + Receiving Yards",
}


# ============================================================
# FANDUEL MARKETS
# ============================================================
#
# FanDuel exposes player-specific markets through the
# "popular" category.
#
# We explicitly allow the standard and alternate versions
# of the markets we use.
#
# ============================================================

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
# DRAFTKINGS COLLECTOR
# ============================================================

def collect_draftkings(client):

    rows = []

    categories = client.get_prop_categories(
        "nfl",
        book="draftkings"
    )

    for category in categories:

        # Only examine our relevant NFL prop categories.
        #
        # 1000 = Passing Props
        # 1001 = Rushing Props
        # 1342 = Receiving Props

        if category.category_id not in [
            "1000",
            "1001",
            "1342",
        ]:
            continue

        subcategory_id = str(
            category.subcategory_id
        )

        subcategory_name = str(
            category.subcategory_name
        )

        # ----------------------------------------------------
        # Standard markets
```

