from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/support/getall", methods=["GET"], endpoint="support_all")
@handle_exceptions
def support_all():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to display list of support_id's")
    # execute the query to fetch all values
    cur.execute("select support_id,question,answer from support_table")
    rows = cur.fetchall()
    if not rows:
        return jsonify({"message": f"No rows found "})
    data_list = []
    for row in rows:
        support_id, question, answer = row
        data = {
            "support_id": support_id,
            "question": question,
            "answer": answer,
        }
        data_list.append(data)

    # log the details into logger file
    logger(__name__).info("display list of all support_id's")
    return jsonify({"message": data_list}), 202
