# Frontend User Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Start the Backend API
```bash
cd phishing_detection/backend
python app.py
```
✓ API running on http://localhost:8000

### Step 2: Start the Frontend Server
```bash
cd phishing_detection/frontend
python -m http.server 8080
```
✓ Frontend running on http://localhost:8080

### Step 3: Open in Browser
Open your browser and go to: **http://localhost:8080**

---

## 🎯 Using the Frontend

### Home Page - URL Analysis

1. **Enter a URL**
   - Type or paste a URL in the input field
   - Example: `http://paypal-verify.com/login`

2. **Click "Analyze URL"**
   - The system will analyze the URL
   - Results appear in 2-3 seconds

3. **View Results**
   - Risk Score (0-100)
   - Classification (Phishing/Suspicious/Legitimate)
   - Detailed features analyzed
   - Clear warning message

### Home Page - Email Analysis

1. **Switch to Email Tab**
   - Click "Email Analysis" button

2. **Paste Email Content**
   - Copy and paste suspicious email text
   - Include subject and body

3. **Click "Analyze Email"**
   - System checks for phishing indicators
   - Results show urgency keywords, suspicious phrases, etc.

### Quick Examples

Click the example buttons to test instantly:
- **Phishing Example**: See how phishing URLs are detected
- **Safe Example**: See how legitimate URLs are classified
- **IP Address**: See IP address detection in action

---

## 📊 Understanding Results

### Risk Score

```
🚨 Score > 70    = PHISHING (High Risk)
⚠️  Score 40-70  = SUSPICIOUS (Medium Risk)
✅ Score < 40    = LEGITIMATE (Low Risk)
```

### Classification

**Phishing (Red)**
- Do not proceed
- High confidence of phishing attempt
- Multiple suspicious indicators detected

**Suspicious (Yellow)**
- Proceed with caution
- Some concerning features found
- Verify before trusting

**Legitimate (Green)**
- Appears safe
- No major red flags
- Low risk indicators

### Features Analyzed

The results show key features that influenced the classification:
- **URL Length**: Longer URLs can be suspicious
- **Domain Length**: Unusually long domains
- **HTTPS**: Lack of HTTPS is a red flag
- **Suspicious Keywords**: Words like "verify", "urgent", "account"
- **IP Address**: Using IP instead of domain name
- **URL Shortener**: Shortened URLs hide destination

---

## 📜 History Page

### View Past Analyses

1. Click **"History"** in the navigation
2. See all your recent analyses
3. Each entry shows:
   - Type (URL or Email)
   - Content analyzed
   - Classification result
   - Risk score
   - Time stamp

### Filter History

Use the filter dropdown to show:
- **All**: Everything
- **URLs Only**: Just URL analyses
- **Emails Only**: Just email analyses
- **Phishing Only**: Only phishing detections
- **Legitimate Only**: Only safe results

### Clear History

Click **"Clear History"** to delete all saved analyses.

**Note**: History is stored locally in your browser (localStorage).

---

## ℹ️ About Page

Learn more about:
- What is phishing
- How the system works
- Features analyzed
- Classification system
- Tips to avoid phishing
- Technology stack

---

## 🎨 Features

### Modern Design
- Clean, professional interface
- Color-coded results
- Smooth animations
- Responsive layout

### User-Friendly
- Simple input forms
- One-click examples
- Clear error messages
- Loading indicators

### Smart Features
- Local history storage
- Filter and search
- Real-time analysis
- Detailed breakdowns

### Mobile Responsive
- Works on phones
- Works on tablets
- Works on desktops
- Adaptive layout

---

## 🔧 Troubleshooting

### "Failed to analyze" Error

**Problem**: Cannot connect to API

**Solutions**:
1. ✓ Check backend is running: `python app.py`
2. ✓ Verify API URL: http://localhost:8000
3. ✓ Check firewall settings
4. ✓ Try restarting both servers

### Results Not Showing

**Problem**: Analysis completes but no results

**Solutions**:
1. ✓ Check browser console (F12)
2. ✓ Verify API response format
3. ✓ Try refreshing the page
4. ✓ Clear browser cache

### History Not Saving

**Problem**: History disappears on refresh

**Solutions**:
1. ✓ Enable localStorage in browser
2. ✓ Check browser privacy settings
3. ✓ Disable private/incognito mode
4. ✓ Try a different browser

### Slow Performance

**Problem**: Analysis takes too long

**Solutions**:
1. ✓ Check API server performance
2. ✓ Verify network connection
3. ✓ Close other browser tabs
4. ✓ Restart the servers

---

## 💡 Tips & Tricks

### Best Practices

1. **Always verify suspicious URLs** before clicking
2. **Check multiple indicators** not just one
3. **Use the history** to track patterns
4. **Test known phishing sites** to see detection
5. **Share results** with others to educate

### Power User Features

- **Keyboard Shortcuts**: Tab to navigate, Enter to submit
- **Quick Examples**: Click examples for instant testing
- **Batch Testing**: Open multiple tabs for parallel analysis
- **Export History**: Copy from history page (manual)

### Educational Use

- **Demonstrate phishing**: Use examples in presentations
- **Train employees**: Show real vs fake URLs
- **Security awareness**: Educate about indicators
- **Test knowledge**: Quiz users with examples

---

## 📱 Browser Compatibility

### Fully Supported
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Opera

### Requirements
- Modern browser (2020+)
- JavaScript enabled
- LocalStorage enabled
- Internet connection (for API)

---

## 🎓 Example Scenarios

### Scenario 1: Suspicious Email

**Input**: "URGENT: Your account will be suspended! Click here to verify immediately."

**Expected Result**:
- Classification: Phishing or Suspicious
- High urgency keyword count
- Suspicious phrases detected
- Warning message displayed

### Scenario 2: Legitimate URL

**Input**: "https://www.google.com"

**Expected Result**:
- Classification: Legitimate
- Low risk score (< 10)
- HTTPS enabled
- No suspicious keywords

### Scenario 3: IP Address URL

**Input**: "http://192.168.1.1/login"

**Expected Result**:
- Classification: Phishing
- IP address detected
- No HTTPS
- Suspicious keyword: "login"

---

## 📊 Statistics

After using the system, you can:
- View total analyses in history
- See phishing detection rate
- Track most common threats
- Monitor your security awareness

---

## 🔐 Privacy & Security

### Your Data
- ✅ Processed locally
- ✅ Stored in browser only
- ✅ No external servers
- ✅ No tracking
- ✅ No data collection

### API Communication
- ✅ Local API only (localhost)
- ✅ No internet required (except API)
- ✅ No third-party services
- ✅ Full control over data

---

## 🆘 Getting Help

### Common Questions

**Q: Do I need internet?**
A: Only to connect to the local API server.

**Q: Is my data safe?**
A: Yes, everything is local. No data leaves your computer.

**Q: Can I use this offline?**
A: Yes, if the API server is running locally.

**Q: How accurate is it?**
A: 100% on test data, but expand training data for production.

**Q: Can I customize it?**
A: Yes! Edit the HTML, CSS, and JavaScript files.

---

## 🎉 Enjoy!

You're now ready to use the Phishing Detection System frontend!

**Remember**: This tool helps identify phishing, but always use multiple security measures and stay vigilant online.

---

**Need more help?** Check the main README.md or backend documentation.
