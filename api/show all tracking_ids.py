from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/tracking/getall", methods=["GET"], endpoint="show_list")
@handle_exceptions
def show_list():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to display list of tracking_id's")
    # execute the query to fetch all values

    cur.execute("select tracking_id, order_id, user_id, delivery_id, status from tracking_table")
    rows = cur.fetchall()
    if not rows:
        return jsonify({"message": f"No rows found "})
    data_list = []
    for row in rows:
        tracking_id, order_id, user_id, delivery_id, status = row
        data = {
            "tracking_id": tracking_id,
            "order_id": order_id,
            "user_id": user_id,
            "delivery_id": delivery_id,
            "status": status
        }
        data_list.append(data)

    # log the details into the logger file
    logger(__name__).info("display list of all tracking_id's")

    return jsonify({"message": data_list}), 202
