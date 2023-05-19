# report of refund id
from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/refund/report/<int:refund_id>", methods=["GET"], endpoint="refund_id_report")
@handle_exceptions
def refund_id_report(refund_id):
    cur, conn = connection()
    logger(__name__).warning("starting database connection to get report of refund_id")
    # get query
    cur.execute("SELECT return_id,order_id,refund_amount,transaction_id,status  from refund_table where refund_id=%s",
                (refund_id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"refund_id not found"}), 200
    show_query = "SELECT return_id,order_id,refund_amount,transaction_id,status FROM refund_table WHERE refundid = %s"
    cur.execute(show_query, (return_id,))
    rows = cur.fetchone()
    if not rows:
        return jsonify({"message": f"No rows found for history_id {return_id}"})
    return_id,order_id,refund_amount,transaction_id,status = rows

    data = {
        "return_id" : return_id,
        "order_id": order_id,
        "refund_amount": refund_amount,
        "transaction_id": transaction_id,
        "status": status,
    }
    # log the details into logger file
    logger(__name__).info(f"generated report of particular id ")
    # close the database connection
    logger(__name__).warning("hence we got the report closing the connection")
    return jsonify({"message": "report of refund_id", "details": data}), 200