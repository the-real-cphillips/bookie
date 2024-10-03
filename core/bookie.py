#! /usr/bin/env python3
import os
import datetime
import sys
import logging
import requests

# Configure logging for better error reporting
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_odds(api_key, sport):
    """Fetches odds data from the Odds API."""
    time_now = datetime.datetime.now()
    formatted_date = time_now.strftime("%Y-%m-%d")
    one_week = (time_now + datetime.timedelta(days=7)).strftime("%Y-%m-%d")

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

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching odds: {e}")
        return None  # Or raise the exception, depending on desired error handling


def parse_odds_data(json_data):
    """Parses the JSON response into a list of game dictionaries."""
    if json_data is None:
        return [] #Handle case where fetch_odds returns None

    odds_data = []
    for game in json_data:
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
                    game_data["moneyline"] = [outcome["price"] for outcome in market["outcomes"]]
                elif market["key"] == "spreads":
                    game_data["spreads_price"] = [outcome["price"] for outcome in market["outcomes"]]
                    game_data["spreads_point"] = [outcome["point"] for outcome in market["outcomes"]]
                elif market["key"] == "totals":
                    game_data["totals"] = [outcome["price"] for outcome in market["outcomes"]]
        except (IndexError, KeyError) as e:
            logger.warning(f"Error parsing game data: {e}, skipping game.")
            continue #Skip to the next game if parsing fails

        odds_data.append(game_data)
    return odds_data


def main():
    """Main function to fetch and process odds data."""
    if len(sys.argv) != 2:
        logger.error("Usage: python bookie.py <sport>")
        sys.exit(1)

    sport = sys.argv[1]
    api_key = os.getenv("ODDS_API_KEY")
    if api_key is None:
        logger.error("ODDS_API_KEY environment variable not set.")
        sys.exit(1)

    odds_data = fetch_odds(api_key, sport)
    parsed_data = parse_odds_data(odds_data)
    print(parsed_data)


if __name__ == "__main__":
    main()
