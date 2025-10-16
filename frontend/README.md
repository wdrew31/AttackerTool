# AttackerTool Frontend

Modern React + TypeScript web interface for AttackerTool security scanner.

## Features

- 🎨 Clean, modern UI with Tailwind CSS
- 📊 Real-time scan progress monitoring
- 📈 Interactive vulnerability reports
- 🎯 User-friendly scan configuration
- 📱 Responsive design

## Prerequisites

- Node.js 16+ and npm
- AttackerTool backend API running (http://localhost:8000)

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm start
```

The app will open at http://localhost:3000

### 3. Make Sure Backend is Running

In a separate terminal:

```bash
cd ../backend
source ../venv/bin/activate
python -m uvicorn app.main:app --reload
```

## Project Structure

```
src/
├── components/
│   └── common/           # Reusable UI components
│       ├── Header.tsx
│       ├── Button.tsx
│       └── Card.tsx
├── pages/                # Main application pages
│   ├── Home.tsx         # Dashboard/landing page
│   ├── NewScan.tsx      # Scan configuration form
│   ├── ScanProgress.tsx # Real-time progress monitoring
│   └── ScanResults.tsx  # Vulnerability report viewer
├── services/
│   └── api.ts           # Backend API client
├── types/
│   └── index.ts         # TypeScript type definitions
├── App.tsx              # Main app with routing
└── index.tsx            # Entry point
```

## Available Scripts

### `npm start`
Runs the app in development mode at http://localhost:3000

### `npm test`
Launches the test runner

### `npm run build`
Builds the app for production to the `build` folder

## Usage Guide

### Starting a New Scan

1. Click "Start New Scan" or navigate to /scan/new
2. Enter target URL (e.g., http://localhost:5001)
3. Adjust max crawl depth if needed (1-5)
4. Check the consent checkbox
5. Click "Start Scan"

### Monitoring Progress

- Progress bar shows scan completion (0-100%)
- Real-time statistics update every 2 seconds
- Status shows current phase (crawling/testing)
- Auto-redirects to results when complete

### Viewing Results

- Summary cards show vulnerability breakdown
- Full list of discovered vulnerabilities
- Each vulnerability includes:
  - Type and severity
  - Affected URL and parameter
  - CVSS score
  - CWE and OWASP mappings
  - Remediation guidance

## API Configuration

The frontend connects to the backend at `http://localhost:8000` by default.

To change this, set the environment variable:

```bash
REACT_APP_API_URL=http://your-api-url:port npm start
```

## Customization

### Colors

Edit `tailwind.config.js` to customize colors:

```javascript
colors: {
  primary: '#4F46E5',  // Main brand color
  severity: {
    critical: '#DC2626',
    high: '#EA580C',
    // ...
  }
}
```

### Components

All components are in `src/components/` and can be easily customized or extended.

## Troubleshooting

### "API Disconnected" on Home Page

**Cause:** Backend API is not running or not accessible

**Solution:**
```bash
cd backend
source ../venv/bin/activate
python -m uvicorn app.main:app --reload
```

### Network Errors During Scan

**Cause:** CORS or network connectivity issues

**Solution:** 
- Check backend logs
- Verify CORS configuration in backend/app/main.py
- Ensure both servers are running

### Blank Page or JavaScript Errors

**Cause:** Missing dependencies or build errors

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
npm start
```

## Development

### Adding New Pages

1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Add navigation link in `src/components/common/Header.tsx`

### Adding API Endpoints

1. Add method to `src/services/api.ts`
2. Add TypeScript types to `src/types/index.ts`
3. Use in your component with async/await

## Production Build

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

To serve it:

```bash
npm install -g serve
serve -s build -p 3000
```

Or integrate with backend (Phase 2):
- Configure FastAPI to serve static files from `build/`
- Single deployment unit

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Follow the existing code style
2. Use TypeScript for type safety
3. Keep components small and reusable
4. Add comments for complex logic

## Next Steps

### Phase 1.6 Enhancements
- [ ] Add scan history page
- [ ] Implement filtering and sorting
- [ ] Add charts and visualizations
- [ ] Export functionality (JSON/CSV)

### Phase 1.7 Polish
- [ ] Animations and transitions
- [ ] Better error messages
- [ ] Keyboard shortcuts
- [ ] Dark mode support

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Recharts** - Charts (planned)

## License

Part of AttackerTool project - see root LICENSE file

## Support

For issues or questions, check the main project README or documentation.
