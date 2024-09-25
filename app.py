#!/usr/bin/env python3
"""bookie
"""
import os
import datetime
from flask import Flask, render_template, send_from_directory
from core import bookie

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
        raise ValueError("[X] Please set ODDS_API_KEY")

    sport_map = {
        "mlb": {
            "backend": "baseball_mlb",
            "title": "MLB",
        },
        "ncaaf": {
            "backend": "americanfootball_ncaaf",
            "title": "NCAA Football",
        },
        "nfl": {
            "backend": "americanfootball_nfl",
            "title": "NFL",
        },
    }

    sport_uri = sport_map[sport]["backend"]
    title = sport_map[sport]["title"]

    time_now = datetime.datetime.now()
    formatted_time = time_now.strftime("%m/%d/%Y")
    last_refresh_time = time_now.strftime("%I:%M:%S %p")
    odds = bookie.fetch_odds(api_key, sport_uri)
    parsed_odds = bookie.parse_odds_data(odds)
    return render_template(
        "index.html",
        odds=parsed_odds,
        date=formatted_time,
        last_refresh_time=last_refresh_time,
        title=title,
    )


if __name__ == "__main__":
    app.run(debug=True)
