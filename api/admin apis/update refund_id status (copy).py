# status of refund
from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/refund/status/<int:id>", methods=["PUT"], endpoint="refund_status_update")
@handle_exceptions
def refund_status_update(id):
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to update the status of return_id's")

    # fetch the details exists or not
    cur.execute("SELECT refund_id from return_table where refund_id= %s", (id,))
    get_id = cur.fetchone()

    # if not return error
    if not get_id:
        return jsonify({"message": "refund_id not found"}), 200

    # get the return_id and status from the request body
    data = request.get_json()
    status = request.json["status"]
    # update the status in the database
    cur.execute("UPDATE refund_table SET status = %s WHERE refund_id = %s", (status, id))
    conn.commit()
    # log the details into logger file
    logger(__name__).info(f"status updated:{data}")

    # close the data base connection
    logger(__name__).warning("Hence status updated,closing the connection")

    # return message
    return jsonify({'message': status}), 200
