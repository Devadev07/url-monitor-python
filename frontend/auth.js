const api = "http://127.0.0.1:8000";

async function login() {
    const res = await fetch(`${api}/login`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            username: document.getElementById("loginUsername").value,
            password: document.getElementById("loginPassword").value
        })
    });

    const data = await res.json();

    if (data.id) {
        localStorage.setItem("user_id", data.id);
        window.location.href = "dashboard.html";
    } else {
        alert(data.message);
    }
}

async function signup() {
    const res = await fetch(`${api}/signup`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            username: document.getElementById("signupUsername").value,
            password: document.getElementById("signupPassword").value
        })
    });

    const data = await res.json();

    alert(data.message || "Signup successful");
}