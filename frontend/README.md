# Phishing Detection System - Frontend

A modern, responsive web interface for the Phishing Detection System.

## Features

- **URL Analysis**: Analyze URLs for phishing indicators
- **Email Analysis**: Check email content for suspicious patterns
- **Real-time Results**: Instant feedback with detailed analysis
- **Analysis History**: Track your recent analyses with local storage
- **Responsive Design**: Works on desktop, tablet, and mobile
- **No Build Required**: Pure HTML, CSS, and JavaScript

## Quick Start

### 1. Start the Backend API

```bash
cd phishing_detection/backend
python app.py
```

The API will run on `http://localhost:8000`

### 2. Open the Frontend

Simply open `index.html` in your web browser:

**Option A: Double-click**
- Navigate to `phishing_detection/frontend/`
- Double-click `index.html`

**Option B: Use a local server (recommended)**
```bash
cd phishing_detection/frontend

# Python 3
python -m http.server 8080

# Or use any other local server
```

Then open `http://localhost:8080` in your browser.

### 3. Start Analyzing

- Click on "URL Analysis" tab
- Enter a URL or click an example
- Click "Analyze URL"
- View detailed results

## Pages

### Home Page
- **URL Analysis Tab**: Analyze suspicious URLs
- **Email Analysis Tab**: Check email content
- **Example Buttons**: Quick test with sample data
- **Results Display**: Detailed analysis with risk score

### History Page
- View all your recent analyses
- Filter by type (URL/Email) or classification
- Clear history option
- Persistent storage using localStorage

### About Page
- Learn about phishing
- Understand how the system works
- View features analyzed
- Get tips to avoid phishing

## Features

### URL Analysis
Analyzes 14 features including:
- URL length and structure
- Domain characteristics
- HTTPS usage
- Suspicious keywords
- IP address detection
- URL shortener detection

### Email Analysis
Analyzes 5 features including:
- Urgency keywords
- Suspicious phrases
- URL count in content
- Exclamation marks
- Email length

### Risk Scoring
- **Score > 70**: Phishing (High Risk) 🚨
- **Score 40-70**: Suspicious (Medium Risk) ⚠️
- **Score < 40**: Legitimate (Low Risk) ✅

## Technology Stack

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript**: No frameworks or dependencies
- **LocalStorage**: Client-side data persistence
- **Fetch API**: RESTful API communication

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Opera

## Configuration

The API URL is configured in `script.js`:

```javascript
const API_URL = 'http://localhost:8000';
```

If your API runs on a different port, update this value.

## Features Showcase

### Responsive Design
- Mobile-friendly layout
- Adaptive navigation
- Touch-optimized buttons

### User Experience
- Smooth animations
- Loading states
- Error handling
- Success feedback

### Data Persistence
- Analysis history saved locally
- Filter and search history
- Clear history option

## Troubleshooting

### "Failed to analyze" error
**Problem**: Cannot connect to API server

**Solution**:
1. Make sure the backend is running: `python app.py`
2. Check the API URL in `script.js`
3. Verify no firewall is blocking port 8000

### CORS errors
**Problem**: Cross-Origin Resource Sharing errors

**Solution**:
- The backend already has CORS enabled
- Use a local server instead of opening HTML directly
- Check browser console for specific errors

### History not saving
**Problem**: Analysis history disappears

**Solution**:
- Check if localStorage is enabled in your browser
- Clear browser cache and try again
- Check browser privacy settings

## Development

### File Structure
```
frontend/
├── index.html      # Main HTML file
├── styles.css      # All styles
├── script.js       # All JavaScript
└── README.md       # This file
```

### Customization

**Change Colors**:
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-color: #4285f4;
    --danger-color: #ea4335;
    --warning-color: #fbbc04;
    --success-color: #34a853;
}
```

**Add Features**:
1. Add HTML in `index.html`
2. Add styles in `styles.css`
3. Add functionality in `script.js`

## API Integration

The frontend communicates with the backend API:

### URL Analysis Endpoint
```javascript
POST http://localhost:8000/analyze/url
Content-Type: application/json

{
  "url": "http://example.com"
}
```

### Email Analysis Endpoint
```javascript
POST http://localhost:8000/analyze/email
Content-Type: application/json

{
  "content": "Email content here"
}
```

## Screenshots

### Home Page - URL Analysis
- Clean, modern interface
- Easy-to-use input form
- Example buttons for quick testing

### Results Display
- Large risk score display
- Color-coded classification
- Detailed feature breakdown
- Clear warning messages

### History Page
- Chronological list of analyses
- Filter by type or classification
- Time stamps for each analysis

## Performance

- **Load Time**: < 1 second
- **Analysis Time**: 2-3 seconds (depends on API)
- **Memory Usage**: Minimal (< 5MB)
- **Storage**: Uses localStorage (< 1MB)

## Security Notes

- All data is processed locally and via your API
- No data sent to external servers
- History stored only in browser localStorage
- Clear history anytime

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Export history to CSV
- [ ] Batch URL analysis
- [ ] Real-time URL scanning
- [ ] Browser extension integration
- [ ] User accounts and cloud sync
- [ ] Advanced filtering options
- [ ] Charts and statistics

## License

MIT License - Free to use and modify

## Support

For issues or questions:
1. Check the main project README
2. Verify API server is running
3. Check browser console for errors
4. Review this documentation

---

**Built with ❤️ for cybersecurity awareness**
