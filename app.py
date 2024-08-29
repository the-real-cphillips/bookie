#!/usr/bin/env python3
"""bookie
"""
import os
import datetime
from flask import Flask, render_template, request
from core import fetch

app = Flask(__name__)


@app.route("/")
def get_odds():
    """get_odds"""
    # test = request.args["sport"]
    api_key = os.getenv("ODDS_API_KEY")
    sport = request.args["sport"]

    if sport not in ("upcoming", "baseball_mlb", "americanfootball_nfl"):
        sport = "upcoming"

    time_now = datetime.datetime.now()
    formatted_time = time_now.strftime("%m/%d/%Y")
    last_refresh_time = time_now.strftime("%I:%M:%S %p")

    odds = fetch.fetchOdds(api_key, sport)
    return render_template(
        "index.html",
        date=formatted_time,
        odds=odds,
        last_refresh_time=last_refresh_time,
        sport=sport,
    )


if __name__ == "__main__":
    app.run()
