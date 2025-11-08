// Popup script for displaying analysis results

document.addEventListener('DOMContentLoaded', async () => {
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');

    try {
        // Get current tab
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // Get stored analysis result
        const key = `analysis_${tab.id}`;
        const data = await chrome.storage.local.get(key);

        if (data[key]) {
            displayResult(data[key]);
        } else {
            // Trigger new analysis
            chrome.runtime.sendMessage({ type: 'ANALYZE_CURRENT_URL' });

            // Wait for result
            setTimeout(async () => {
                const newData = await chrome.storage.local.get(key);
                if (newData[key]) {
                    displayResult(newData[key]);
                } else {
                    showError();
                }
            }, 2000);
        }
    } catch (error) {
        console.error('Error:', error);
        showError();
    }
});

function displayResult(result) {
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const statusIcon = document.getElementById('status-icon');
    const statusText = document.getElementById('status-text');
    const scoreDiv = document.getElementById('score');
    const messageDiv = document.getElementById('message');

    loadingDiv.style.display = 'none';
    resultDiv.style.display = 'block';

    // Set icon and status
    if (result.classification === 'phishing') {
        statusIcon.textContent = '🚨';
        statusText.textContent = 'Phishing Detected!';
        statusText.style.color = '#ea4335';
        scoreDiv.className = 'score danger';
    } else if (result.classification === 'suspicious') {
        statusIcon.textContent = '⚠️';
        statusText.textContent = 'Suspicious Site';
        statusText.style.color = '#fbbc04';
        scoreDiv.className = 'score suspicious';
    } else {
        statusIcon.textContent = '✅';
        statusText.textContent = 'Site Appears Safe';
        statusText.style.color = '#34a853';
        scoreDiv.className = 'score safe';
    }

    scoreDiv.textContent = result.score.toFixed(1);
    messageDiv.textContent = result.message;
}

function showError() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('error').style.display = 'block';
}

// Re-analyze button
document.getElementById('analyze-btn')?.addEventListener('click', () => {
    location.reload();
});

// Retry button
document.getElementById('retry-btn')?.addEventListener('click', () => {
    location.reload();
});
