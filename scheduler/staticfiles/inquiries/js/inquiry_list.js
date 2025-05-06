document.addEventListener("DOMContentLoaded", function () {
  console.log("inquiry_list.js loaded");
  const table = document.getElementById("inquiryTable");
  const headers = table.querySelectorAll("th.sortable");
  let currentSort = { column: null, direction: "asc" };

  headers.forEach((header) => {
    header.addEventListener("click", () => {
      console.log("header clicked");
      const column = header.dataset.sort;
      if (!column) return; // Skip if no sort attribute

      // Remove previous sort classes
      headers.forEach((h) => {
        h.classList.remove("sort-asc", "sort-desc");
      });

      // Determine sort direction
      let direction = "asc";
      if (currentSort.column === column) {
        direction = currentSort.direction === "asc" ? "desc" : "asc";
      }

      // Add sort class to current header
      header.classList.add(`sort-${direction}`);

      // Update current sort
      currentSort = { column, direction };

      // Sort the table
      const tbody = table.querySelector("tbody");
      const rows = Array.from(tbody.querySelectorAll("tr"));

      rows.sort((a, b) => {
        const aValue = a
          .querySelector(`td:nth-child(${getColumnIndex(column)})`)
          .textContent.trim();
        const bValue = b
          .querySelector(`td:nth-child(${getColumnIndex(column)})`)
          .textContent.trim();

        if (direction === "asc") {
          return aValue.localeCompare(bValue);
        } else {
          return bValue.localeCompare(aValue);
        }
      });

      // Reorder the rows
      rows.forEach((row) => tbody.appendChild(row));
    });
  });

  function getColumnIndex(column) {
    const columnMap = {
      'ship_name': 1,
      'block_name': 2,
      'inquirer_group': 3,
      'inquiry_detail': 4,
      'device': 5,
      'inquirer': 6,
      'contact_number': 7,
      'request_date': 8,
      'measurement_date': 9,
      'manager': 10,
      'status': 11
    };
    return columnMap[column] || 1;
  }
}); 