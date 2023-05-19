

# update status of return

from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/return/status/<int:return_id>", methods=["PUT"], endpoint="return_status_update")
@handle_exceptions
def return_status_update(return_id):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to update the status of return_id's")

    # fetch the details exists or not
    cur.execute("SELECT return_id from return_table where return_id= %s", (id,))
    get_id = cur.fetchone()

    # if not return error
    if not get_id:
        return jsonify({"message": "return_id not found"}), 200

    # get the return_id and status from the request body
    data = request.get_json()
    status = request.json["status"]
    # update the status in the database
    cur.execute("UPDATE return_table SET status = %s WHERE return_id = %s", (status, id))
    conn.commit()
    # log the details into logger file
    logger(__name__).info(f"status updated:{data}")