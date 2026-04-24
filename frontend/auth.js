const api = "http://127.0.0.1:8000";

async function login() {
    const res = await fetch(`${api}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: document.getElementById("loginUsername").value,
            password: document.getElementById("loginPassword").value
        })
    });

    const data = await res.json();

    if (data.access_token) {
        localStorage.setItem("token", data.access_token);

        localStorage.setItem(
            "username",
            document.getElementById("loginUsername").value
        );

        alert("Login successful");

        window.location.href = "dashboard.html";
    } else {
        alert("Login failed");
    }
}

async function signup() {
    const res = await fetch(`${api}/signup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: document.getElementById("signupUsername").value,
            password: document.getElementById("signupPassword").value
        })
    });

    const data = await res.json();

    if (res.ok) {
        alert("Signup successful");
    } else {
        alert(data.detail);
    }
}