from oddswrap import OddsClient

# Only use the two sportsbooks we want
client = OddsClient(
    books=["draftkings", "fanduel"]
)

print("Available sportsbooks:")
print(client.available_books)

print("\nNFL support:")
print("DraftKings:", client.supports("nfl"))
print("FanDuel:", client.supports("nfl"))

print("\nDraftKings NFL prop categories:")
dk_categories = client.get_prop_categories(
    "nfl",
    book="draftkings"
)

for category in dk_categories:
    print(category)

print("\nFanDuel NFL prop categories:")
fd_categories = client.get_prop_categories(
    "nfl",
    book="fanduel"
)

for category in fd_categories:
    print(category)
