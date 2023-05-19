from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/tracking/delete/<int:tracking_id>", methods=["DELETE"], endpoint="delete_tracking_id")
@handle_exceptions
def delete_tracking_id(tracking_id):
    # start the db connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to delete the tracking_id from the table")

    # execute the query
    cur.execute("SELECT * from tracking_table where tracking_id=%s", (tracking_id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"tracking_id not found"}), 404
    delete_query = "DELETE from tracking_table WHERE tracking_id = %s"
    cur.execute(delete_query, (tracking_id,))
    conn.commit()

    # log the details into logger file
    logger(__name__).info(f"tracking_id {tracking_id} deleted from the table")

    # close the db connection
    logger(__name__).warning("hence the tracking_id is deleted closing the connection")
    cur.close()
    conn.close()
    # return message
    return jsonify({"messages": "tracking_id deleted successfully", "tracking_id": tracking_id}), 200
