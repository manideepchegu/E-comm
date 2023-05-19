from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


# report of a paricular tracking_id
@app.route("/app/v1/tracking/report/<int:tracking_id>", methods=["GET"], endpoint="tracking_id_report")
@handle_exceptions
def tracking_id_report(tracking_id):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting data base connection to get report of a particular tracking_id")

    # get query
    cur.execute("SELECT tracking_id,order_id,user_id,delivery_id,status from tracking_table where tracking_id=%s",
                (tracking_id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"history_id not found"}), 200
    show_query = "SELECT tracking_id,order_id,user_id,delivery_id,status FROM tracking_table WHERE tracking_id = %s"
    # execute the query
    cur.execute(show_query, (tracking_id,))
    rows = cur.fetchall()
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
    logger(__name__).info(f"generated report of particular id ")
    # close the data base connection
    logger(__name__).warning("hence we got the report closing the connection")
    return jsonify({"message": "report of tracking_id", "details": data_list}), 200

