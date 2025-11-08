# Phishing Detection System

A machine learning-based system to detect phishing attempts by analyzing URLs, email content, and website features. Includes a REST API backend and a browser extension for real-time protection.

## Features

- **URL Analysis**: Detect phishing URLs using ML-based feature extraction
- **Email Classification**: Identify phishing emails based on content analysis
- **Browser Extension**: Real-time protection while browsing
- **REST API**: Easy integration with other applications

## Project Structure

```
phishing_detection/
├── backend/
│   ├── app.py                 # FastAPI server
│   ├── model.pkl              # Trained ML model (generated)
│   ├── feature_extractor.py   # Feature extraction logic
│   ├── train_model.py         # Model training script
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html             # Web application UI
│   ├── styles.css             # Styling
│   ├── script.js              # Frontend logic
│   └── README.md              # Frontend documentation
├── extension/
│   ├── manifest.json          # Extension configuration
│   ├── background.js          # Background service worker
│   ├── content_script.js      # Content script for warnings
│   ├── popup.html             # Extension popup UI
│   ├── popup.css              # Popup styling
│   └── popup.js               # Popup logic
├── data/
│   ├── phishing_urls.csv      # Phishing URL dataset
│   ├── legitimate_urls.csv    # Legitimate URL dataset
│   └── emails.csv             # Email dataset
├── README.md                  # This file
├── QUICKSTART.md              # Quick setup guide
└── START_ALL.bat              # Start both backend and frontend
```

## Setup Instructions

### Quick Start (All-in-One)

**Windows**:
```bash
# Start both backend and frontend
START_ALL.bat
```

Then open your browser to: **http://localhost:8080**

### Backend Setup

1. **Install Python dependencies**:
```bash
cd phishing_detection/backend
pip install -r requirements.txt
```

2. **Train the ML model**:
```bash
python train_model.py
```

This will:
- Load training data from `../data/` directory
- Extract features from URLs
- Train a Random Forest classifier
- Save the model as `model.pkl`
- Display accuracy metrics

3. **Start the API server**:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Frontend Web App Setup

1. **Start the frontend server**:
```bash
cd phishing_detection/frontend
python -m http.server 8080
```

2. **Open in browser**:
   - Navigate to `http://localhost:8080`
   - Or double-click `index.html` to open directly

3. **Start using**:
   - Analyze URLs in the URL Analysis tab
   - Check emails in the Email Analysis tab
   - View history of your analyses
   - Learn more in the About page

**Features**:
- Modern, responsive web interface
- Real-time URL and email analysis
- Analysis history with filtering
- No build tools required (pure HTML/CSS/JS)
- Mobile-friendly design

### Browser Extension Setup

1. **Open Chrome Extensions page**:
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)

2. **Load the extension**:
   - Click "Load unpacked"
   - Select the `phishing_detection/extension` folder

3. **The extension is now active**:
   - Icon will appear in the toolbar
   - Automatic URL analysis on navigation
   - Click icon to see analysis results

## Usage

### API Endpoints

#### Analyze URL
```bash
POST http://localhost:8000/analyze/url
Content-Type: application/json

{
  "url": "http://suspicious-site.com/login"
}
```

Response:
```json
{
  "classification": "phishing",
  "score": 85.5,
  "features": {
    "url_length": 35,
    "has_ip": 0,
    "suspicious_keywords": 1,
    ...
  },
  "message": "⚠️ This URL appears to be a phishing attempt. Do not proceed."
}
```

#### Analyze Email
```bash
POST http://localhost:8000/analyze/email
Content-Type: application/json

{
  "content": "URGENT: Verify your account now!"
}
```

Response:
```json
{
  "classification": "phishing",
  "score": 75.0,
  "features": {
    "urgency_count": 2,
    "url_count": 1,
    ...
  },
  "message": "⚠️ This email appears to be a phishing attempt."
}
```

### Browser Extension

1. **Automatic Protection**:
   - Extension automatically analyzes URLs as you browse
   - Displays warning overlay for phishing sites
   - Options to go back or proceed anyway

2. **Manual Check**:
   - Click extension icon to see current page analysis
   - View risk score and classification
   - Re-analyze if needed

## Features Extracted

### URL Features
- URL length, domain length, path length
- Subdomain count
- IP address detection
- HTTPS usage
- Suspicious keywords (login, verify, account, etc.)
- URL shortening service detection
- Special character count
- Digit ratio

### Email Features
- Email length
- Urgency keywords count
- Number of URLs in content
- Suspicious phrases
- Exclamation mark count

## Model Performance

The Random Forest classifier is trained on URL features and achieves:
- **Accuracy**: ~90%+ (depends on training data)
- **False Positive Rate**: <5%

Note: With the sample dataset (10 phishing + 10 legitimate URLs), accuracy will be limited. For production use, train with a larger dataset (10,000+ samples recommended).

## Extending the Dataset

To improve model accuracy:

1. Add more URLs to `data/phishing_urls.csv` and `data/legitimate_urls.csv`
2. Ensure balanced dataset (similar number of phishing and legitimate samples)
3. Retrain the model: `python train_model.py`

## Security Considerations

- The extension requires `<all_urls>` permission to analyze any website
- API runs locally by default (localhost:8000)
- No data is sent to external servers
- Cache stores analysis results locally for 1 hour

## Troubleshooting

**Model not loading**:
- Ensure you've run `python train_model.py` first
- Check that `model.pkl` exists in the backend directory

**Extension not working**:
- Verify the API server is running on port 8000
- Check browser console for errors
- Ensure extension has necessary permissions

**API errors**:
- Install all dependencies: `pip install -r requirements.txt`
- Check Python version (3.10+ recommended)
- Verify port 8000 is not in use

## Future Enhancements

- [ ] Add website content analysis (HTML, forms, scripts)
- [ ] Implement neural network model for improved accuracy
- [ ] Add user feedback mechanism to improve model
- [ ] Support for Firefox and Edge browsers
- [ ] Database for storing analysis history
- [ ] User authentication and personalized settings
- [ ] Real-time threat intelligence integration
- [ ] Whitelist/blacklist management

## License

MIT License - Feel free to use and modify for your projects.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
