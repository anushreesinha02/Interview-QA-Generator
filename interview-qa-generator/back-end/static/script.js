// script.js

document.addEventListener("DOMContentLoaded", async () => {

    // Dynamic base URL
    const API_BASE = window.location.origin.includes("localhost") || window.location.origin.includes("127.0.0.1")
        ? "http://127.0.0.1:5000"
        : "https://interview-qa-generator.onrender.com";

    // Auth logic
    const authContainer = document.getElementById("auth-container");
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const container = document.querySelector(".container");

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    document.getElementById("showSignup").onclick = e => {
        e.preventDefault();
        loginForm.style.display = "none";
        signupForm.style.display = "block";
    };
    document.getElementById("showLogin").onclick = e => {
        e.preventDefault();
        signupForm.style.display = "none";
        loginForm.style.display = "block";
    };

    document.getElementById("signupBtn").onclick = async () => {
        console.log("Signup clicked");
        const email = document.getElementById("signup-email").value;
        const password = document.getElementById("signup-password").value;
        if (!isValidEmail(email)) {
            document.getElementById("signup-error").innerText = "Please enter a valid email address.";
            return;
        }

        const res = await fetch(`${API_BASE}/api/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
            credentials: "include"
        });
        const data = await res.json();
        console.log(data);
        if (data.success) {
            authContainer.style.display = "none";
            container.style.display = "block";
        } else {
            document.getElementById("signup-error").innerText = data.error || "Signup failed";
        }
    };

    document.getElementById("loginBtn").onclick = async () => {
        console.log("Login clicked");
        const email = document.getElementById("login-email").value;
        const password = document.getElementById("login-password").value;
        if (!isValidEmail(email)) {
            document.getElementById("login-error").innerText = "Please enter a valid email address.";
            return;
        }

        const res = await fetch(`${API_BASE}/api/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
            credentials: "include"
        });
        const data = await res.json();
        console.log(data);
        if (data.success) {
            authContainer.style.display = "none";
            container.style.display = "block";
        } else {
            document.getElementById("login-error").innerText = data.error || "Login failed";
        }
    };

    // Tagify setup
    const input = document.querySelector('#tags-input');
    const tagify = new Tagify(input, {
        whitelist: [
            "Python", "JavaScript", "React", "Node.js", "Machine Learning",
            "Data Science", "SQL", "C++", "HR", "Frontend Developer", "Backend Developer"
        ],
        dropdown: {
            enabled: 1,
            fuzzySearch: true,
            position: 'text',
            highlightFirst: true
        }
    });

    const generateBtn = document.getElementById("generateBtn");
    const output = document.getElementById("output");

    generateBtn.addEventListener("click", async () => {
        const role = document.getElementById("role").value;
        const experience = document.getElementById("experience").value;
        const numQuestions = document.getElementById("numQuestions").value;
        const tags = tagify.value.map(tag => tag.value);

        if (!role || !experience || tags.length === 0) {
            output.innerHTML = "<p>Please fill all fields: role, experience, and at least one skill/tool.</p>";
            return;
        }

        container.style.display = "block";
        output.innerHTML = "<p>Generating questions...</p>";

        try {
            const response = await fetch(`${API_BASE}/api/generate`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                body: JSON.stringify({
                    role: role,
                    experience: experience,
                    tools: tags,
                    count: parseInt(numQuestions)
                })
            });

            if (!response.ok) {
                output.innerHTML = "<p style='color:red;'>Server error. Please try again.</p>";
                return;
            }

            const data = await response.json();
            if (data.result && Array.isArray(data.result)) {
                output.innerHTML = data.result.map((q, i) => `
                    <div class="question-block">
                        <h3>Q${i + 1}: ${q.question}</h3>
                        <p><strong>Answer:</strong> ${q.answer}</p>
                        <p><strong>Critique:</strong> ${q.critique}</p>
                    </div>
                `).join("");
            } else if (data.error) {
                output.innerHTML = `<p style="color:red;">${data.error}</p>`;
            } else {
                output.innerHTML = "<p>No questions generated. Try again.</p>";
            }
        } catch (error) {
            output.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
        }
    });

    // PDF Download
    document.getElementById("downloadPdfBtn").addEventListener("click", () => {
        if (!output.innerText.trim()) {
            alert("No Q&A to export!");
            return;
        }
        const doc = new window.jspdf.jsPDF();
        doc.setFontSize(14);
        doc.text("Interview Q&A", 10, 10);
        let y = 20;
        document.querySelectorAll('.question-block').forEach(block => {
            doc.text(block.innerText, 10, y);
            y += block.innerText.split('\n').length * 10 + 5;
            if (y > 270) { doc.addPage(); y = 20; }
        });
        doc.save("interview-qa.pdf");
    });

    // Share Q&A
    document.getElementById("shareBtn").addEventListener("click", async () => {
        if (!output.innerText.trim()) {
            alert("No Q&A to share!");
            return;
        }
        const text = Array.from(document.querySelectorAll('.question-block'))
            .map(block => block.innerText)
            .join('\n\n');
        if (navigator.share) {
            try {
                await navigator.share({ title: "Interview Q&A", text });
            } catch (e) {
                alert("Share cancelled or failed.");
            }
        } else {
            try {
                await navigator.clipboard.writeText(text);
                alert("Q&A copied to clipboard! You can now paste it anywhere.");
            } catch (err) {
                alert("Failed to copy Q&A.");
            }
        }
    });

    // Logout
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.onclick = () => {
            window.location.href = "index.html";
        };
    }
});
