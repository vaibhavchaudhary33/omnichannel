"""
mock_servers/loyalty_mock.py
Simulates a Loyalty Program REST API.
Run:  python mock_servers/loyalty_mock.py
"""
import json
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_FILE = Path(__file__).parent.parent / "data" / "raw" / "loyalty_data.json"


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"members": []}


@app.route("/api/v1/members")
def members():
    data    = load_data()
    members = data.get("members", [])
    page    = int(request.args.get("page",   1))
    limit   = int(request.args.get("limit", 50))
    start   = (page - 1) * limit
    end     = start + limit
    return jsonify({
        "members": members[start:end],
        "meta": {
            "total":       len(members),
            "page":        page,
            "per_page":    limit,
            "total_pages": (len(members) + limit - 1) // limit,
        }
    })


@app.route("/api/v1/members/<member_id>")
def member_detail(member_id):
    data = load_data()
    for m in data.get("members", []):
        if str(m.get("member_id")) == str(member_id):
            return jsonify(m)
    return jsonify({"error": "not found"}), 404


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "loyalty-mock"})


if __name__ == "__main__":
    app.run(port=5002, debug=False)
