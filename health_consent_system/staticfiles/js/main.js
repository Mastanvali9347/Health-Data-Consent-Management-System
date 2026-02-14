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
        setTimeout(() => t.remove(), 400)
    }, 3200)
}

const lockBtn = btn => {
    if (!btn) return
    btn.disabled = true
    btn.dataset.text = btn.innerText
    btn.innerText = "Processing..."
}

const unlockBtn = btn => {
    if (!btn) return
    btn.disabled = false
    btn.innerText = btn.dataset.text || "Submit"
}

const postJSON = async (url, data) => {
    const res = await fetch(API_BASE + url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        credentials: "include",
        body: JSON.stringify(data)
    })
    return res.json()
}

const postForm = async (url, data) => {
    const res = await fetch(API_BASE + url, {
        method: "POST",
        headers: { "X-CSRFToken": csrftoken },
        credentials: "include",
        body: data
    })
    return res.json()
}

const getJSON = async url => {
    const res = await fetch(API_BASE + url, { credentials: "include" })
    return res.json()
}

document.addEventListener("DOMContentLoaded", () => {

    const preloader = qs("#preloader")
    if (preloader) setTimeout(() => preloader.remove(), 1200)

    const toggle = qs(".menu-toggle")
    const sidebar = qs(".sidebar")
    const overlay = qs(".sidebar-overlay")

    if (toggle && sidebar && overlay) {
        toggle.onclick = () => {
            sidebar.classList.toggle("active")
            overlay.classList.toggle("active")
            document.body.style.overflow = sidebar.classList.contains("active") ? "hidden" : ""
        }

        overlay.onclick = () => {
            sidebar.classList.remove("active")
            overlay.classList.remove("active")
            document.body.style.overflow = ""
        }
    }

    document.addEventListener("keydown", e => {
        if (e.key === "Escape") {
            sidebar?.classList.remove("active")
            overlay?.classList.remove("active")
            document.body.style.overflow = ""
        }
    })

    window.addEventListener("resize", () => {
        if (window.innerWidth > 1024) {
            sidebar?.classList.remove("active")
            overlay?.classList.remove("active")
            document.body.style.overflow = ""
        }
    })

    const loginForm = qs("form[action='/auth/login/']")
    if (loginForm) {
        loginForm.onsubmit = () => {
            lockBtn(loginForm.querySelector("button"))
            return true
        }
    }

    const registerForm = qs("form[action='/auth/register/']")
    if (registerForm) {
        registerForm.onsubmit = () => {
            lockBtn(registerForm.querySelector("button"))
            return true
        }
    }

    const uploadForm = qs("form[action='/records/api/upload/']")
    if (uploadForm) {
        uploadForm.onsubmit = async e => {
            e.preventDefault()
            const btn = uploadForm.querySelector("button")
            lockBtn(btn)
            try {
                const res = await postForm("/records/api/upload/", new FormData(uploadForm))
                res?.message ? toast("Medical record uploaded successfully") : toast("Upload failed")
            } catch {
                toast("Network error")
            }
            unlockBtn(btn)
        }
    }

    const consentForm = qs("form[action='/consent/api/grant/']")
    if (consentForm) {
        consentForm.onsubmit = async e => {
            e.preventDefault()
            const btn = consentForm.querySelector("button")
            lockBtn(btn)
            try {
                const data = Object.fromEntries(new FormData(consentForm))
                const res = await postJSON("/consent/api/grant/", data)
                res?.message ? toast("Consent granted successfully") : toast("Consent failed")
            } catch {
                toast("Network error")
            }
            unlockBtn(btn)
        }
    }

    qsa("[data-record-id]").forEach(btn => {
        btn.onclick = async () => {
            btn.classList.add("loading")
            try {
                const res = await getJSON(`/records/doctor-access/${btn.dataset.recordId}/`)
                res?.message ? toast("Access granted") : toast("Access denied")
            } catch {
                toast("Access error")
            }
            btn.classList.remove("loading")
        }
    })

    const emergencyForm = qs("form[action='/emergency/api/start/']")
    if (emergencyForm) {
        emergencyForm.onsubmit = async e => {
            e.preventDefault()
            const btn = emergencyForm.querySelector("button")
            lockBtn(btn)
            try {
                const data = Object.fromEntries(new FormData(emergencyForm))
                const res = await postJSON("/emergency/api/start/", data)
                res?.message ? toast("Emergency access activated") : toast("Emergency request failed")
            } catch {
                toast("Network error")
            }
            unlockBtn(btn)
        }
    }

    const notifyBox = qs(".notification-list")
    if (notifyBox) {
        getJSON("/notifications/")
            .then(list => {
                notifyBox.innerHTML = ""
                list.forEach(n => {
                    const d = document.createElement("div")
                    d.className = "notification-card"
                    d.innerHTML = `
                        <div class="notification-content">
                            <strong>${n.message}</strong>
                            <small>${new Date(n.created_at).toLocaleString()}</small>
                        </div>
                    `
                    notifyBox.appendChild(d)
                })
            })
            .catch(() => toast("Failed to load notifications"))
    }

})
