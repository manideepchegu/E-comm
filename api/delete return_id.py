# delete return_id
from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/return/delete/<int:return_id>", methods=["DELETE"], endpoint="delete_return_id")
@handle_exceptions
def delete_return_id(return_id):
    # start database connection
    cur, conn = connection()
    logger(__name__).warning("starting the database connection to delete the return_id")
    # execute the query
    cur.execute("SELECT * from return_table where return_id=%s", (return_id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"return_id not found"}), 200

    delete_query = "DELETE from return_table WHERE return_id = %s"

    cur.execute(delete_query, (return_id,))

    conn.commit()

    # log the details into logger file
    logger(__name__).info(f"return_id {return_id} deleted from the table")
    # close the db connection
    logger(__name__).warning("hence the return_id is deleted closing the connection")

    # return message
    return jsonify({"messages": "return_id deleted successfully", "reutrn_id": return_id}), 200