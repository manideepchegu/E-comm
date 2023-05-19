# order history
# creating a new history id
from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


@app.route("/app/v1/history/insert", methods=["POST"], endpoint="create_history_id")
@handle_exceptions
def create_history_id():
    # set data base connection
    cur, conn = connection()
    logger(__name__).warning("starting data base connection to create history_id in the table")

    # get the values from the user
    data = request.get_json()
    tracking_id = data.get('tracking_id')
    order_id = data.get('order_id')
    order_total = data.get('order_total')
    order_date = data.get('order_date')
    shipping_address = data.get('shipping_address')
    transaction_id = data.get('transaction_id')

    # insert query
    insert_query = "INSERT INTO history_table(tracking_id, order_id, order_total ,order_date, shipping_address,transaction_id) VALUES (%s,%s,%s,%s,%s,%s)"
    values = (tracking_id, order_id, order_total, order_date, shipping_address, transaction_id)

    # execute the query with required values
    cur.execute(insert_query, values)
    # log the details into logger file

    logger(__name__).info(f"{order_id}'s history_id created")

    # commit to database
    conn.commit()
    return jsonify({"message": "history_id created"}), 200
