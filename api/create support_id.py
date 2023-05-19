from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/support/insert", methods=["POST"], endpoint="create_support_id")
@handle_exceptions
def create_support_id():
    # set data base connection
    cur, conn = connection()
    logger(__name__).warning("starting data base connection to create support_id in the table")

    # get the values from the user
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')
    # insert query
    insert_query = "INSERT INTO support_table(question,answer) VALUES (%s,%s)"
    values = (question, answer)

    # execute the query with required values
    cur.execute(insert_query, values)
    # log the details into logger file

    logger(__name__).info(" support_id created")

    # commit to database
    conn.commit()
    return jsonify({"message": "support_id created"}), 200