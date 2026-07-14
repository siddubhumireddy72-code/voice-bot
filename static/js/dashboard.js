// Voice Bot Dashboard JavaScript

const API_BASE = '/api';

// Dashboard initialization
document.addEventListener('DOMContentLoaded', function() {
    console.log('Voice Bot Dashboard initialized');
    initializeCharts();
    loadDashboardData();
});

// Initialize charts
function initializeCharts() {
    // Calls over time chart
    const callsCtx = document.getElementById('callsChart');
    if (callsCtx) {
        new Chart(callsCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Calls',
                    data: [12, 19, 3, 5, 2, 3, 9],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Status distribution chart
    const statusCtx = document.getElementById('statusChart');
    if (statusCtx) {
        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Answered', 'Missed', 'Pending'],
                datasets: [{
                    data: [65, 25, 10],
                    backgroundColor: [
                        '#28a745',
                        '#dc3545',
                        '#ffc107'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// Load dashboard data
function loadDashboardData() {
    fetch(`${API_BASE}/stats`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateStatistics(data.stats);
            }
        })
        .catch(error => console.error('Error loading stats:', error));
}

// Update statistics
function updateStatistics(stats) {
    console.log('Updating statistics:', stats);
    // Update UI with stats
}

// Auto-refresh dashboard
setInterval(loadDashboardData, 30000); // Refresh every 30 seconds

// Format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleString();
}

// Format duration
function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
        return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
        return `${minutes}m ${secs}s`;
    } else {
        return `${secs}s`;
    }
}
