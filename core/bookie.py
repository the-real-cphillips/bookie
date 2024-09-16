#! /usr/bin/env python3
import os
import datetime
import sys
import logging
import requests
from utils import mock

mock_response = mock.mock_response

def fetch_odds(sport):
    """fetchOdds"""
    time_now = datetime.datetime.now()
    formatted_date = time_now.strftime("%Y-%m-%d")
    one_week = time_now + datetime.timedelta(days=7)
    one_week = one_week.strftime("%Y-%m-%d")
    api_key = os.getenv("ODDS_API_KEY")

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

    params = {
        "api_key": api_key,
        "regions": "us",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "american",
        "bookmakers": "fanduel",
        "commenceTimeFrom": f"{formatted_date}T23:59:59Z",
        "commenceTimeTo": f"{one_week}T00:00:00Z",
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        response.json()["message"]

    return response.json()


def parse_odds_data(json_data):
    odds_data = []
    count = 0

    while count < 10:
        for game in json_data:
            count += 1
            game_data = {
                "sport": game["sport_key"],
                "home": game["home_team"],
                "away": game["away_team"],
                "commence_time": game["commence_time"],
                "moneyline": None,
                "spreads_price": None,
                "spreads_point": None,
                "totals": None,
            }

            try:
                for market in game["bookmakers"][0]["markets"]:
                    if market["key"] == "h2h":
                        game_data["moneyline"] = [
                            outcome["price"] for outcome in market["outcomes"]
                        ]
                    elif market["key"] == "spreads":
                        game_data["spreads_price"] = [
                            outcome["price"] for outcome in market["outcomes"]
                        ]
                        game_data["spreads_point"] = [
                            outcome["point"] for outcome in market["outcomes"]
                        ]
                    elif market["key"] == "totals":
                        game_data["totals"] = [
                            outcome["price"] for outcome in market["outcomes"]
                        ]
            except IndexError as err:
                pass

            odds_data.append(game_data)

    return odds_data


def main():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s   - %(message)s")
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)

    try:
        sport = sys.argv[1]
    except IndexError:
        sport = "mock"

    logger.info(sport)

    if sys.argv[1] == "mock":
        print(mock_response)
        parsed = parse_odds_data(mock_response)
        print(parsed)
    elif sys.argv[1] == "live":
        odds = fetch_odds("baseball_mlb")
        parsed = parse_odds_data(odds)
        print(parsed)


if __name__ == "__main__":
    main()
