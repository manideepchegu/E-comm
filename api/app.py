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


# show the tracking id's in the table

@app.route("/app/v1/tracking/getall", methods=["GET"], endpoint="show_list")
@handle_exceptions
def show_list():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to display list of tracking_id's")
    # execute the query to fetch all values

    cur.execute("select tracking_id, order_id, user_id, delivery_id, status from tracking_table")
    rows = cur.fetchall()
    if not rows:
        return jsonify({"message": f"No rows found "})
    for row in rows:
        tracking_id, order_id, user_id, delivery_id, status = rows

    data = {
        "tracking_id": tracking_id,
        " order_id": order_id,
        "user_id ": user_id,
        "delivery_id": delivery_id,
        "status": "status"

    }
    list.append(data)

    # log the details into logger file
    logger(__name__).info("display list of all tracking_id's")

    return jsonify({"message": data}), 202


# updating the status of a particular id
@app.route("/app/v1/tracking/status/<int:tracking_id>", methods=["PUT"], endpoint="tracking_status_update")
@handle_exceptions
def tracking_status_update(tracking_id):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to update the status of tracking_id's")

    # fetch the details exists or not
    cur.execute("SELECT tracking_id from tracking_table where tracking_id= %s", (tracking_id,))
    get_id = cur.fetchone()

    # if not return error
    if not get_id:
        return jsonify({"message": "tracking_id not found"}), 200

    # get the tracking_id and status from the request body
    data = request.get_json()
    status = request.json["status"]

    # update the status in the database
    cur.execute("UPDATE tracking_table SET status = %s WHERE tracking_id = %s", (status, tracking_id))
    conn.commit()

    # log the details into logger file
    logger(__name__).info(f"status updated:{data}")

    # close the data base connection
    logger(__name__).warning("Hence status updated,closing the connection")

    # return message
    return jsonify({'message': status}), 200


# delete tracking_id from the table

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


# report of a paricular tracking_id
@app.route("/app/v1/tracking/report/<int:tracking_id>", methods=["GET"], endpoint="tracking_id_report")
@handle_exceptions
def tracking_id_report(tracking_id):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting data base connection to get report of a particular tracking_id")

    # get query
    cur.execute("SELECT tracking_id,order_id,user_id,delivery_id,status from tracking_table where tracking_id=%s",
                (tracking_id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"history_id not found"}), 200
    show_query = "SELECT tracking_id,order_id,user_id,delivery_id,status FROM tracking_table WHERE tracking_id = %s"
    # execute the query
    cur.execute(show_query, (tracking_id,))
    rows = cur.fetchall()
    columns = [column[0] for column in cur.description]
    data = [dict(zip(columns, row)) for row in rows]
    # log the details into logger file
    logger(__name__).info(f"generated report of particular id ")
    # close the data base connection
    logger(__name__).warning("hence we got the report closing the connection")
    return jsonify({"message": "report of tracking_id", "details": data}), 200


# order history
# creating a new history id
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


# fetch information about all order history_id's
@app.route("/app/v1/history/getall", methods=["GET"], endpoint="history")
@handle_exceptions
def history():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to display list of history_id's")
    # execute the query to fetch all values

    cur.execute(
        "select history_id,tracking_id, order_id, order_total, "
        "order_date, shipping_address, transaction_id from history_table")
    get_rows = cur.fetchall()

    if not get_rows:
        return jsonify({"message": f"No rows found "})

    print("show all details", get_rows)
    history_id, tracking_id, order_id, order_total, order_date, shipping_address, transaction_id = get_rows

    data = {
        "history_id": history_id,
        "tracking_id": tracking_id,
        "order_id": order_id,
        "order_total": order_total,
        "order_date": order_date,
        "shipping_address": shipping_address,
        "transaction_id": transaction_id
    }

    print(data)
    # log the details into logger file
    logger(__name__).info("display list of all history_id's")

    return jsonify({"message": data}), 202


@app.route("/app/v1/history/report/<int:history_id>", methods=["GET"], endpoint="history_id_report")
@handle_exceptions
def history_id_report(history_id):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting data base connection to get report of a particular history_id")

    # get query
    cur.execute("SELECT * from history_table where history_id= %s", (history_id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"history_id not found"})
    show_query = "SELECT tracking_id,order_id,order_total,order_date,shipping_address,transaction_id FROM history_table WHERE history_id = %s"

    # execute the query
    cur.execute(show_query, (history_id,))
    rows = cur.fetchone()
    if not rows:
        return jsonify({"message": f"No rows found for history_id {history_id}"})
    tracking_id, order_id, order_total, order_date, shipping_address, transaction_id = rows

    data = {
        "tracking_id": tracking_id,
        "order_id": order_id,
        "order_total": order_total,
        "order_date": order_date,
        "shipping_address": shipping_address,
        "transaction_id": transaction_id
    }
    logger(__name__).info(f"generated report of particular id ")
    # close the data base connection
    logger(__name__).warning("hence we got the report closing the connection")
    return jsonify({"message": "report of history_id", "details": data}), 200


# delete history of a particular id
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


# return table
# create return id
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


# fetch information about all return_id
@app.route("/app/v1/return/getall", methods=["GET"], endpoint="return_all")
@handle_exceptions
def return_all():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to display list of return_id's")
    # execute the query to fetch all values

    cur.execute("select return_id,order_id,reason_for_return,return_date,status from return_table")
    rows = cur.fetchall()

    # log the details into logger file
    logger(__name__).info("display list of all return_id's")
    return jsonify({"message": data}), 202


# report of particular return_id
@app.route("/app/v1/return/report/<int:return_id>", methods=["GET"], endpoint="return_id_report")
@handle_exceptions
def return_id_report(return_id):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting data base connection to get report of a particular return_id")

    # get query
    cur.execute("SELECT order_id,reason_for_return,return_date,status from return_table where return_id=%s", (id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"return_id not found"}), 200
    show_query = "SELECT order_id,reason_for_return,return_date,status FROM return_table WHERE return_id = %s"

    # execute the query
    cur.execute(show_query, (id,))
    rows = cur.fetchall()
    columns = [column[0] for column in cur.description]
    data = [dict(zip(columns, row)) for row in rows]
    # log the details into logger file
    logger(__name__).info(f"generated report of particular id ")
    # close the database connection
    logger(__name__).warning("hence we got the report closing the connection")
    return jsonify({"message": "report of return_id", "details": data}), 200


# update status of return
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

    # close the data base connection
    logger(__name__).warning("Hence status updated,closing the connection")

    # return message
    return jsonify({'message': status}), 200


# delete return_id
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


# create refund_id
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


# report of refund id
@app.route("/app/v1/refund/report/<int:refund_id>", methods=["GET"], endpoint="refund_id_report")
@handle_exceptions
def refund_id_report(refund_id):
    cur, conn = connection()
    logger(__name__).warning("starting database connection to get report of refund_id")
    # get query
    cur.execute("SELECT return_id,order_id,refund_amount,transaction_id,status  from refund_table where refund_id=%s",
                (id,))
    get_id = cur.fetchone()
    if not get_id:
        return jsonify({"message": f"refund_id not found"}), 200
    show_query = "SELECT return_id,order_id,refund_amount,transaction_id,status FROM refund_table WHERE refundid = %s"
    # execute the query
    cur.execute(show_query, (id,))
    rows = cur.fetchall()
    columns = [column[0] for column in cur.description]
    data = [dict(zip(columns, row)) for row in rows]
    # log the details into logger file
    logger(__name__).info(f"generated report of particular id ")
    # close the database connection
    logger(__name__).warning("hence we got the report closing the connection")
    return jsonify({"message": "report of refund_id", "details": data}), 200


# status of refund

@app.route("/app/v1/refund/status/<int:id>", methods=["PUT"], endpoint="refund_status_update")
@handle_exceptions
def refund_status_update(id):
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to update the status of return_id's")

    # fetch the details exists or not
    cur.execute("SELECT refund_id from return_table where refund_id= %s", (id,))
    get_id = cur.fetchone()

    # if not return error
    if not get_id:
        return jsonify({"message": "refund_id not found"}), 200

    # get the return_id and status from the request body
    data = request.get_json()
    status = request.json["status"]
    # update the status in the database
    cur.execute("UPDATE refund_table SET status = %s WHERE refund_id = %s", (status, id))
    conn.commit()
    # log the details into logger file
    logger(__name__).info(f"status updated:{data}")

    # close the data base connection
    logger(__name__).warning("Hence status updated,closing the connection")

    # return message
    return jsonify({'message': status}), 200


# chart support

# create id
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


@app.route("/app/v1/support/getall", methods=["GET"], endpoint="support_all")
@handle_exceptions
def support_all():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("starting the db connection to display list of support_id's")
    # execute the query to fetch all values

    cur.execute("select * from support_table")
    rows = cur.fetchall()
    columns = [column[0] for column in cur.description]
    data = [dict(zip(columns, row)) for row in rows]

    # log the details into logger file
    logger(__name__).info("display list of all support_id's")
    return jsonify({"message": data}), 202


if __name__ == '__main__':
    app.run(debug=True, port=5000)
