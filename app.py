import io
from contextlib import redirect_stdout
from flask import Flask, jsonify, request
import pandas as pd
import os

# Define your global DataFrame
traffic_df = None

app = Flask(__name__)

def load_traffic_data():
    global traffic_df
    print("Loading Austin Traffic Data...")
    traffic_df = pd.read_csv("atxtraffic.csv")
    print(f"Loaded {len(traffic_df)} rows into memory.")

@app.route("/")
def index():
    global traffic_df
    sample = traffic_df.head(10).to_dict(orient="records")
    return jsonify(sample)

@app.route("/head")
def top():
    global traffic_df
    num = int(request.args.get('count'))
    sample = traffic_df.head(num).to_dict(orient="records")
    return jsonify(sample)

@app.route("/shape")
def get_shape():
    global traffic_df
    if traffic_df is None:
        return jsonify({"error": "Data not loaded"}), 500

    rows, cols = traffic_df.shape
    return jsonify({"rows": rows, "columns": cols})

@app.route("/columns")
def get_columns():
    global traffic_df
    if traffic_df is None:
        return jsonify({"error": "Data not loaded"}), 500

    columns = traffic_df.columns.tolist()
    return jsonify({"columns": columns})

@app.route("/info")
def get_info():
    global traffic_df
    if traffic_df is None:
        return jsonify({"error": "Data not loaded"}), 500

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        traffic_df.info()
    info_str = buffer.getvalue()
    return jsonify({"info": info_str})

@app.route("/summary")
def get_summary():
    global traffic_df
    if traffic_df is None:
        return jsonify({"error": "Data not loaded"}), 500

    summary = {
        "shape": {
            "rows": traffic_df.shape[0],
            "columns": traffic_df.shape[1]
        },
        "columns": traffic_df.columns.tolist(),
        "dtypes": traffic_df.dtypes.astype(str).to_dict(),
        "null_counts": traffic_df.isnull().sum().to_dict(),
        "describe": traffic_df.describe(include="all").to_dict()
    }

    return jsonify(summary)

@app.route("/describe")
def get_describe():
    global traffic_df
    if traffic_df is None:
        return jsonify({"error": "Data not loaded"}), 500

    # Include all columns (numeric + non-numeric)
    stats = traffic_df.describe(include="all").to_dict()
    return jsonify(stats)


if __name__ == "__main__":
    load_traffic_data()  # <- This runs BEFORE the server starts
    app.run(debug=True, host="0.0.0.0", port=8076)
