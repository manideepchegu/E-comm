# create refund_id
from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/refund/insert", methods=["POST"], endpoint="create_refund_id")
@handle_exceptions
def create_refund_id():
    cur, conn = connection()
    logger(__name__).warning("starting the database connection for creating the refund_id")

    # get the values from the user
    data = request.get_json()
    return_id = data.get('return_id')
    order_id = data.get('order_id')
    refund_amount = data.get('refund_amount')
    transaction_id = data.get('transaction_id')
    status = data.get('status')

    # insert query
    insert_query = "INSERT INTO return_table(return_id,order_id,refund_amount,transaction_id,status) VALUES (%s,%s,%s,%s,%s)"
    values = (return_id, order_id, refund_amount, transaction_id, status)

    # execute the query with required values
    cur.execute(insert_query, values)
    # log the details into logger file

    logger(__name__).info(f"{order_id}'s refund_id created")

    # commit to database
    conn.commit()
    return jsonify({"message": "refund_id created"}), 200
