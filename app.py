from flask import Flask, render_template, request, jsonify

from database import connect_database, create_tables

from model import predict_surplus


app = Flask(__name__)

create_tables()


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------
# FOOD SURPLUS PREDICTION
# -----------------------------

@app.route("/predict", methods=["POST"])
def predict():

    food_prepared = int(request.form["food_prepared"])

    food_sold = int(request.form["food_sold"])

    remaining_food = int(request.form["remaining_food"])


    surplus = predict_surplus(
        food_prepared,
        food_sold,
        remaining_food
    )


    return jsonify({

        "success": True,

        "surplus": surplus

    })


# -----------------------------
# ADD DONATION
# -----------------------------

@app.route("/add_donation", methods=["POST"])
def add_donation():

    donor_name = request.form["donor_name"]

    food_name = request.form["food_name"]

    quantity = int(request.form["quantity"])

    location = request.form["location"]

    expiry = request.form["expiry"]


    connection = connect_database()

    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO donations
        (
            donor_name,
            food_name,
            quantity,
            location,
            expiry,
            status,
            matched_ngo
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        donor_name,
        food_name,
        quantity,
        location,
        expiry,
        "Available",
        "Not Matched"
    ))


    connection.commit()

    connection.close()


    return jsonify({

        "success": True,

        "message": "Donation added successfully"

    })


# -----------------------------
# SHOW DONATIONS
# -----------------------------

@app.route("/donations")
def donations():

    connection = connect_database()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT * FROM donations
        ORDER BY id DESC
    """)


    data = cursor.fetchall()

    connection.close()


    donations_list = []

    for donation in data:

        donations_list.append({

            "id": donation["id"],

            "donor_name": donation["donor_name"],

            "food_name": donation["food_name"],

            "quantity": donation["quantity"],

            "location": donation["location"],

            "expiry": donation["expiry"],

            "status": donation["status"],

            "matched_ngo": donation["matched_ngo"]

        })


    return jsonify(donations_list)


# -----------------------------
# SMART DONATION MATCHING
# -----------------------------

@app.route("/match/<int:donation_id>", methods=["POST"])
def match_donation(donation_id):

    connection = connect_database()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT * FROM donations
        WHERE id = ?
    """, (donation_id,))


    donation = cursor.fetchone()


    if donation is None:

        connection.close()

        return jsonify({

            "success": False,

            "message": "Donation not found"

        })


    # Simple matching based on location
    location = donation["location"].lower()


    if location == "ludhiana":

        ngo = "Helping Hands NGO"

    elif location == "amritsar":

        ngo = "Hope Charity NGO"

    elif location == "jalandhar":

        ngo = "Community Food NGO"

    else:

        ngo = "Nearest Available NGO"


    cursor.execute("""
        UPDATE donations

        SET matched_ngo = ?,
            status = ?

        WHERE id = ?
    """,
    (
        ngo,
        "Matched",
        donation_id
    ))


    connection.commit()

    connection.close()


    return jsonify({

        "success": True,

        "ngo": ngo,

        "message": "Donation matched successfully"

    })


# -----------------------------
# UPDATE DONATION STATUS
# -----------------------------

@app.route("/update_status/<int:donation_id>", methods=["POST"])
def update_status(donation_id):

    status = request.form["status"]


    connection = connect_database()

    cursor = connection.cursor()


    cursor.execute("""
        UPDATE donations

        SET status = ?

        WHERE id = ?
    """,
    (
        status,
        donation_id
    ))


    connection.commit()

    connection.close()


    return jsonify({

        "success": True,

        "message": "Donation status updated"

    })


# -----------------------------
# RUN APPLICATION
# -----------------------------

if __name__ == "__main__":

    app.run(debug=True)