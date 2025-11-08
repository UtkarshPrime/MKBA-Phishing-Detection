// Configuration
const API_URL = 'http://localhost:8000';

// State
let analysisHistory = JSON.parse(localStorage.getItem('analysisHistory')) || [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    initializeTabs();
    initializeForms();
    initializeExamples();
    initializeHistory();
});

// Navigation
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.page');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = link.dataset.page;

            // Update active nav link
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            // Show corresponding page
            pages.forEach(p => p.classList.remove('active'));
            document.getElementById(`${pageName}-page`).classList.add('active');

            // Load history if on history page
            if (pageName === 'history') {
                displayHistory();
            }
        });
    });
}

// Tabs
function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;

            // Update active tab button
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Show corresponding tab content
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });
}

// Forms
function initializeForms() {
    // URL Form
    const urlForm = document.getElementById('url-form');
    urlForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = document.getElementById('url-input').value.trim();
        if (url) {
            await analyzeURL(url);
        }
    });

    // Email Form
    const emailForm = document.getElementById('email-form');
    emailForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const content = document.getElementById('email-input').value.trim();
        if (content) {
            await analyzeEmail(content);
        }
    });

    // Close buttons
    document.getElementById('close-results').addEventListener('click', () => {
        document.getElementById('results-section').style.display = 'none';
    });

    document.getElementById('close-error').addEventListener('click', () => {
        document.getElementById('error-section').style.display = 'none';
    });
}

// Examples
function initializeExamples() {
    // URL examples
    document.querySelectorAll('.example-btn[data-url]').forEach(btn => {
        btn.addEventListener('click', () => {
            const url = btn.dataset.url;
            document.getElementById('url-input').value = url;
            analyzeURL(url);
        });
    });

    // Email examples
    document.querySelectorAll('.example-btn[data-email]').forEach(btn => {
        btn.addEventListener('click', () => {
            const email = btn.dataset.email;
            document.getElementById('email-input').value = email;
            analyzeEmail(email);
        });
    });
}

// Analyze URL
async function analyzeURL(url) {
    const btn = document.getElementById('url-analyze-btn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoader = btn.querySelector('.btn-loader');

    try {
        // Show loading state
        btn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'flex';
        hideResults();
        hideError();

        // Call API
        const response = await fetch(`${API_URL}/analyze/url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const result = await response.json();

        // Add to history
        addToHistory('url', url, result);

        // Display results
        displayResults('url', url, result);

    } catch (error) {
        console.error('Error analyzing URL:', error);
        showError('Failed to analyze URL. Make sure the API server is running on http://localhost:8000');
    } finally {
        // Reset button state
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Analyze Email
async function analyzeEmail(content) {
    const btn = document.getElementById('email-analyze-btn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoader = btn.querySelector('.btn-loader');

    try {
        // Show loading state
        btn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'flex';
        hideResults();
        hideError();

        // Call API
        const response = await fetch(`${API_URL}/analyze/email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: content })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const result = await response.json();

        // Add to history
        addToHistory('email', content, result);

        // Display results
        displayResults('email', content, result);

    } catch (error) {
        console.error('Error analyzing email:', error);
        showError('Failed to analyze email. Make sure the API server is running on http://localhost:8000');
    } finally {
        // Reset button state
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Display Results
function displayResults(type, input, result) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');

    // Determine status
    const classification = result.classification.toLowerCase();
    let statusIcon, statusClass, statusText;

    if (classification === 'phishing') {
        statusIcon = '🚨';
        statusClass = 'danger';
        statusText = 'Phishing Detected!';
    } else if (classification === 'suspicious') {
        statusIcon = '⚠️';
        statusClass = 'warning';
        statusText = 'Suspicious Content';
    } else {
        statusIcon = '✅';
        statusClass = 'safe';
        statusText = 'Appears Safe';
    }

    // Build features HTML
    let featuresHTML = '';
    if (result.features) {
        const featureEntries = Object.entries(result.features).slice(0, 8); // Show first 8 features
        featuresHTML = `
            <div class="features-details">
                <h4>Detected Features</h4>
                <div class="feature-grid">
                    ${featureEntries.map(([key, value]) => `
                        <div class="feature-box">
                            <div class="feature-name">${formatFeatureName(key)}</div>
                            <div class="feature-value">${formatFeatureValue(value)}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // Build results HTML
    resultsContent.innerHTML = `
        <div class="result-status">
            <div class="status-icon">${statusIcon}</div>
            <h3 class="status-title ${statusClass}">${statusText}</h3>
            
            <div class="score-display">
                <div class="score-label">Risk Score</div>
                <div class="score-value ${statusClass}">${result.score.toFixed(1)}<span style="font-size: 1.5rem;">/100</span></div>
            </div>

            <div class="result-message">
                <strong>${result.message}</strong>
            </div>

            <div style="margin-top: 1.5rem; padding: 1rem; background: var(--bg-light); border-radius: 8px; text-align: left;">
                <strong style="display: block; margin-bottom: 0.5rem;">Analyzed ${type === 'url' ? 'URL' : 'Email'}:</strong>
                <div style="word-break: break-all; color: var(--text-light); font-size: 14px;">
                    ${input.length > 200 ? input.substring(0, 200) + '...' : input}
                </div>
            </div>

            ${featuresHTML}
        </div>
    `;

    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Helper Functions
function formatFeatureName(name) {
    return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function formatFeatureValue(value) {
    if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No';
    }
    if (typeof value === 'number') {
        return value % 1 === 0 ? value : value.toFixed(2);
    }
    return value;
}

function hideResults() {
    document.getElementById('results-section').style.display = 'none';
}

function showError(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-section').style.display = 'block';
}

function hideError() {
    document.getElementById('error-section').style.display = 'none';
}

// History Management
function addToHistory(type, input, result) {
    const historyItem = {
        id: Date.now(),
        type: type,
        input: input,
        result: result,
        timestamp: new Date().toISOString()
    };

    analysisHistory.unshift(historyItem);

    // Keep only last 50 items
    if (analysisHistory.length > 50) {
        analysisHistory = analysisHistory.slice(0, 50);
    }

    localStorage.setItem('analysisHistory', JSON.stringify(analysisHistory));
}

function initializeHistory() {
    // Clear history button
    document.getElementById('clear-history').addEventListener('click', () => {
        if (confirm('Are you sure you want to clear all history?')) {
            analysisHistory = [];
            localStorage.removeItem('analysisHistory');
            displayHistory();
        }
    });

    // Filter
    document.getElementById('history-filter').addEventListener('change', displayHistory);
}

function displayHistory() {
    const historyList = document.getElementById('history-list');
    const emptyState = document.getElementById('empty-history');
    const filter = document.getElementById('history-filter').value;

    // Filter history
    let filteredHistory = analysisHistory;
    if (filter !== 'all') {
        if (filter === 'url' || filter === 'email') {
            filteredHistory = analysisHistory.filter(item => item.type === filter);
        } else {
            filteredHistory = analysisHistory.filter(item =>
                item.result.classification.toLowerCase() === filter
            );
        }
    }

    if (filteredHistory.length === 0) {
        historyList.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    historyList.style.display = 'flex';
    emptyState.style.display = 'none';

    historyList.innerHTML = filteredHistory.map(item => {
        const classification = item.result.classification.toLowerCase();
        const date = new Date(item.timestamp);
        const timeAgo = getTimeAgo(date);

        return `
            <div class="history-item">
                <div class="history-info">
                    <span class="history-type ${item.type}">${item.type}</span>
                    <div class="history-content">
                        ${item.input.length > 100 ? item.input.substring(0, 100) + '...' : item.input}
                    </div>
                    <div class="history-time">${timeAgo}</div>
                </div>
                <div class="history-result">
                    <div class="history-classification ${classification}">
                        ${item.result.classification}
                    </div>
                    <div class="history-score">
                        Score: ${item.result.score.toFixed(1)}/100
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);

    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;

    return date.toLocaleDateString();
}

// Check API Status on Load
async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_URL}/`, { method: 'GET' });
        if (response.ok) {
            console.log('✓ API server is running');
        }
    } catch (error) {
        console.warn('⚠ API server is not running. Please start it with: python app.py');
    }
}

checkAPIStatus();
