document.addEventListener("DOMContentLoaded", () => {
    const tenantsList = document.getElementById("tenants-list");
    const form = document.getElementById("add-tenant-form");
  
    // Fetch tenants and display in the table
    async function fetchTenants() {
      const response = await fetch("/tenants");
      const tenants = await response.json();
  
      tenantsList.innerHTML = tenants
        .map(
          (tenant) =>
            `<tr>
              <td>${tenant.tenant_id}</td>
              <td>${tenant.db_name}</td>
              <td>
                <button class="edit">Edit</button>
                <button class="delete">Delete</button>
              </td>
            </tr>`
        )
        .join("");
    }
  
    // Add new tenant
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
  
      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());
  
      const response = await fetch("/tenants", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
  
      if (response.ok) {
        alert("Tenant added successfully!");
        fetchTenants();
      } else {
        alert("Error adding tenant.");
      }
    });
  
    fetchTenants();
  });
  