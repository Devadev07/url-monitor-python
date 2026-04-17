const api = "http://127.0.0.1:8000";

async function addUrl() {
    const user_id = localStorage.getItem("user_id");

    await fetch(`${api}/add-url`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            address: document.getElementById("urlAddress").value,
            user_id: parseInt(user_id)
        })
    });

    document.getElementById("urlAddress").value = "";
    getUrls();
}

async function getUrls() {
    const user_id = localStorage.getItem("user_id");

    const res = await fetch(`${api}/user-urls/${user_id}`);
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
                <td>
                    <button onclick="deleteUrl(${url.id})">Delete</button>
                </td>
            </tr>
        `;
    });
}

async function checkUrl() {
    const id = document.getElementById("checkId").value;

    if (!id) {
        alert("Enter URL ID");
        return;
    }

    const res = await fetch(`${api}/check-url/${id}`, {
        method: "POST"
    });

    if (!res.ok) {
        alert("Invalid URL ID or URL not found");
        return;
    }

    document.getElementById("checkId").value = "";
    getUrls();
}

async function deleteUrl(id) {
    await fetch(`${api}/delete-url/${id}`, {
        method: "DELETE"
    });

    getUrls();
}

function logout() {
    localStorage.removeItem("user_id");
    window.location.href = "login.html";
}

async function refreshUrls() {
    await fetch(`${api}/check-all`, {
        method: "POST"
    });

    getUrls();
}

window.onload = getUrls;