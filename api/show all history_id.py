from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


# fetch information about all order history_id's
@app.route("/app/v1/history/getall", methods=["GET"], endpoint="history")
@handle_exceptions
def history():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to display list of history_id's")
    # execute the query to fetch all values

    cur.execute(
        "select history_id,tracking_id, order_id, order_total, "
        "order_date, shipping_address, transaction_id from history_table")
    rows = cur.fetchall()
    if not rows:
        return jsonify({"message": f"No rows found "})
    data_list = []
    for row in rows:
        history_id, tracking_id, order_id, order_total, order_date, shipping_address, transaction_id = row
        data = {
            "history_id": history_id,
            "tracking_id": tracking_id,
            "order_id": order_id,
            "order_total": order_total,
            "order_date": order_date,
            "shipping_address": shipping_address,
            "transaction_id": transaction_id
        }
        data_list.append(data)
    # log the details into logger file
    logger(__name__).info("display list of all history_id's")

    return jsonify({"message": data_list}), 202
