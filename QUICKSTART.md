# Quick Start Guide

## Get Started in 3 Steps

### Step 1: Train the Model

```bash
cd phishing_detection/backend
pip install -r requirements.txt
python train_model.py
```

Expected output:
```
Starting model training...
Total samples: 20 (Phishing: 10, Legitimate: 10)
Extracting features...
Training samples: 16, Test samples: 4
Training Random Forest model...

Model Accuracy: 100.00%
Model saved as model.pkl
```

### Step 2: Start the API Server

```bash
python app.py
```

Expected output:
```
Model loaded successfully
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Keep this terminal open!

### Step 3: Install Browser Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right corner)
3. Click "Load unpacked"
4. Navigate to and select the `phishing_detection/extension` folder
5. Done! The extension icon should appear in your toolbar

## Test It Out

### Test the API

Open a new terminal and try:

```bash
curl -X POST http://localhost:8000/analyze/url \
  -H "Content-Type: application/json" \
  -d '{"url": "http://paypal-verify.com/login"}'
```

### Test the Extension

1. Visit a test phishing URL (e.g., `http://paypal-verify.com`)
2. The extension should show a warning overlay
3. Click the extension icon to see detailed analysis

### Test with Safe URLs

Try visiting legitimate sites like:
- https://www.google.com
- https://github.com
- https://stackoverflow.com

The extension should show them as safe.

## Troubleshooting

**"Model not found" error**:
- Make sure you ran `python train_model.py` first
- Check that `model.pkl` exists in the backend folder

**Extension not working**:
- Verify the API is running on port 8000
- Check the browser console (F12) for errors
- Make sure you loaded the extension correctly

**API connection errors**:
- Ensure no firewall is blocking port 8000
- Try accessing http://localhost:8000 in your browser
- Check that all dependencies are installed

## Next Steps

- Add more training data to `data/` folder for better accuracy
- Customize the warning UI in `extension/content_script.js`
- Modify feature extraction in `backend/feature_extractor.py`
- Deploy the API to a cloud server for production use

Enjoy your phishing detection system! 🛡️
