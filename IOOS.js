document.getElementById('process-button').addEventListener('click', function () {
    const fileInput = document.getElementById('file-upload');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            const csvData = event.target.result;
            displayCSV(csvData);
        };
        reader.readAsText(file);
    } else {
        alert('Please upload a dataset!');
    }
});

function displayCSV(data) {
    const rows = data.split('\n');
    const tableHead = document.querySelector('#data-table thead');
    const tableBody = document.querySelector('#data-table tbody');

    tableHead.innerHTML = '';
    tableBody.innerHTML = '';

    rows.forEach((row, index) => {
        const cells = row.split(',');
        const rowElement = document.createElement('tr');

        cells.forEach(cell => {
            const cellElement = document.createElement(index === 0 ? 'th' : 'td');
            cellElement.textContent = cell;
            rowElement.appendChild(cellElement);
        });

        if (index === 0) {
            tableHead.appendChild(rowElement);
        } else {
            tableBody.appendChild(rowElement);
        }
    });
}

document.getElementById('quality-check-button').addEventListener('click', function () {
    alert('Running IOOS Quality Control checks!');
});

