from flask import Flask, jsonify, request
from settings import connection, logger, handle_exceptions

app = Flask(__name__)


# creating tracking_id
@app.route("/app/v1/tracking/insert", methods=['POST'], endpoint="create_new_tracking_id")
@handle_exceptions
def create_new_tracking_id():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("start the database connection to create the tracking_id")
    # Take values from the user
    data = request.get_json()
    order_id = data.get('order_id')
    user_id = data.get('user_id')
    delivery_id = data.get('delivery_id')
    status = data.get('status')

    # insert query
    postgres_insert_query = "INSERT INTO tracking_table(order_id, user_id ,delivery_id, status) VALUES (%s ,%s ,%s, %s)"
    values = (order_id, user_id, delivery_id, status)

    # execute the query with required values
    cur.execute(postgres_insert_query, values)
    # log the details into logger file

    logger(__name__).info(f"{order_id}'s account created")

    # commit to database
    conn.commit()
    return jsonify({"message": "tracking_id created"}), 200