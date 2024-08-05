function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
function filterHospitals() {
    var pincode = document.getElementById('filter').value;
    fetch("/filter_hospitals/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
                body: JSON.stringify({ pincode: pincode })
            })
    .then(response => response.json())
    .then(data => {
        var table = document.querySelector('.htable');
        table.innerHTML = `
                <tr>
                    <th>Hospital Name</th>
                    <th>City</th>
                    <th>Address</th>
                </tr>
        `;
        // Add new rows
        data.hospitals.forEach(item => {
            var row = table.insertRow();
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            cell1.innerHTML = item.name;
            cell2.innerHTML = item.city;
            cell3.innerHTML = item.address;
        });
    })
}