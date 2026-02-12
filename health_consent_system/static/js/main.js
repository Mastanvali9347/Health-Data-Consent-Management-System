const API_BASE = window.location.origin

const qs = s => document.querySelector(s)
const qsa = s => document.querySelectorAll(s)

const csrftoken = qs("#csrf-token")?.value || ""

const toast = msg => {
    const t = document.createElement("div")
    t.className = "toast"
    t.innerText = msg
    document.body.appendChild(t)
    requestAnimationFrame(() => t.classList.add("show"))
    setTimeout(() => {
        t.classList.remove("show")
        setTimeout(() => t.remove(), 300)
    }, 3000)
}

const lockBtn = btn => {
    if (!btn) return
    btn.disabled = true
    btn.dataset.txt = btn.innerText
    btn.innerText = "Please wait..."
}

const unlockBtn = btn => {
    if (!btn) return
    btn.disabled = false
    btn.innerText = btn.dataset.txt
}

const postJSON = async (url, data) => {
    const r = await fetch(API_BASE + url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        credentials: "include",
        body: JSON.stringify(data)
    })
    return r.json()
}

const postForm = async (url, data) => {
    const r = await fetch(API_BASE + url, {
        method: "POST",
        headers: { "X-CSRFToken": csrftoken },
        credentials: "include",
        body: data
    })
    return r.json()
}

const getJSON = async url => {
    const r = await fetch(API_BASE + url, { credentials: "include" })
    return r.json()
}

document.addEventListener("DOMContentLoaded", () => {

    const preloader = qs("#preloader")
    if (preloader) setTimeout(() => preloader.remove(), 1200)

    const toggle = qs(".menu-toggle")
    const sidebar = qs(".sidebar")
    if (toggle && sidebar) {
        toggle.onclick = () => sidebar.classList.toggle("open")
    }

    document.addEventListener("keydown", e => {
        if (e.key === "Escape" && sidebar) sidebar.classList.remove("open")
    })

    /* ---------- LOGIN (HTML SUBMIT ONLY) ---------- */
    const loginForm = qs("form[action='/auth/login/']")
    if (loginForm) {
        loginForm.onsubmit = () => {
            lockBtn(loginForm.querySelector("button"))
            return true
        }
    }

    /* ---------- REGISTER (HTML SUBMIT ONLY) ---------- */
    const registerForm = qs("form[action='/auth/register/']")
    if (registerForm) {
        registerForm.onsubmit = () => {
            lockBtn(registerForm.querySelector("button"))
            return true
        }
    }

    /* ---------- UPLOAD MEDICAL RECORD ---------- */
    const uploadForm = qs("form[action='/records/api/upload/']")
    if (uploadForm) {
        uploadForm.onsubmit = async e => {
            e.preventDefault()
            const btn = uploadForm.querySelector("button")
            lockBtn(btn)
            const res = await postForm("/records/api/upload/", new FormData(uploadForm))
            unlockBtn(btn)
            res.message ? toast("Medical record uploaded") : toast("Upload failed")
        }
    }

    /* ---------- GRANT CONSENT ---------- */
    const consentForm = qs("form[action='/consent/api/grant/']")
    if (consentForm) {
        consentForm.onsubmit = async e => {
            e.preventDefault()
            const btn = consentForm.querySelector("button")
            lockBtn(btn)
            const data = Object.fromEntries(new FormData(consentForm))
            const res = await postJSON("/consent/api/grant/", data)
            unlockBtn(btn)
            res.message ? toast("Consent granted") : toast("Consent failed")
        }
    }

    /* ---------- DOCTOR ACCESS ---------- */
    qsa("[data-record-id]").forEach(btn => {
        btn.onclick = async () => {
            btn.classList.add("loading")
            const res = await getJSON(`/records/doctor-access/${btn.dataset.recordId}/`)
            btn.classList.remove("loading")
            res.message ? toast("Access granted") : toast("Access denied")
        }
    })

    /* ---------- EMERGENCY ACCESS ---------- */
    const emergencyForm = qs("form[action='/emergency/api/start/']")
    if (emergencyForm) {
        emergencyForm.onsubmit = async e => {
            e.preventDefault()
            const btn = emergencyForm.querySelector("button")
            lockBtn(btn)
            const data = Object.fromEntries(new FormData(emergencyForm))
            const res = await postJSON("/emergency/api/start/", data)
            unlockBtn(btn)
            res.message ? toast("Emergency access activated") : toast("Emergency failed")
        }
    }

    /* ---------- NOTIFICATIONS ---------- */
    const notifyBox = qs(".notification-list")
    if (notifyBox) {
        getJSON("/notifications/").then(list => {
            notifyBox.innerHTML = ""
            list.forEach(n => {
                const d = document.createElement("div")
                d.className = "notification-card"
                d.innerHTML = `<strong>${n.message}</strong><span>${new Date(n.created_at).toLocaleString()}</span>`
                notifyBox.appendChild(d)
            })
        })
    }

})
