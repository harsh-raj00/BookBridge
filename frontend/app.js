/* ═══════════════════════════════════════════════════════════════════
   BookBridge — Frontend Application Logic
   Handles auth, navigation, API calls, and UI state management
   ═══════════════════════════════════════════════════════════════════ */

const API_BASE = "http://127.0.0.1:8000";

// ─── State ─────────────────────────────────────────────────────────
let state = {
    token: localStorage.getItem("bb_token") || null,
    user: JSON.parse(localStorage.getItem("bb_user") || "null"),
    currentSection: "dashboard",
    booksPage: 1,
    resourcesPage: 1,
};

// ─── Init on Load ──────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    if (state.token && state.user) {
        showApp();
    }
});

// ═══════════════════════════════════════════════════════════════════
//  AUTH
// ═══════════════════════════════════════════════════════════════════

function switchAuthTab(tab) {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const tabs = document.querySelectorAll(".auth-tab");
    const footer = document.getElementById("authFooterText");

    tabs.forEach(t => t.classList.remove("active"));

    if (tab === "login") {
        loginForm.classList.remove("hidden");
        registerForm.classList.add("hidden");
        tabs[0].classList.add("active");
        footer.innerHTML = `Don't have an account? <a href="#" onclick="switchAuthTab('register')">Sign up</a>`;
    } else {
        loginForm.classList.add("hidden");
        registerForm.classList.remove("hidden");
        tabs[1].classList.add("active");
        footer.innerHTML = `Already have an account? <a href="#" onclick="switchAuthTab('login')">Login</a>`;
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const btn = document.getElementById("loginBtn");
    btn.disabled = true;
    btn.textContent = "Logging in...";

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: document.getElementById("loginEmail").value,
                password: document.getElementById("loginPassword").value,
            }),
        });

        const data = await res.json();

        if (!res.ok) throw new Error(data.detail || "Login failed");

        state.token = data.access_token;
        state.user = data.user;
        localStorage.setItem("bb_token", data.access_token);
        localStorage.setItem("bb_user", JSON.stringify(data.user));

        showToast("Welcome back! 🎉", "success");
        showApp();
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "Login";
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const btn = document.getElementById("regBtn");
    btn.disabled = true;
    btn.textContent = "Creating account...";

    try {
        const res = await fetch(`${API_BASE}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: document.getElementById("regName").value,
                email: document.getElementById("regEmail").value,
                password: document.getElementById("regPassword").value,
            }),
        });

        const data = await res.json();

        if (!res.ok) throw new Error(data.detail || "Registration failed");

        showToast("Account created! Please login. ✅", "success");
        switchAuthTab("login");
        document.getElementById("loginEmail").value = document.getElementById("regEmail").value;
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "Create Account";
    }
}

function logout() {
    state.token = null;
    state.user = null;
    localStorage.removeItem("bb_token");
    localStorage.removeItem("bb_user");
    document.getElementById("appPage").classList.add("hidden");
    document.getElementById("authPage").classList.remove("hidden");
    showToast("Logged out successfully", "info");
}

// ═══════════════════════════════════════════════════════════════════
//  APP NAVIGATION
// ═══════════════════════════════════════════════════════════════════

function showApp() {
    document.getElementById("authPage").classList.add("hidden");
    document.getElementById("appPage").classList.remove("hidden");
    document.getElementById("navUserName").textContent = state.user?.name || "";
    document.getElementById("heroUserName").textContent = state.user?.name?.split(" ")[0] || "";
    showSection("dashboard");
}

function showSection(section) {
    state.currentSection = section;

    // Hide all sections
    ["dashboardSection", "buySection", "sellSection", "vaultSection"].forEach(id => {
        document.getElementById(id).classList.add("hidden");
    });

    // Update nav active state
    document.querySelectorAll(".nav-link").forEach(link => {
        link.classList.toggle("active", link.dataset.section === section);
    });

    // Show selected section
    const sectionMap = {
        dashboard: "dashboardSection",
        buy: "buySection",
        sell: "sellSection",
        vault: "vaultSection",
    };

    document.getElementById(sectionMap[section]).classList.remove("hidden");

    // Load data for section
    if (section === "dashboard") loadDashboardStats();
    if (section === "buy") loadBooks();
    if (section === "sell") loadMyBooks();
    if (section === "vault") loadResources();
}

// ═══════════════════════════════════════════════════════════════════
//  API HELPERS
// ═══════════════════════════════════════════════════════════════════

function authHeaders() {
    return {
        Authorization: `Bearer ${state.token}`,
        "Content-Type": "application/json",
    };
}

function authHeadersMultipart() {
    return {
        Authorization: `Bearer ${state.token}`,
    };
}

async function apiGet(path) {
    const res = await fetch(`${API_BASE}${path}`, { headers: authHeaders() });
    if (res.status === 401) { logout(); throw new Error("Session expired"); }
    return res.json();
}

async function apiPost(path, body) {
    const res = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(body),
    });
    if (res.status === 401) { logout(); throw new Error("Session expired"); }
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Request failed");
    return data;
}

async function apiPut(path, body) {
    const res = await fetch(`${API_BASE}${path}`, {
        method: "PUT",
        headers: authHeaders(),
        body: JSON.stringify(body),
    });
    if (res.status === 401) { logout(); throw new Error("Session expired"); }
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Request failed");
    return data;
}

async function apiDelete(path) {
    const res = await fetch(`${API_BASE}${path}`, {
        method: "DELETE",
        headers: authHeaders(),
    });
    if (res.status === 401) { logout(); throw new Error("Session expired"); }
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Request failed");
    return data;
}

async function apiPostFormData(path, formData) {
    const res = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: authHeadersMultipart(),
        body: formData,
    });
    if (res.status === 401) { logout(); throw new Error("Session expired"); }
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Upload failed");
    return data;
}

// ═══════════════════════════════════════════════════════════════════
//  DASHBOARD
// ═══════════════════════════════════════════════════════════════════

async function loadDashboardStats() {
    try {
        const [booksData, myBooks, resourcesData, myUploads] = await Promise.all([
            apiGet("/books/?per_page=1"),
            apiGet("/books/my-listings"),
            apiGet("/resources/?per_page=1"),
            apiGet("/resources/my-uploads"),
        ]);

        document.getElementById("statTotalBooks").textContent = booksData.total || 0;
        document.getElementById("statMyBooks").textContent = myBooks.length || 0;
        document.getElementById("statResources").textContent = resourcesData.total || 0;
        document.getElementById("statMyUploads").textContent = myUploads.length || 0;
    } catch (err) {
        console.error("Failed to load stats:", err);
    }
}

// ═══════════════════════════════════════════════════════════════════
//  BOOKS — BROWSE (BUY)
// ═══════════════════════════════════════════════════════════════════

let booksDebounce;
function debouncedLoadBooks() {
    clearTimeout(booksDebounce);
    booksDebounce = setTimeout(() => { state.booksPage = 1; loadBooks(); }, 400);
}

async function loadBooks() {
    const grid = document.getElementById("booksGrid");
    grid.innerHTML = `<div class="loading-overlay"><div class="spinner"></div></div>`;

    try {
        const params = new URLSearchParams();
        const search = document.getElementById("buySearch").value;
        const category = document.getElementById("buyCategory").value;
        const condition = document.getElementById("buyCondition").value;
        const maxPrice = document.getElementById("buyMaxPrice").value;

        if (search) params.set("search", search);
        if (category) params.set("category", category);
        if (condition) params.set("condition", condition);
        if (maxPrice) params.set("max_price", maxPrice);
        params.set("page", state.booksPage);
        params.set("per_page", 12);

        const data = await apiGet(`/books/?${params.toString()}`);

        if (data.books.length === 0) {
            grid.innerHTML = `
                <div class="empty-state" style="grid-column:1/-1;">
                    <div class="empty-state-icon">📚</div>
                    <h3>No books found</h3>
                    <p>Try changing your filters or search term</p>
                </div>`;
        } else {
            grid.innerHTML = data.books.map(book => renderBookCard(book)).join("");
        }

        renderPagination("booksPagination", data, (page) => {
            state.booksPage = page;
            loadBooks();
        });
    } catch (err) {
        grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;"><p>Error loading books</p></div>`;
    }
}

function renderBookCard(book) {
    const conditionLabels = {
        new: "New", like_new: "Like New", good: "Good", fair: "Fair", poor: "Poor"
    };
    const categoryLabels = {
        engineering: "Engineering", medical: "Medical", competitive: "Competitive",
        school: "School", arts: "Arts", science: "Science", commerce: "Commerce",
        law: "Law", other: "Other"
    };
    const bookIcons = {
        engineering: "⚙️", medical: "🏥", competitive: "🏆", school: "🏫",
        arts: "🎨", science: "🔬", commerce: "💼", law: "⚖️", other: "📖"
    };

    return `
        <div class="book-card">
            <div class="book-card-image">
                ${bookIcons[book.category] || "📖"}
                <span class="book-condition-badge">${conditionLabels[book.condition] || book.condition}</span>
            </div>
            <div class="book-card-body">
                <h3 title="${book.title}">${book.title}</h3>
                <p class="author">by ${book.author}</p>
                <span class="category-tag">${categoryLabels[book.category] || book.category}</span>
                ${book.subject ? `<span class="category-tag" style="margin-left:4px">${book.subject}</span>` : ""}
            </div>
            <div class="book-card-footer">
                <span class="book-price">₹${book.price}</span>
                <button class="btn btn-sm btn-secondary" onclick="viewBookDetails(${book.id})">View Details</button>
            </div>
        </div>`;
}

async function viewBookDetails(bookId) {
    try {
        const book = await apiGet(`/books/${bookId}`);
        const conditionLabels = { new: "New", like_new: "Like New", good: "Good", fair: "Fair", poor: "Poor" };

        const modal = document.getElementById("sellModal");
        const modalContent = modal.querySelector(".modal");

        modalContent.innerHTML = `
            <div class="modal-header">
                <h2>📖 Book Details</h2>
                <button class="modal-close" onclick="closeModal('sellModal')">&times;</button>
            </div>
            <div style="margin-bottom:16px;">
                <h3 style="font-size:1.3rem;margin-bottom:4px;">${book.title}</h3>
                <p class="text-muted">by ${book.author}</p>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;">
                <div class="stat-card" style="text-align:left;padding:12px 16px;">
                    <div class="stat-label">Price</div>
                    <div style="font-size:1.3rem;font-weight:700;color:var(--accent);">₹${book.price}</div>
                </div>
                <div class="stat-card" style="text-align:left;padding:12px 16px;">
                    <div class="stat-label">Condition</div>
                    <div style="font-size:1rem;font-weight:600;">${conditionLabels[book.condition] || book.condition}</div>
                </div>
            </div>
            ${book.description ? `<div style="margin-bottom:16px;"><strong>Description</strong><p class="text-muted" style="margin-top:4px;">${book.description}</p></div>` : ""}
            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;">
                ${book.subject ? `<span class="tag">${book.subject}</span>` : ""}
                ${book.semester ? `<span class="tag">Sem ${book.semester}</span>` : ""}
                ${book.isbn ? `<span class="tag">ISBN: ${book.isbn}</span>` : ""}
                ${book.edition ? `<span class="tag">${book.edition} Ed.</span>` : ""}
            </div>
            <button class="btn btn-primary btn-lg" style="width:100%;" onclick="closeModal('sellModal')">Close</button>
        `;
        openModal("sellModal");
    } catch (err) {
        showToast("Failed to load book details", "error");
    }
}

// ═══════════════════════════════════════════════════════════════════
//  BOOKS — MY LISTINGS (SELL)
// ═══════════════════════════════════════════════════════════════════

async function loadMyBooks() {
    const grid = document.getElementById("myBooksGrid");
    const empty = document.getElementById("myBooksEmpty");

    grid.innerHTML = `<div class="loading-overlay" style="grid-column:1/-1;"><div class="spinner"></div></div>`;
    empty.classList.add("hidden");

    try {
        const books = await apiGet("/books/my-listings");

        if (books.length === 0) {
            grid.innerHTML = "";
            empty.classList.remove("hidden");
        } else {
            grid.innerHTML = books.map(book => renderMyBookCard(book)).join("");
        }
    } catch (err) {
        grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;"><p>Error loading your books</p></div>`;
    }
}

function renderMyBookCard(book) {
    const conditionLabels = { new: "New", like_new: "Like New", good: "Good", fair: "Fair", poor: "Poor" };

    return `
        <div class="book-card">
            <div class="book-card-image">
                📖
                <span class="book-condition-badge">${conditionLabels[book.condition] || book.condition}</span>
            </div>
            <div class="book-card-body">
                <h3 title="${book.title}">${book.title}</h3>
                <p class="author">by ${book.author}</p>
                <span class="category-tag">${book.category}</span>
                <span style="margin-left:8px;color:${book.is_available ? 'var(--success)' : 'var(--danger)'};font-size:0.8rem;font-weight:600;">
                    ${book.is_available ? "● Available" : "● Sold"}
                </span>
            </div>
            <div class="book-card-footer">
                <span class="book-price">₹${book.price}</span>
                <div class="flex gap-sm">
                    <button class="btn btn-sm btn-secondary" onclick="editBook(${book.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteBook(${book.id})">Delete</button>
                </div>
            </div>
        </div>`;
}

function openSellModal(book = null) {
    const title = document.getElementById("sellModalTitle");
    const submitBtn = document.getElementById("sellSubmitBtn");

    // Reset the modal content to the form
    const modal = document.getElementById("sellModal").querySelector(".modal");
    modal.innerHTML = `
        <div class="modal-header">
            <h2 id="sellModalTitle">${book ? "Edit Book" : "List a Book for Sale"}</h2>
            <button class="modal-close" onclick="closeModal('sellModal')">&times;</button>
        </div>
        <form onsubmit="handleSellBook(event)">
            <div class="form-group">
                <label>Book Title *</label>
                <input type="text" class="form-input" id="sellTitle" placeholder="e.g. Engineering Mathematics" required value="${book?.title || ""}">
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Author *</label>
                    <input type="text" class="form-input" id="sellAuthor" placeholder="Author name" required value="${book?.author || ""}">
                </div>
                <div class="form-group">
                    <label>Price (₹) *</label>
                    <input type="number" class="form-input" id="sellPrice" placeholder="250" required min="0" value="${book?.price || ""}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Category</label>
                    <select class="form-select" id="sellCategory">
                        ${["engineering", "medical", "competitive", "school", "arts", "science", "commerce", "law", "other"].map(c =>
        `<option value="${c}" ${book?.category === c ? "selected" : ""}>${c.charAt(0).toUpperCase() + c.slice(1)}</option>`
    ).join("")}
                    </select>
                </div>
                <div class="form-group">
                    <label>Condition</label>
                    <select class="form-select" id="sellCondition">
                        ${[["new", "New"], ["like_new", "Like New"], ["good", "Good"], ["fair", "Fair"], ["poor", "Poor"]].map(([v, l]) =>
        `<option value="${v}" ${(book?.condition || "good") === v ? "selected" : ""}>${l}</option>`
    ).join("")}
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Subject</label>
                    <input type="text" class="form-input" id="sellSubject" placeholder="e.g. Mathematics" value="${book?.subject || ""}">
                </div>
                <div class="form-group">
                    <label>Semester</label>
                    <input type="text" class="form-input" id="sellSemester" placeholder="e.g. 3rd" value="${book?.semester || ""}">
                </div>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea class="form-textarea" id="sellDescription" placeholder="Describe the book's condition, edition, etc.">${book?.description || ""}</textarea>
            </div>
            <input type="hidden" id="sellBookId" value="${book?.id || ""}">
            <button type="submit" class="btn btn-primary btn-lg" style="width:100%;" id="sellSubmitBtn">${book ? "Update Book" : "List Book"}</button>
        </form>
    `;

    openModal("sellModal");
}

async function editBook(bookId) {
    try {
        const book = await apiGet(`/books/${bookId}`);
        openSellModal(book);
    } catch (err) {
        showToast("Failed to load book", "error");
    }
}

async function handleSellBook(e) {
    e.preventDefault();
    const btn = document.getElementById("sellSubmitBtn");
    btn.disabled = true;
    btn.textContent = "Saving...";

    const bookId = document.getElementById("sellBookId").value;
    const bookData = {
        title: document.getElementById("sellTitle").value,
        author: document.getElementById("sellAuthor").value,
        price: parseFloat(document.getElementById("sellPrice").value),
        category: document.getElementById("sellCategory").value,
        condition: document.getElementById("sellCondition").value,
        subject: document.getElementById("sellSubject").value,
        semester: document.getElementById("sellSemester").value,
        description: document.getElementById("sellDescription").value,
    };

    try {
        if (bookId) {
            await apiPut(`/books/${bookId}`, bookData);
            showToast("Book updated successfully! ✅", "success");
        } else {
            await apiPost("/books/", bookData);
            showToast("Book listed successfully! 🎉", "success");
        }
        closeModal("sellModal");
        loadMyBooks();
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.textContent = bookId ? "Update Book" : "List Book";
    }
}

async function deleteBook(bookId) {
    if (!confirm("Are you sure you want to delete this listing?")) return;

    try {
        await apiDelete(`/books/${bookId}`);
        showToast("Book deleted! 🗑️", "success");
        loadMyBooks();
    } catch (err) {
        showToast(err.message, "error");
    }
}

// ═══════════════════════════════════════════════════════════════════
//  RESOURCES — STUDYVAULT
// ═══════════════════════════════════════════════════════════════════

let resourcesDebounce;
function debouncedLoadResources() {
    clearTimeout(resourcesDebounce);
    resourcesDebounce = setTimeout(() => { state.resourcesPage = 1; loadResources(); }, 400);
}

async function loadResources() {
    const grid = document.getElementById("resourcesGrid");
    grid.innerHTML = `<div class="loading-overlay" style="grid-column:1/-1;"><div class="spinner"></div></div>`;

    try {
        const params = new URLSearchParams();
        const search = document.getElementById("vaultSearch").value;
        const fileType = document.getElementById("vaultType").value;
        const subject = document.getElementById("vaultSubject").value;

        if (search) params.set("search", search);
        if (fileType) params.set("file_type", fileType);
        if (subject) params.set("subject", subject);
        params.set("page", state.resourcesPage);
        params.set("per_page", 12);

        const data = await apiGet(`/resources/?${params.toString()}`);

        if (data.resources.length === 0) {
            grid.innerHTML = `
                <div class="empty-state" style="grid-column:1/-1;">
                    <div class="empty-state-icon">📝</div>
                    <h3>No resources found</h3>
                    <p>Be the first to upload study resources!</p>
                </div>`;
        } else {
            grid.innerHTML = data.resources.map(r => renderResourceCard(r)).join("");
        }

        renderPagination("resourcesPagination", data, (page) => {
            state.resourcesPage = page;
            loadResources();
        });
    } catch (err) {
        grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;"><p>Error loading resources</p></div>`;
    }
}

function renderResourceCard(r) {
    const typeIcons = {
        notes: "📝", pdf: "📄", assignment: "📋", question_paper: "❓",
        solution: "✅", presentation: "📊", other: "📁"
    };
    const typeLabels = {
        notes: "Notes", pdf: "PDF", assignment: "Assignment", question_paper: "Question Paper",
        solution: "Solution", presentation: "Presentation", other: "Other"
    };

    const tags = r.tags ? r.tags.split(",").filter(t => t.trim()).map(t => `<span class="tag">${t.trim()}</span>`).join("") : "";

    return `
        <div class="resource-card">
            <div class="resource-header">
                <div class="resource-icon">${typeIcons[r.file_type] || "📁"}</div>
                <div>
                    <h3>${r.title}</h3>
                    <span class="category-tag" style="font-size:0.7rem;margin-top:4px;display:inline-block;">${typeLabels[r.file_type] || r.file_type}</span>
                </div>
            </div>
            ${r.description ? `<p class="text-muted" style="font-size:0.85rem;margin-bottom:8px;">${r.description.substring(0, 100)}${r.description.length > 100 ? "..." : ""}</p>` : ""}
            <div class="resource-meta">
                ${r.subject ? `<span>📖 ${r.subject}</span>` : ""}
                ${r.semester ? `<span>📅 Sem ${r.semester}</span>` : ""}
                ${r.category ? `<span>📂 ${r.category}</span>` : ""}
            </div>
            ${tags ? `<div class="resource-tags">${tags}</div>` : ""}
            <div class="resource-footer">
                <span class="download-count">⬇️ ${r.download_count} downloads</span>
                <button class="btn btn-sm btn-primary" onclick="downloadResource(${r.id})">Download</button>
            </div>
        </div>`;
}

function openUploadModal() {
    openModal("uploadModal");
}

async function handleUploadResource(e) {
    e.preventDefault();
    const btn = document.getElementById("uploadSubmitBtn");
    btn.disabled = true;
    btn.textContent = "Uploading...";

    try {
        const formData = new FormData();
        formData.append("file", document.getElementById("uploadFile").files[0]);
        formData.append("title", document.getElementById("uploadTitle").value);
        formData.append("description", document.getElementById("uploadDescription").value);
        formData.append("file_type", document.getElementById("uploadType").value);
        formData.append("category", document.getElementById("uploadCategory").value);
        formData.append("subject", document.getElementById("uploadSubject").value);
        formData.append("semester", document.getElementById("uploadSemester").value);
        formData.append("tags", document.getElementById("uploadTags").value);

        await apiPostFormData("/resources/upload", formData);
        showToast("Resource uploaded successfully! 🎉", "success");
        closeModal("uploadModal");
        e.target.reset();
        loadResources();
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "Upload Resource";
    }
}

function downloadResource(id) {
    window.open(`${API_BASE}/resources/${id}/download`, "_blank");
}

// ═══════════════════════════════════════════════════════════════════
//  MODAL HELPERS
// ═══════════════════════════════════════════════════════════════════

function openModal(id) {
    document.getElementById(id).classList.add("active");
    document.body.style.overflow = "hidden";
}

function closeModal(id) {
    document.getElementById(id).classList.remove("active");
    document.body.style.overflow = "";
}

// Close modal on overlay click
document.querySelectorAll(".modal-overlay").forEach(overlay => {
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) {
            overlay.classList.remove("active");
            document.body.style.overflow = "";
        }
    });
});

// Close modal on Escape key
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        document.querySelectorAll(".modal-overlay.active").forEach(m => {
            m.classList.remove("active");
        });
        document.body.style.overflow = "";
    }
});

// ═══════════════════════════════════════════════════════════════════
//  PAGINATION
// ═══════════════════════════════════════════════════════════════════

function renderPagination(containerId, data, onPageChange) {
    const container = document.getElementById(containerId);
    const { page, total_pages } = data;

    if (total_pages <= 1) {
        container.innerHTML = "";
        return;
    }

    let html = "";
    html += `<button ${page <= 1 ? "disabled" : ""} onclick="void(0)">← Prev</button>`;

    for (let i = 1; i <= total_pages; i++) {
        if (i === page) {
            html += `<button class="current-page">${i}</button>`;
        } else if (i === 1 || i === total_pages || Math.abs(i - page) <= 2) {
            html += `<button onclick="void(0)">${i}</button>`;
        } else if (Math.abs(i - page) === 3) {
            html += `<button disabled>...</button>`;
        }
    }

    html += `<button ${page >= total_pages ? "disabled" : ""} onclick="void(0)">Next →</button>`;

    container.innerHTML = html;

    // Attach click handlers
    container.querySelectorAll("button:not(:disabled):not(.current-page)").forEach(btn => {
        btn.addEventListener("click", () => {
            const text = btn.textContent.trim();
            if (text === "← Prev") onPageChange(page - 1);
            else if (text === "Next →") onPageChange(page + 1);
            else onPageChange(parseInt(text));
        });
    });
}

// ═══════════════════════════════════════════════════════════════════
//  TOAST NOTIFICATIONS
// ═══════════════════════════════════════════════════════════════════

function showToast(message, type = "info") {
    const container = document.getElementById("toastContainer");
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(100%)";
        toast.style.transition = "all 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}
