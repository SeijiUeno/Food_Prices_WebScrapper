from flask import Flask, render_template
import csv
import json
import os

app = Flask(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "..", "data")
csv_file = os.path.join(data_dir, "historical_food_products_clean.csv")

def load_historical_data():
    data = {}
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row["date"]
            if date not in data:
                data[date] = []
            data[date].append(row)
    return data

@app.route("/")
def index():
    raw_data = load_historical_data()
    # Prepare data to plot average price per category per day
    graph_data = {}
    for date, rows in raw_data.items():
        for row in rows:
            category = row["category"]
            # Clean the price string and convert to float
            price_str = row["price"].replace("R$", "").strip()
            try:
                price = float(price_str.replace(",", "."))
            except ValueError:
                continue
            if category not in graph_data:
                graph_data[category] = {}
            if date not in graph_data[category]:
                graph_data[category][date] = []
            graph_data[category][date].append(price)
    
    # Compute average prices per category per date
    chart_data = {}
    for category, dates in graph_data.items():
        chart_data[category] = {"dates": [], "prices": []}
        for date in sorted(dates.keys()):
            prices = dates[date]
            avg_price = sum(prices) / len(prices)
            chart_data[category]["dates"].append(date)
            chart_data[category]["prices"].append(round(avg_price, 2))
    
    # Pass the chart data as JSON to the template
    return render_template("index.html", chart_data=json.dumps(chart_data))

if __name__ == "__main__":
    app.run(debug=True)
    