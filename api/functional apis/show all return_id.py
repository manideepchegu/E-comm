# fetch information about all return_id
from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/return/getall", methods=["GET"], endpoint="return_all")
@handle_exceptions
def return_all():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to display list of return_id's")
    # execute the query to fetch all values
    cur.execute("select return_id,order_id,reason_for_return,return_date,status from return_table")
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

    # log the details into logger file
    logger(__name__).info("display list of all return_id's")
    return jsonify({"message": data_list}), 202