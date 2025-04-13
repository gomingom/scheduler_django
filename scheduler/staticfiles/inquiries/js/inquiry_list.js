document.addEventListener("DOMContentLoaded", function () {
  const table = document.getElementById("inquiryTable");
  const headers = table.querySelectorAll("th.sortable");
  let currentSort = { column: null, direction: "asc" };

  headers.forEach((header) => {
    header.addEventListener("click", () => {
      const column = header.dataset.sort;

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
    switch (column) {
      case "ship":
        return 1;
      case "block":
        return 2;
      case "status":
        return 3;
      default:
        return 1;
    }
  }
}); 