#!/usr/bin/env python3
"""bookie
"""
import os
import datetime
import logging
from flask import Flask, render_template, send_from_directory, jsonify
from core import bookie

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/")
@app.route("/<sport>")
def get_odds(sport="mlb"):
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        logger.error("ODDS_API_KEY environment variable not set.")
        return render_template("error.html", message="API key not configured."), 500

    sport_map = {
        "mlb": {
            "backend": "baseball_mlb",
            "title": "MLB",
            "logo": "mlb.jpg"
        },
        "nba": {
            "backend": "americanfootball_nfl",
            "title": "NFL",
            "logo": "nba.png"
        },
        "ncaaf": {
            "backend": "americanfootball_ncaaf",
            "title": "NCAA Football",
            "logo": "ncaa.png"
        },
        "nfl": {
            "backend": "americanfootball_nfl",
            "title": "NFL",
            "logo": "nfl.png"
        },
        "nhl": {
            "backend": "icehockey_nhl",
            "title": "NHL",
            "logo": "nhl.png"
        },
    }

    if sport not in sport_map:
        logger.error(f"Invalid sport: {sport}")
        return render_template("error.html", message=f"Invalid sport: {sport}"), 400

    sport_uri = sport_map[sport]["backend"]
    title = sport_map[sport]["title"]
    logo = sport_map[sport]["logo"]

    time_now = datetime.datetime.now()
    formatted_time = time_now.strftime("%m/%d/%Y")
    last_refresh_time = time_now.strftime("%I:%M:%S %p")
    odds = bookie.fetch_odds(api_key, sport_uri)
    if odds is None:
        logger.error(f"Failed to fetch odds for {sport_uri}")
        return render_template("error.html", message=f"Failed to fetch odds for {sport_uri}"), 500

    parsed_odds = bookie.parse_odds_data(odds)
    return render_template(
        "index.html",
        odds=parsed_odds,
        date=formatted_time,
        last_refresh_time=last_refresh_time,
        title=title,
        logo=logo,
    )


if __name__ == "__main__":
    app.run(debug=True)
