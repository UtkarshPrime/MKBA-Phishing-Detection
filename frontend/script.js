// Configuration
const API_URL = 'http://localhost:8000';

// State
let analysisHistory = JSON.parse(localStorage.getItem('analysisHistory')) || [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    initializeGSAP();
    initializeNavigation();
    initializeTabs();
    initializeForms();
    initializeExamples();
    initializeHistory();
});

// ===== THEME MANAGEMENT =====
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);

    // Animate theme transition
    gsap.to('body', {
        duration: 0.3,
        ease: 'power2.inOut'
    });
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('theme-icon');
    const text = document.getElementById('theme-text');

    if (theme === 'dark') {
        icon.className = 'fas fa-moon';
        text.textContent = 'Dark Mode';
    } else {
        icon.className = 'fas fa-sun';
        text.textContent = 'Light Mode';
    }
}

// ===== GSAP ANIMATIONS =====
function initializeGSAP() {
    // Ensure elements are visible if GSAP fails or hangs
    setTimeout(() => {
        document.querySelectorAll('.sidebar, .top-header, .analysis-card, .nav-item, .chat-toggle').forEach(el => {
            if (getComputedStyle(el).opacity === '0') {
                el.style.opacity = '1';
            }
        });
    }, 2000);

    // Animate background shapes
    gsap.to('.shape-1', {
        x: 100,
        y: 100,
        rotation: 20,
        duration: 20,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });

    gsap.to('.shape-2', {
        x: -80,
        y: -80,
        rotation: -15,
        duration: 25,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });

    gsap.to('.shape-3', {
        x: 60,
        y: -60,
        rotation: 10,
        duration: 18,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });

    // Sidebar entrance
    gsap.set('.sidebar', { x: -100, opacity: 0 });
    gsap.to('.sidebar', {
        x: 0,
        opacity: 1,
        duration: 1,
        ease: 'power3.out',
        clearProps: 'transform' // Keep opacity 1, clear transform to avoid layout issues
    });

    // Header entrance
    gsap.set('.top-header', { y: -50, opacity: 0 });
    gsap.to('.top-header', {
        y: 0,
        opacity: 1,
        duration: 1,
        delay: 0.2,
        ease: 'power3.out',
        clearProps: 'transform'
    });

    // Content entrance
    gsap.set('.analysis-card', { y: 50, opacity: 0 });
    gsap.to('.analysis-card', {
        y: 0,
        opacity: 1,
        duration: 0.8,
        delay: 0.4,
        ease: 'back.out(1.4)',
        clearProps: 'transform'
    });

    // Stagger nav items
    gsap.set('.nav-item', { x: -30, opacity: 0 });
    gsap.to('.nav-item', {
        x: 0,
        opacity: 1,
        duration: 0.5,
        stagger: 0.1,
        delay: 0.6,
        ease: 'power2.out',
        clearProps: 'transform'
    });

    // Animate bot
    gsap.set('.chat-toggle', { scale: 0, opacity: 0 });
    gsap.to('.chat-toggle', {
        scale: 1,
        opacity: 1,
        duration: 0.6,
        delay: 1,
        ease: 'back.out(2)',
        clearProps: 'transform'
    });
}

// ===== PAGE SWITCHING =====
function switchPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
        // Ensure opacity is reset to 1 so it's visible when class is added back
        // We rely on display: none from CSS to hide it
        page.style.opacity = '1';
    });

    // Deactivate all nav items
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected page
    const selectedPage = document.getElementById(`${pageId}-page`);
    if (selectedPage) {
        selectedPage.classList.add('active');

        // Animate page entrance safely
        // We explicitly start from 0 and animate to 1
        gsap.fromTo(selectedPage,
            { y: 30, opacity: 0 },
            {
                y: 0,
                opacity: 1,
                duration: 0.5,
                ease: 'power2.out',
                clearProps: 'transform' // Keep opacity 1, clear transform
            }
        );
    }

    // Activate nav item
    const activeBtn = document.querySelector(`.nav-item[onclick="switchPage('${pageId}')"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }

    // Update page title
    const titles = {
        'url': 'URL Analysis',
        'email': 'Email Analysis',
        'history': 'Scan History',
        'about': 'About System'
    };
    const titleElement = document.getElementById('page-title');
    if (titleElement) {
        titleElement.textContent = titles[pageId] || 'Dashboard';
    }

    // Load history if on history page
    if (pageId === 'history') {
        displayHistory();
    }
}

// ===== INITIALIZATION FUNCTIONS =====
function initializeNavigation() {
    // Navigation is handled by onclick in HTML
    // This function is kept for compatibility
}

function initializeTabs() {
    // Tabs are not needed in new design
    // This function is kept for compatibility
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
    // URL examples (using chip class)
    document.querySelectorAll('.chip[data-url]').forEach(btn => {
        btn.addEventListener('click', () => {
            const url = btn.dataset.url;
            document.getElementById('url-input').value = url;
            analyzeURL(url);
        });
    });

    // Email examples
    document.querySelectorAll('.chip[data-email]').forEach(btn => {
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
    // URL section uses default 'results-section' ID
    // Email section uses 'email-results-section' ID
    const sectionId = type === 'url' ? 'results-section' : 'email-results-section';
    const contentId = type === 'url' ? 'results-content' : 'email-results-content';

    const resultsSection = document.getElementById(sectionId);
    const resultsContent = document.getElementById(contentId);

    if (!resultsSection || !resultsContent) {
        console.error(`Results elements not found: ${sectionId}, ${contentId}`);
        return;
    }

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
    if (result.features && Object.keys(result.features).length > 0) {
        const featureEntries = Object.entries(result.features).slice(0, 8); // Show first 8 features
        featuresHTML = `
            <div class="features-details">
                <h4><i class="fas fa-list-ul"></i> Analysis Details</h4>
                <div class="feature-table-container">
                    <table class="feature-table">
                        <thead>
                            <tr>
                                <th>Feature Detected</th>
                                <th style="text-align: right;">Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${featureEntries.map(([key, value]) => `
                                <tr>
                                    <td>
                                        <i class="fas fa-check-circle feature-icon"></i>
                                        ${formatFeatureName(key)}
                                    </td>
                                    <td>${formatFeatureValue(value)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
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
                <div class="score-value ${statusClass}">${result.score.toFixed(1)}<span style="font-size: 1rem;">/100</span></div>
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
    const urlSection = document.getElementById('results-section');
    const emailSection = document.getElementById('email-results-section');

    if (urlSection) urlSection.style.display = 'none';
    if (emailSection) emailSection.style.display = 'none';
}

// Close buttons
document.getElementById('close-results')?.addEventListener('click', hideResults);
document.getElementById('close-email-results')?.addEventListener('click', hideResults);

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

    historyList.style.display = 'block'; // Changed from flex to block for timeline
    emptyState.style.display = 'none';

    const timelineItems = filteredHistory.map(item => {
        const classification = item.result.classification.toLowerCase();
        const date = new Date(item.timestamp);
        const timeAgo = getTimeAgo(date);

        let statusIcon = '✅';
        if (classification === 'phishing') statusIcon = '🚨';
        else if (classification === 'suspicious') statusIcon = '⚠️';

        return `
            <div class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                    <div class="timeline-header">
                        <span class="type-badge ${item.type}">${item.type}</span>
                        <span class="timeline-date"><i class="far fa-clock"></i> ${timeAgo}</span>
                    </div>
                    <div class="timeline-body">
                        ${item.input.length > 120 ? item.input.substring(0, 120) + '...' : item.input}
                    </div>
                    <div class="timeline-footer">
                        <span class="status-badge ${classification}">
                            ${statusIcon} ${item.result.classification}
                        </span>
                        <span class="score-badge" style="color: ${getScoreColor(item.result.score)}">
                            ${item.result.score.toFixed(1)}
                        </span>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    historyList.innerHTML = `<div class="timeline">${timelineItems}</div>`;
}

function getScoreColor(score) {
    if (score > 80) return '#ff6b6b';
    if (score > 50) return '#feca57';
    return '#1dd1a1';
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

/* ===== CHAT FUNCTIONALITY ===== */
let chatHistory = [];

// Initialize Chat Toggle & Robot Sounds
document.addEventListener('DOMContentLoaded', () => {
    const robotContainer = document.querySelector('.css-robot-container');
    if (robotContainer) {
        // Toggle Chat
        robotContainer.addEventListener('click', () => {
            toggleChat();
        });

        // Hover Sound (Laugh)
        robotContainer.addEventListener('mouseenter', () => {
            playAudio('laugh');
        });
    }
});

/* ===== ROBOT AUDIO SYSTEM ===== */
const sounds = {
    laugh: new Audio('Laugh.wav'),
    move: new Audio('move.wav'),
    return: new Audio('return.wav'),
    respond: new Audio('respond.wav')
};

// Preload sounds
Object.values(sounds).forEach(sound => {
    sound.load();
    sound.volume = 0.5; // Set reasonable volume
});

// Track currently playing sound
let currentAudio = null;

function playAudio(type) {
    // Stop currently playing sound if any
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }

    const sound = sounds[type];
    if (sound) {
        currentAudio = sound;
        sound.currentTime = 0; // Reset to start
        sound.play().catch(e => console.log('Audio play failed (interaction required):', e));
    }
}

function toggleChat() {
    const chatWidget = document.getElementById('chat-widget');
    const isOpening = !chatWidget.classList.contains('active');

    chatWidget.classList.toggle('active');

    // Play appropriate sound
    if (isOpening) {
        playAudio('move');
    } else {
        playAudio('return');
    }

    // Focus input when opening
    if (isOpening) {
        setTimeout(() => {
            document.getElementById('chat-input').focus();
        }, 300);
    }
}

function handleChatInput(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message) return;

    // Add user message
    addMessage(message, 'user');
    input.value = '';

    // Show typing indicator
    showTypingIndicator();

    try {
        // Prepare context from current analysis if available
        const context = {};
        const urlInput = document.getElementById('url-input');
        const emailInput = document.getElementById('email-content');

        if (urlInput && urlInput.value) context.url = urlInput.value;
        if (emailInput && emailInput.value) context.email = emailInput.value;

        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: chatHistory,
                context: context
            }),
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator();

        // Play response sound
        playAudio('respond');

        // Add bot response
        addMessage(data.response, 'bot');

        // Update history
        chatHistory.push({ role: "user", content: message });
        chatHistory.push({ role: "assistant", content: data.response });

        // Limit history to last 10 messages to prevent context overflow
        if (chatHistory.length > 10) {
            chatHistory = chatHistory.slice(-10);
        }

    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator();
        addMessage("I'm having trouble connecting to the server. Please check if the backend is running.", 'bot');
    }
}

function showTypingIndicator() {
    const messagesDiv = document.getElementById('chat-messages');
    const indicatorDiv = document.createElement('div');
    indicatorDiv.className = 'typing-indicator';
    indicatorDiv.id = 'typing-indicator';

    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'typing-dot';
        indicatorDiv.appendChild(dot);
    }

    messagesDiv.appendChild(indicatorDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

function addMessage(text, sender) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
