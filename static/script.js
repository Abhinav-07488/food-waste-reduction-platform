console.log("SCRIPT JS LOADED");
// =====================================
// SURPLUS PREDICTION
// =====================================

function predictSurplus() {

    let prepared =
        document.getElementById("food_prepared").value;

    let sold =
        document.getElementById("food_sold").value;

    let remaining =
        document.getElementById("remaining_food").value;


    let formData = new FormData();

    formData.append("food_prepared", prepared);

    formData.append("food_sold", sold);

    formData.append("remaining_food", remaining);


    fetch("/predict", {

        method: "POST",

        body: formData

    })

        .then(response => response.json())

        .then(data => {

            document.getElementById(
                "prediction_result"
            ).innerHTML =

                "Predicted Food Surplus: "
                + data.surplus;

        });

}



// =====================================
// ADD DONATION
// =====================================

function addDonation() {

    let formData = new FormData();


    formData.append(
        "donor_name",
        document.getElementById("donor_name").value
    );


    formData.append(
        "food_name",
        document.getElementById("food_name").value
    );


    formData.append(
        "quantity",
        document.getElementById("quantity").value
    );


    formData.append(
        "location",
        document.getElementById("location").value
    );


    formData.append(
        "expiry",
        document.getElementById("expiry").value
    );


    fetch("/add_donation", {

        method: "POST",

        body: formData

    })

        .then(response => response.json())

        .then(data => {

            document.getElementById(
                "donation_message"
            ).innerHTML = data.message;


            loadDonations();

        });

}



// =====================================
// LOAD DONATIONS
// =====================================

function loadDonations() {

    fetch("/donations")

        .then(response => response.json())

        .then(data => {


            let table =
                document.getElementById("donation_table");


            table.innerHTML = "";


            data.forEach(donation => {


                let row =
                    document.createElement("tr");


                row.innerHTML = `

                <td>${donation.id}</td>

                <td>${donation.food_name}</td>

                <td>${donation.quantity}</td>

                <td>${donation.location}</td>

                <td>${donation.expiry}</td>

                <td>${donation.status}</td>

                <td>${donation.matched_ngo}</td>

                <td>

                    <button
                        onclick="matchDonation(${donation.id})">

                        Match NGO

                    </button>


                    <button
                        onclick="updateStatus(
                            ${donation.id},
                            'Collected'
                        )">

                        Collected

                    </button>


                    <button
                        onclick="updateStatus(
                            ${donation.id},
                            'Distributed'
                        )">

                        Distributed

                    </button>

                </td>

            `;


                table.appendChild(row);

            });

        });

}



// =====================================
// SMART MATCHING
// =====================================

function matchDonation(id) {

    fetch(
        "/match/" + id,
        {
            method: "POST"
        }
    )

        .then(response => response.json())

        .then(data => {

            alert(
                "Matched NGO: "
                + data.ngo
            );


            loadDonations();

        });

}



// =====================================
// UPDATE STATUS
// =====================================

function updateStatus(id, status) {

    let formData = new FormData();


    formData.append(
        "status",
        status
    );


    fetch(
        "/update_status/" + id,
        {

            method: "POST",

            body: formData

        }
    )

        .then(response => response.json())

        .then(data => {

            alert(data.message);

            loadDonations();

        });

}



// Load data when page opens

window.onload = function () {

    loadDonations();

};