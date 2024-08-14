function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}


function filterUserID() {
    // document.body.classList.add('cursor-loading');
    var userID= document.getElementById('filteruser').value;
    fetch("/insurer/filter_userid/", {
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
                    <th>User ID</th>
                    <th>User Name</th>
                    <th>Age</th>
                    <th>Policy Name</th>
                    <th>Plan Type</th>
                    <th>Endrolled Date</th>
                    <th>Claimable Amount</th>
                    <th>No. of claims</th>
                </tr>
        `;
        // Add new rows
            var row = table.insertRow();
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            var cell6 = row.insertCell(5);
            var cell7 = row.insertCell(6);
            var cell8 = row.insertCell(7);
            cell1.innerHTML = data.user_id;
            cell2.innerHTML = data.user_name;
            cell3.innerHTML = data.age;
            cell4.innerHTML = data.policy_name;
            cell5.innerHTML = data.plan;
            cell6.innerHTML = data.date;
            cell7.innerHTML = data.claimable_amt;
            cell8.innerHTML = data.claims;
    })
}

function filterpolicyname() {
    // document.body.classList.add('cursor-loading');
    var policy_name= document.getElementById('filterpolicy').value;
    fetch("/insurer/filter_policy_name/", {
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
                    <th>User ID</th>
                    <th>User Name</th>
                    <th>Age</th>
                    <th>Policy Name</th>
                    <th>Plan Type</th>
                    <th>Endrolled Date</th>
                    <th>Claimable Amount</th>
                    <th>No. of claims</th>
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
            cell1.innerHTML = item.user_id;
            cell2.innerHTML = item.user_name;
            cell3.innerHTML = item.age;
            cell4.innerHTML = item.policy_name;
            cell5.innerHTML = item.plan;
            cell6.innerHTML = item.date;
            cell7.innerHTML = item.claimable_amt;
            cell8.innerHTML = item.claims;
        });
    })
}