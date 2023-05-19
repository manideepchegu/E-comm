from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)

# report of particular return_id


@app.route("/app/v1/return/report/<int:return_id>", methods=["GET"], endpoint="return_id_report")
@handle_exceptions
def return_id_report(return_id):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting data base connection to get report of a particular return_id")

    # get query
    cur.execute("SELECT order_id,reason_for_return,return_date,status from return_table where return_id=%s", (return_id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"return_id not found"}), 200
    show_query = "SELECT order_id,reason_for_return,return_date,status FROM return_table WHERE return_id = %s"

    # execute the query
    cur.execute(show_query, (return_id,))
    rows = cur.fetchone()
    if not rows:
        return jsonify({"message": f"No rows found for history_id {return_id}"})
    order_id, reason_for_return, return_date, status = rows

    data = {
        "order_id": order_id,
        "reason_for_return": reason_for_return,
        "return_date": return_date,
        "status": status
    }
    # log the details into logger file
    logger(__name__).info(f"generated report of particular id ")
    # close the database connection
    logger(__name__).warning("hence we got the report closing the connection")
    return jsonify({"message": "report of return_id", "details": data}), 200