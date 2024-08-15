function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}


function filterUserID() {
    // document.body.classList.add('cursor-loading');
    var userID= document.getElementById('filteruser').value;
    fetch("/insurer/filter_userid_claims/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
                body: JSON.stringify({ filteruserID: userID })
            })
    .then(response => response.json())
    .then(data => {
        document.body.classList.remove('cursor-loading');
        var table = document.querySelector('.utable');
        table.innerHTML = `
                <tr>
                    <th>Claim ID</th>
                    <th>User ID</th>
                    <th>User Name</th>
                    <th>Policy_Name</th>
                    <th>Applied Date</th>
                    <th>Claimed Date</th>
                    <th>Hospital Name</th>
                    <th>Claimed Amount</th>
                    <th>Claim Info</th>
                </tr>
        `;
        // Add new rows
        data.profiles.forEach(item => {
            var row = table.insertRow();
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            var cell6 = row.insertCell(5);
            var cell7 = row.insertCell(6);
            var cell8 = row.insertCell(7);
            var cell9 = row.insertCell(8);
            cell1.innerHTML = item.claim_id;
            cell2.innerHTML = item.user_id;
            cell3.innerHTML = item.name;
            cell4.innerHTML = item.policy_name;
            cell5.innerHTML = item.applied;
            cell6.innerHTML = item.claimed;
            cell7.innerHTML = item.hospital;
            cell8.innerHTML = item.claimed_amt;
            cell9.innerHTML = item.claim_info;
        });
    })
}

function filterpolicyname() {
    // document.body.classList.add('cursor-loading');
    var policy_name= document.getElementById('filterpolicy').value;
    fetch("/insurer/filter_policy_name_claims/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
                body: JSON.stringify({ policy_name: policy_name })
            })
    .then(response => response.json())
    .then(data => {
        document.body.classList.remove('cursor-loading');
        var table = document.querySelector('.utable');
        table.innerHTML = `
                <tr>
                    <th>Claim ID</th>
                    <th>User ID</th>
                    <th>User Name</th>
                    <th>Policy_Name</th>
                    <th>Applied Date</th>
                    <th>Claimed Date</th>
                    <th>Hospital Name</th>
                    <th>Claimed Amount</th>
                    <th>Claim Info</th>
                </tr>
        `;
        // Add new rows
        data.profiles.forEach(item => {
            var row = table.insertRow();
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            var cell6 = row.insertCell(5);
            var cell7 = row.insertCell(6);
            var cell8 = row.insertCell(7);
            var cell9 = row.insertCell(8);
            cell1.innerHTML = item.claim_id;
            cell2.innerHTML = item.user_id;
            cell3.innerHTML = item.name;
            cell4.innerHTML = item.policy_name;
            cell5.innerHTML = item.applied;
            cell6.innerHTML = item.claimed;
            cell7.innerHTML = item.hospital;
            cell8.innerHTML = item.claimed_amt;
            cell9.innerHTML = item.claim_info;
        });
    })
}