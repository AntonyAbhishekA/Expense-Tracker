// ===========================================
// Analytics page charts
// 4 visualizations: category, monthly trend,
// payment method distribution, top 5 categories
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
    new Chart(document.getElementById("categoryChart"), {
        type: "pie",
        data: {
            labels: data.labels,
            datasets: [{ data: data.values, backgroundColor: CHART_COLORS, borderColor: "#fff", borderWidth: 2 }]
        },
        options: { responsive: true, plugins: { legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } } } }
    });
}

async function renderMonthlyChart() {
    const res = await fetch("/api/monthly-data");
    const data = await res.json();
    new Chart(document.getElementById("monthlyChart"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Spending",
                data: data.values,
                borderColor: "#4f46e5",
                backgroundColor: "rgba(79,70,229,0.1)",
                fill: true,
                tension: 0.3,
                pointRadius: 4
            }]
        },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
    });
}

async function renderPaymentChart() {
    const res = await fetch("/api/payment-method-data");
    const data = await res.json();
    new Chart(document.getElementById("paymentChart"), {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{ label: "Amount Spent", data: data.values, backgroundColor: "#06b6d4", borderRadius: 6 }]
        },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
    });
}

async function renderTopCategoriesChart() {
    const res = await fetch("/api/top-categories");
    const data = await res.json();
    new Chart(document.getElementById("topCategoriesChart"), {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{ label: "Total Spent", data: data.values, backgroundColor: CHART_COLORS, borderRadius: 6 }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { x: { beginAtZero: true } }
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadInsights();
    renderCategoryChart();
    renderMonthlyChart();
    renderPaymentChart();
    renderTopCategoriesChart();
});
