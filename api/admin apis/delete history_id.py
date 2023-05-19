from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)
@app.route("/app/v1/history/delete/<int:history_id>", methods=["DELETE"], endpoint="delete_history_id")
@handle_exceptions
def delete_history_id(history_id):
    # start the db connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to delete the history_id from the table")

    # execute the query
    cur.execute("SELECT * from history_table where history_id=%s", (history_id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"history_id not found"}), 200

    delete_query = "DELETE from history_table WHERE history_id = %s"

    cur.execute(delete_query, (history_id,))

    conn.commit()

    # log the details into logger file
    logger(__name__).info(f"history_id {history_id} deleted from the table")

    # close the db connection
    logger(__name__).warning("hence the history_id is deleted closing the connection")

    # return message
    return jsonify({"messages": "history_id deleted successfully", "history_id": history_id}), 200
