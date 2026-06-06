import json
import random
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_FILE = Path(__file__).parent.parent / "data" / "raw" / "shopify_data.json"


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"customers": [], "orders": []}


@app.route("/admin/api/2024-01/customers.json")
def customers():
    data      = load_data()
    customers = data.get("customers", [])
    page      = int(request.args.get("page",     1))
    limit     = int(request.args.get("limit",   50))
    start     = (page - 1) * limit
    end       = start + limit
    return jsonify({
        "customers": customers[start:end],
        "pagination": {
            "total":       len(customers),
            "page":        page,
            "limit":       limit,
            "total_pages": (len(customers) + limit - 1) // limit,
        }
    })


@app.route("/admin/api/2024-01/orders.json")
def orders():
    data   = load_data()
    orders = data.get("orders", [])
    page   = int(request.args.get("page",   1))
    limit  = int(request.args.get("limit", 50))
    start  = (page - 1) * limit
    end    = start + limit
    return jsonify({
        "orders": orders[start:end],
        "pagination": {
            "total":       len(orders),
            "page":        page,
            "limit":       limit,
            "total_pages": (len(orders) + limit - 1) // limit,
        }
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "shopify-mock"})


if __name__ == "__main__":
    app.run(port=5001, debug=False)
