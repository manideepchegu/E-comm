# return table
# create return id
from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/return/insert", methods=["POST"], endpoint="create_return_id")
@handle_exceptions
def create_return_id():
    # set data base connection
    cur, conn = connection()
    logger(__name__).warning("starting data base connection to create return_id in the table")

    # get the values from the user
    data = request.get_json()
    order_id = data.get('order_id')
    reason_for_return = data.get('reason_for_return')
    return_date = data.get('reutrn_date')
    status = data.get('status')

    # insert query
    insert_query = "INSERT INTO return_table(order_id,reason_for_return,return_date,status) VALUES (%s,%s,%s,%s)"
    values = (order_id, reason_for_return, return_date, status)

    # execute the query with required values
    cur.execute(insert_query, values)
    # log the details into logger file

    logger(__name__).info(f"{order_id}'s return_id created")

    # commit to database
    conn.commit()
    return jsonify({"message": "return_id created"}), 200
