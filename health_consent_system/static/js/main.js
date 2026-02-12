const API_BASE = window.location.origin;

const qs = s => document.querySelector(s);
const qsa = s => document.querySelectorAll(s);

const csrftoken = qs("#csrf-token") ? qs("#csrf-token").value : "";

const toast = msg => {
    const t = document.createElement("div");
    t.className = "toast";
    t.innerText = msg;
    document.body.appendChild(t);
    setTimeout(() => t.classList.add("show"), 50);
    setTimeout(() => {
        t.classList.remove("show");
        t.remove();
    }, 3000);
};

const postJSON = async (url, data) => {
    const r = await fetch(API_BASE + url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        credentials: "include",
        body: JSON.stringify(data)
    });
    return r.json();
};

const postForm = async (url, formData) => {
    const r = await fetch(API_BASE + url, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        credentials: "include",
        body: formData
    });
    return r.json();
};

const getJSON = async url => {
    const r = await fetch(API_BASE + url, {
        method: "GET",
        credentials: "include"
    });
    return r.json();
};

document.addEventListener("DOMContentLoaded", () => {

    const preloader = qs("#preloader");
    if (preloader) setTimeout(() => preloader.remove(), 1500);

    const toggle = qs(".menu-toggle");
    const sidebar = qs(".sidebar");
    if (toggle && sidebar) {
        toggle.onclick = () => sidebar.classList.toggle("open");
    }

    const loginForm = qs("form[action='/auth/login/']");
    if (loginForm) {
        loginForm.onsubmit = async e => {
            e.preventDefault();
            const data = Object.fromEntries(new FormData(loginForm));
            const res = await postJSON("/auth/login/", data);
            if (res.message) {
                toast("Login successful");
                setTimeout(() => window.location.href = "/records/dashboard/", 800);
            } else toast("Login failed");
        };
    }

    const registerForm = qs("form[action='/auth/register/']");
    if (registerForm) {
        registerForm.onsubmit = async e => {
            e.preventDefault();
            const data = Object.fromEntries(new FormData(registerForm));
            const res = await postJSON("/auth/register/", data);
            if (res.message) {
                toast("Registration successful");
                setTimeout(() => window.location.href = "/auth/login/", 800);
            } else toast("Registration failed");
        };
    }

    const uploadForm = qs("form[action='/records/api/upload/']");
    if (uploadForm) {
        uploadForm.onsubmit = async e => {
            e.preventDefault();
            const res = await postForm("/records/api/upload/", new FormData(uploadForm));
            if (res.message) toast("Record uploaded successfully");
            else toast("Upload failed");
        };
    }

    const consentForm = qs("form[action='/consent/api/grant/']");
    if (consentForm) {
        consentForm.onsubmit = async e => {
            e.preventDefault();
            const data = Object.fromEntries(new FormData(consentForm));
            const res = await postJSON("/consent/api/grant/", data);
            if (res.message) toast("Consent granted");
            else toast("Consent failed");
        };
    }

    qsa("[data-record-id]").forEach(btn => {
        btn.onclick = async () => {
            const id = btn.dataset.recordId;
            const res = await getJSON(`/records/doctor-access/${id}/`);
            if (res.message) toast("Access granted");
            else toast("Access denied");
        };
    });

    const emergencyForm = qs("form[action='/emergency/api/start/']");
    if (emergencyForm) {
        emergencyForm.onsubmit = async e => {
            e.preventDefault();
            const data = Object.fromEntries(new FormData(emergencyForm));
            const res = await postJSON("/emergency/api/start/", data);
            if (res.message) toast("Emergency access activated");
            else toast("Emergency access failed");
        };
    }

    const notificationsBox = qs(".notification-list");
    if (notificationsBox) {
        getJSON("/notifications/my/").then(list => {
            notificationsBox.innerHTML = "";
            list.forEach(n => {
                const d = document.createElement("div");
                d.className = "notification-card";
                d.innerHTML = `<strong>${n.message}</strong><br><small>${n.created_at}</small>`;
                notificationsBox.appendChild(d);
            });
        });
    }

});
