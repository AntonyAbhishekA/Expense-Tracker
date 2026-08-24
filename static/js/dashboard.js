// ===========================================
// Dashboard charts + insights
// Fetches data from Flask's /api endpoints
// (which use pandas under the hood) and
// renders them with Chart.js
// ===========================================

const CHART_COLORS = [
    "#4f46e5", "#06b6d4", "#f59e0b", "#ef4444",
    "#10b981", "#8b5cf6", "#ec4899", "#84cc16"
];

async function loadInsights() {
    try {
        const res = await fetch("/api/summary");
        const data = await res.json();
        const list = document.getElementById("insightsList");
        list.innerHTML = "";
        data.insights.forEach((text) => {
            const li = document.createElement("li");
            li.textContent = text;
            list.appendChild(li);
        });
    } catch (err) {
        console.error("Failed to load insights:", err);
    }
}

async function renderCategoryChart() {
    const res = await fetch("/api/category-data");
    const data = await res.json();
    const ctx = document.getElementById("categoryChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: CHART_COLORS,
                borderWidth: 2,
                borderColor: "#fff"
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } }
            }
        }
    });
}

async function renderMonthlyChart() {
    const res = await fetch("/api/monthly-data");
    const data = await res.json();
    const ctx = document.getElementById("monthlyChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Monthly Spending",
                data: data.values,
                borderColor: "#4f46e5",
                backgroundColor: "rgba(79,70,229,0.1)",
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: "#4f46e5"
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadInsights();
    renderCategoryChart();
    renderMonthlyChart();
});
