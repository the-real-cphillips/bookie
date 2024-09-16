#!/usr/bin/env python3
"""bookie
"""
import os
import datetime
from flask import Flask, render_template, request
from core import bookie
from utils import mock

app = Flask(__name__)

@app.route("/")
@app.route("/<sport>")
def get_odds(sport="nfl"):

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
        }
    }
    
    sport_uri = sport_map[sport]['backend']
    title = sport_map[sport]['title']

    time_now = datetime.datetime.now()
    formatted_time = time_now.strftime("%m/%d/%Y")
    last_refresh_time = time_now.strftime("%I:%M:%S %p")
    odds = bookie.fetch_odds(sport_uri)
    parsed_odds = bookie.parse_odds_data(odds)
    # parsed_odds = bookie.parse_odds_data(mock_response)
    return render_template(
        "index.html",
        odds=parsed_odds,
        date=formatted_time,
        last_refresh_time=last_refresh_time,
        title=title,
    )


if __name__ == "__main__":
    app.run()
