from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/history/report/<int:history_id>", methods=["GET"], endpoint="history_id_report")
@handle_exceptions
def history_id_report(history_id):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting data base connection to get report of a particular history_id")

    # get query
    cur.execute("SELECT * from history_table where history_id= %s", (history_id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"history_id not found"})
    show_query = "SELECT tracking_id,order_id,order_total,order_date,shipping_address,transaction_id FROM history_table WHERE history_id = %s"

    # execute the query
    cur.execute(show_query, (history_id,))
    rows = cur.fetchone()
    if not rows:
        return jsonify({"message": f"No rows found for history_id {history_id}"})
    tracking_id, order_id, order_total, order_date, shipping_address, transaction_id = rows

    data = {
        "tracking_id": tracking_id,
        "order_id": order_id,
        "order_total": order_total,
        "order_date": order_date,
        "shipping_address": shipping_address,
        "transaction_id": transaction_id
    }
    logger(__name__).info(f"generated report of particular id ")
    # close the data base connection
    logger(__name__).warning("hence we got the report closing the connection")
    return jsonify({"message": "report of history_id", "details": data}), 200
