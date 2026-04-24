const api = "http://127.0.0.1:8000";

async function addUrl() {
    await fetch(`${api}/add-url`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({
            address: document.getElementById("urlAddress").value,
            check_interval: parseInt(document.getElementById("interval").value) || 5
        })
    });

    document.getElementById("urlAddress").value = "";
    document.getElementById("interval").value = "";

    getUrls();
}

async function getUrls() {
    const res = await fetch(`${api}/user-urls`, {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
        }
    });

    const data = await res.json();

    const tbody = document.querySelector("#urlTable tbody");
    tbody.innerHTML = "";

    data.forEach(url => {
        tbody.innerHTML += `
            <tr>
                <td>${url.id}</td>
                <td>${url.address}</td>
                <td>
                    ${
                        url.status === "UP"
                        ? '<span style="color:green;font-weight:bold;">UP</span>'
                        : url.status === "DOWN"
                        ? '<span style="color:red;font-weight:bold;">DOWN</span>'
                        : '<span style="color:orange;font-weight:bold;">UNKNOWN</span>'
                    }
                </td>
                <td>${url.response_time ? url.response_time + " ms" : "-"}</td>
                <td>${url.check_interval}</td>
                <td>${url.reason || "-"}</td>
                <td>
                    <div style="display:flex;flex-direction:column;gap:5px;align-items:center;">
                    <button onclick="checkUrl(${url.id})">Check</button>
                    <button onclick="deleteUrl(${url.id})">Delete</button>
                </td>
            </tr>
        `;
    });
}

async function deleteUrl(id) {
    await fetch(`${api}/delete-url/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
        }
    });

    getUrls();
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

async function refreshUrls() {
    await fetch(`${api}/check-all`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
        }
    });

    getUrls();
}

async function checkUrl(id) {
    await fetch(`${api}/check-url/${id}`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
        }
    });

    getUrls();
}

window.onload = getUrls;

setInterval(getUrls, 30000);

document.getElementById("welcomeUser").innerText =
    "Logged in as: " + localStorage.getItem("username");