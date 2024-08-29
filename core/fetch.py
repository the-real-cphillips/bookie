#!/usr/bin/env python3

import requests
import os
import datetime

apiKey = os.getenv("ODDS_API_KEY")


def fetchOdds(apiKey, sport="baseball_mlb"):
    time_now = datetime.datetime.now()
    formatted_time = time_now.strftime("%Y-%m-%d")
    tomorrow = time_now + datetime.timedelta(days=1)

    odds = list()

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

    params = {
        "apiKey": apiKey,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american",
        "bookmakers": "fanduel",
        "commenceTimeFrom": f"{formatted_time}T00:00:00Z",
        "commenceTimeTo": f"{formatted_time}T23:59:59Z",
    }

    response = requests.get(url, params=params, timeout=10)
    results = response.json()

    for result in results:
        if len(result["bookmakers"]) > 0:
            odds_data = {
                "home": None,
                "away": None,
                "h_odds": None,
                "a_odds": None,
            }
            odds_data["home"] = result["home_team"]
            odds_data["away"] = result["away_team"]
            for outcome in result["bookmakers"][0]["markets"][0]["outcomes"]:
                if outcome["name"] == result["home_team"]:
                    odds_data["h_odds"] = outcome["price"]
                elif outcome["name"] == result["away_team"]:
                    odds_data["a_odds"] = outcome["price"]
                else:
                    pass
        odds.append(odds_data)
    return odds


def main():
    sport = "upcoming"

    all_odds = fetchOdds(apiKey, sport)
    for odd in all_odds:
        print(
            f"Home:  {odd['home']} {odd['h_odds']} | {odd['a_odds']} {odd['away']} : Away"
        )


if __name__ == "__main__":
    main()
