// const datatable = document.getElementById('datatable');

// Initializing datatable
// const dataTable = new simpleDatatables.DataTable("#datatable", {
//     searchable: true,
//     fixedHeight: true,
//     data: {
//       headings: ["SiteInfo", "TimeStamp", "Lvl_ft_Avg", "Cond_Avg", "T_Avg"],
//     }
// })


// dataTable.rows.add([
//     ["Top 10 VS Code shortcuts", "15-11-2022", "451234"],
//     ["Django basics tutorial", "5-09-2021", "451234"],
//     ["How to install Python", "12-01-2020", "451234"],
//     ["###############", "15-11-2022", "451234"],
//     ["###############", "5-09-2021", "451234"],
//     ["###############", "12-01-2020", "451234"],
//     ["###############", "15-11-2022", "451234"],
//     ["###############", "5-09-2021", "451234"],
//     ["###############", "12-01-2020", "451234"],
//     ["###############", "15-11-2022", "451234"],
//     ["###############", "5-09-2021", "451234"],
//     ["###############", "12-01-2020", "451234"],
//     ["###############", "15-11-2022", "451234"],
//     ["###############", "5-09-2021", "451234"],
//     ["###############", "12-01-2020", "451234"],
// ])


const datatable = document.getElementById('datatable');
const siteNameFilter = document.getElementById('siteNameFilter');
const startDateFilter = document.getElementById('startDateFilter');
const endDateFilter = document.getElementById('endDateFilter');
const filterBtn = document.getElementById('filterBtn');
const exportCsvBtn = document.getElementById('exportCsvBtn');

// Initialize DataTable
const dataTable = new simpleDatatables.DataTable(datatable, {
    searchable: true,
    fixedHeight: true,
    data: {
        headings: ["SiteInfo", "TimeStamp", "Lvl_ft_Avg", "Cond_Avg", "T_Avg"],
        data: []
    }
});

// Fetch and display filtered data
filterBtn.addEventListener('click', () => {
    const siteName = siteNameFilter.value;
    const startDate = startDateFilter.value;
    const endDate = endDateFilter.value;

    // Validate inputs
    if (!siteName || !startDate || !endDate) {
        alert("Please select all filter criteria.");
        return;
    }

    // Fetch filtered data
    fetch(`/dashboard/get-filtered-data/?site_name=${encodeURIComponent(siteName)}&start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(response => {
            if (response.error) {
                alert(`Error: ${response.error}`);
                return;
            }

            // Prepare rows for the DataTable
            const rows = response.map(item => [
                item.site_info || "N/A",
                item.timestamp || "N/A",
                item.lvl_ft_avg || "N/A",
                item.cond_avg || "N/A",
                item.t_avg || "N/A",
            ]);

            // Update the DataTable with new data
            dataTable.updateConfig({
                data: {
                    headings: ["SiteInfo", "TimeStamp", "Lvl_ft_Avg", "Cond_Avg", "T_Avg"],
                    data: rows
                }
            }).refresh();  // Refresh the table to show the new data
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert(`Failed to fetch data: ${error.message}`);
        });
});

// Export to CSV
exportCsvBtn.addEventListener('click', () => {
    const rows = dataTable.data.data;
    const csvContent = [
        ["SiteInfo", "TimeStamp", "Lvl_ft_Avg", "Cond_Avg", "T_Avg"], // Headers
        ...rows // Data rows
    ]
        .map(row => row.join(",")) // Join columns with commas
        .join("\n"); // Join rows with newlines

    // Create and download CSV file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'wx_data_report.csv';
    link.click();
});



