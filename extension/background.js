// Background service worker for phishing detection

const API_URL = 'http://localhost:8000';
const CACHE_DURATION = 3600000; // 1 hour in milliseconds

// Cache for analyzed URLs
let urlCache = {};

// Listen for navigation events
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
    if (details.frameId === 0) { // Main frame only
        const url = details.url;

        // Skip chrome://, extension URLs, and local files
        if (url.startsWith('chrome://') ||
            url.startsWith('chrome-extension://') ||
            url.startsWith('file://') ||
            url.startsWith('about:')) {
            return;
        }

        console.log('Analyzing URL:', url);
        await analyzeURL(url, details.tabId);
    }
});

// Analyze URL for phishing
async function analyzeURL(url, tabId) {
    try {
        // Check cache first
        const cached = getCachedResult(url);
        if (cached) {
            console.log('Using cached result for:', url);
            handleAnalysisResult(cached, tabId);
            return;
        }

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

        // Cache result
        cacheResult(url, result);

        // Handle result
        handleAnalysisResult(result, tabId);

    } catch (error) {
        console.log('API not available - skipping analysis for:', url);
        // Continue without blocking if API is unavailable
        // This is normal when the backend is not running
    }
}

// Handle analysis result
function handleAnalysisResult(result, tabId) {
    // Store result for popup
    chrome.storage.local.set({
        [`analysis_${tabId}`]: result
    });

    // If phishing detected, send warning to content script
    if (result.classification === 'phishing') {
        chrome.tabs.sendMessage(tabId, {
            type: 'PHISHING_DETECTED',
            data: result
        }).catch(err => console.log('Could not send message:', err));
    }
}

// Cache management
function getCachedResult(url) {
    const cached = urlCache[url];
    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
        return cached.result;
    }
    return null;
}

function cacheResult(url, result) {
    urlCache[url] = {
        result: result,
        timestamp: Date.now()
    };

    // Limit cache size
    const keys = Object.keys(urlCache);
    if (keys.length > 100) {
        delete urlCache[keys[0]];
    }
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'ANALYZE_CURRENT_URL') {
        chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
            if (tabs[0]) {
                await analyzeURL(tabs[0].url, tabs[0].id);
                sendResponse({ success: true });
            }
        });
        return true; // Keep channel open for async response
    }
});

console.log('Phishing Detection Extension: Background script loaded');
