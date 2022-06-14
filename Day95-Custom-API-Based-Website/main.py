from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flight_search import FlightSearch
from datetime import datetime, timedelta

app = Flask(__name__)
Bootstrap(app)

flight_search = FlightSearch()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.form
        print(data["d_date"])
        min_stay, max_stay = map(int, data["stay"].split('-'))

        departure_date = datetime.strptime(data["d_date"] + " 00:00:00", '%m/%d/%Y %H:%M:%S')
        print(departure_date)

        flight_list = flight_search.check_flights(data["d_city"], data["a_city"], departure_date, min_stay, max_stay, data["direction"])

        # print(len(flight_list))

        return render_template("index.html", result=True, total=len(flight_list), flight_list=flight_list, d_date=data["d_date"], stay=data["stay"])

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)