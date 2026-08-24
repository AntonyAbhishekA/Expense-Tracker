// ===========================================
// General site interactivity
// (mobile nav toggle + delete confirmation)
// ===========================================

document.addEventListener("DOMContentLoaded", () => {
    // Mobile nav toggle
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");
    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            navLinks.classList.toggle("open");
        });
    }

    // Confirm before deleting an expense
    document.querySelectorAll(".delete-form").forEach((form) => {
        form.addEventListener("submit", (e) => {
            const title = form.dataset.title || "this expense";
            const confirmed = window.confirm(`Delete "${title}"? This cannot be undone.`);
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    // Auto-dismiss flash messages after a few seconds
    document.querySelectorAll(".flash").forEach((flash) => {
        setTimeout(() => {
            flash.style.transition = "opacity 0.4s";
            flash.style.opacity = "0";
            setTimeout(() => flash.remove(), 400);
        }, 4000);
    });
});
