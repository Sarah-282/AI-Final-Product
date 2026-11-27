
const API_URL = "http://localhost:5000/api/residents";

// Add Resident to MongoDB
document.getElementById("residentForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;

    const residentData = {
        name: form.elements.namedItem("name").value,
        email: form.elements.namedItem("email").value,
        phone: form.elements.namedItem("phone").value,
        roomNumber: form.elements.namedItem("room").value || "",
        course: form.elements.namedItem("course").value,
        feeStatus: "Pending"
    };

    try {
        const response = await fetch(`${API_URL}/add`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(residentData)
        });

        const result = await response.json();

        if (response.ok) {
            notify("Resident added successfully!");
            form.reset();
            loadResidents();
        } else {
            notify(result.message || result.error || "Failed to add resident");
        }

    } catch (error) {
        console.error(error);
        notify("Backend connection failed!");
    }
});


// Display residents from MongoDB
async function loadResidents() {
    try {
        const response = await fetch(`${API_URL}/all`);
        const residents = await response.json();

        if (!response.ok) {
            throw new Error("Unable to load residents");
        }

        const records = document.getElementById("records");
        records.innerHTML = "";

        residents.forEach(resident => {
            const tr = document.createElement("tr");

            [
                resident.name,
                resident.phone,
                resident.email,
                resident.roomNumber || "Not allocated",
                "Active"
            ].forEach(value => {
                const td = document.createElement("td");
                td.textContent = value;
                tr.appendChild(td);
            });

            records.appendChild(tr);
        });

        document.getElementById("residentTotal").textContent =
            residents.length;

    } catch (error) {
        console.error("Loading error:", error);
        notify("Unable to load residents");
    }
}

// Load saved residents when dashboard opens
loadResidents();
