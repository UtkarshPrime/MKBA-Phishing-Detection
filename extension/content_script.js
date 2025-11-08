// Content script for displaying phishing warnings

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'PHISHING_DETECTED') {
        showPhishingWarning(request.data);
    }
});

// Show phishing warning overlay
function showPhishingWarning(data) {
    // Remove existing warning if any
    const existing = document.getElementById('phishing-warning-overlay');
    if (existing) {
        existing.remove();
    }

    // Create warning overlay
    const overlay = document.createElement('div');
    overlay.id = 'phishing-warning-overlay';
    overlay.innerHTML = `
    <div style="
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.95);
      z-index: 999999;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    ">
      <div style="
        background: white;
        padding: 40px;
        border-radius: 12px;
        max-width: 500px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      ">
        <div style="
          width: 80px;
          height: 80px;
          background: #ff4444;
          border-radius: 50%;
          margin: 0 auto 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 48px;
        ">⚠️</div>
        
        <h1 style="
          color: #ff4444;
          font-size: 28px;
          margin: 0 0 16px 0;
          font-weight: 700;
        ">Phishing Warning!</h1>
        
        <p style="
          color: #333;
          font-size: 16px;
          line-height: 1.6;
          margin: 0 0 24px 0;
        ">${data.message}</p>
        
        <div style="
          background: #f5f5f5;
          padding: 16px;
          border-radius: 8px;
          margin-bottom: 24px;
          text-align: left;
        ">
          <p style="margin: 0 0 8px 0; color: #666; font-size: 14px;">
            <strong>Risk Score:</strong> ${data.score.toFixed(1)}/100
          </p>
          <p style="margin: 0; color: #666; font-size: 14px;">
            <strong>Classification:</strong> ${data.classification.toUpperCase()}
          </p>
        </div>
        
        <div style="display: flex; gap: 12px; justify-content: center;">
          <button id="phishing-go-back" style="
            background: #ff4444;
            color: white;
            border: none;
            padding: 12px 32px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
          ">Go Back (Recommended)</button>
          
          <button id="phishing-proceed" style="
            background: transparent;
            color: #666;
            border: 2px solid #ddd;
            padding: 12px 32px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
          ">Proceed Anyway</button>
        </div>
      </div>
    </div>
  `;

    document.body.appendChild(overlay);

    // Add event listeners
    document.getElementById('phishing-go-back').addEventListener('click', () => {
        window.history.back();
    });

    document.getElementById('phishing-proceed').addEventListener('click', () => {
        overlay.remove();
    });

    // Add hover effects
    const proceedBtn = document.getElementById('phishing-proceed');
    proceedBtn.addEventListener('mouseenter', () => {
        proceedBtn.style.borderColor = '#999';
        proceedBtn.style.color = '#333';
    });
    proceedBtn.addEventListener('mouseleave', () => {
        proceedBtn.style.borderColor = '#ddd';
        proceedBtn.style.color = '#666';
    });

    const backBtn = document.getElementById('phishing-go-back');
    backBtn.addEventListener('mouseenter', () => {
        backBtn.style.background = '#cc0000';
    });
    backBtn.addEventListener('mouseleave', () => {
        backBtn.style.background = '#ff4444';
    });
}

console.log('Phishing Detection Extension: Content script loaded');
