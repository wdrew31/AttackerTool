# Web Frontend Dashboard - Planning Document

## Overview

Build a modern, user-friendly web dashboard for AttackerTool that allows users to easily configure scans, monitor progress in real-time, and review vulnerability reports without needing to use the command line.

## Technology Stack Recommendations

### Primary Choice: React + TypeScript
**Why:**
- Modern, well-supported framework
- Great for real-time updates (scan progress)
- TypeScript provides type safety
- Large ecosystem of components
- You already have Node.js installed

### Alternative: Vue.js
**Why:**
- Simpler learning curve than React
- Great documentation
- Still powerful enough for our needs

### Styling: Tailwind CSS
**Why:**
- Rapid development
- Modern, clean look
- Highly customizable
- No need to write custom CSS

### Additional Libraries:
- **Axios**: HTTP requests to backend API
- **React Router**: Page navigation
- **Recharts** or **Chart.js**: Visualizations
- **React Query**: Data fetching and caching
- **Lucide React**: Icons

## Frontend Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── scan/
│   │   │   ├── ScanForm.tsx
│   │   │   ├── ScanProgress.tsx
│   │   │   ├── ScanList.tsx
│   │   │   └── ScanCard.tsx
│   │   └── report/
│   │       ├── VulnerabilityList.tsx
│   │       ├── VulnerabilityCard.tsx
│   │       ├── SeverityBadge.tsx
│   │       ├── StatisticsPanel.tsx
│   │       └── RemediationGuide.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── NewScan.tsx
│   │   ├── ScanDetails.tsx
│   │   ├── ScanHistory.tsx
│   │   └── About.tsx
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   ├── utils/
│   │   └── helpers.ts
│   ├── App.tsx
│   └── index.tsx
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

## Pages & Features

### 1. Home/Dashboard Page
**Route:** `/`

**Purpose:** Landing page and overview

**Features:**
- Welcome message with security warning
- Quick start button to initiate a new scan
- Recent scans list (last 5)
- Overall statistics:
  - Total scans run
  - Total vulnerabilities found
  - Most common vulnerability type
- Quick actions:
  - Start New Scan
  - View Scan History
  - Documentation

**UI Elements:**
- Hero section with call-to-action
- Statistics cards with icons
- Recent scans table/list
- Navigation to other sections

### 2. New Scan Page
**Route:** `/scan/new`

**Purpose:** Configure and start a new security scan

**Features:**
- URL input with validation
  - Must start with http:// or https://
  - Domain validation
  - Port specification
- Advanced options (collapsible):
  - Max crawl depth (default: 2)
  - Scan timeout
  - Request delay/throttling
- Legal consent checkbox:
  - "I confirm I have permission to test this application"
  - Must be checked to proceed
- Start Scan button
- Redirect to progress page on start

**UI Elements:**
- Form with clear labels
- Input validation with error messages
- Collapsible advanced settings
- Prominent warning about legal requirements
- Progress indicator after starting

### 3. Scan Progress Page
**Route:** `/scan/:scanId/progress`

**Purpose:** Real-time monitoring of active scan

**Features:**
- Live progress bar (0-100%)
- Current status indicator:
  - Queued
  - Crawling
  - Testing
  - Completed
  - Failed
- Real-time statistics:
  - Pages crawled
  - Input points found
  - Vulnerabilities found (so far)
  - Time elapsed
- Activity log/feed (last 10 actions)
- Cancel scan button
- Auto-redirect to results when complete

**UI Elements:**
- Large progress bar with percentage
- Status badge with color coding
- Statistics in cards
- Activity timeline
- Action buttons

**Technical:**
- Poll API every 2 seconds for updates
- WebSocket consideration for Phase 2
- Show loading states appropriately

### 4. Scan Results/Details Page
**Route:** `/scan/:scanId`

**Purpose:** View detailed scan results and vulnerabilities

**Features:**
- Scan summary section:
  - Target URL
  - Scan date/time
  - Duration
  - Overall status
- Statistics dashboard:
  - Pie chart of vulnerabilities by severity
  - Bar chart of vulnerability types
  - Key metrics in cards
- Vulnerability list:
  - Filterable by severity
  - Searchable
  - Sortable
  - Expandable cards for details
- Individual vulnerability details:
  - Type and subtype
  - Severity badge with CVSS score
  - Affected URL and parameter
  - Payload used
  - Evidence/proof
  - CWE and OWASP mappings
  - Remediation guidance (expandable)
- Export options:
  - Download JSON report
  - Copy to clipboard
  - Print-friendly view (Phase 2: PDF)
- Actions:
  - Re-scan same target
  - Delete scan
  - Share scan (Phase 2)

**UI Elements:**
- Summary cards at top
- Charts/visualizations
- Filterable/sortable table or cards
- Expandable vulnerability details
- Color-coded severity indicators
- Action buttons

### 5. Scan History Page
**Route:** `/history`

**Purpose:** View all past scans

**Features:**
- List of all scans
- Sortable by:
  - Date (newest first, default)
  - Target URL
  - Vulnerabilities found
  - Status
- Filterable by:
  - Status (completed, failed, etc.)
  - Date range
  - Has vulnerabilities
- Search by target URL
- Pagination (10-20 per page)
- Bulk actions:
  - Delete selected scans
  - Export multiple
- Click to view details

**UI Elements:**
- Data table with sorting
- Filter controls
- Search bar
- Pagination controls
- Action buttons per row

### 6. About/Help Page
**Route:** `/about`

**Purpose:** Information and documentation

**Features:**
- About AttackerTool
- How to use guide
- Legal and ethical guidelines
- API documentation link
- Contact/support information
- Version information

## Component Specifications

### ScanForm Component
**Props:**
- `onSubmit: (url: string, options: ScanOptions) => void`

**State:**
- URL input value
- Max depth value
- Consent checkbox state
- Validation errors

**Features:**
- Real-time URL validation
- Advanced options toggle
- Form submission handling
- Error display

### ScanProgress Component
**Props:**
- `scanId: string`

**State:**
- Progress percentage
- Status
- Statistics
- Poll interval

**Features:**
- Auto-polling API
- Progress bar animation
- Status updates
- Auto-redirect on completion

### VulnerabilityCard Component
**Props:**
- `vulnerability: Vulnerability`
- `expanded: boolean`
- `onToggle: () => void`

**Features:**
- Severity badge
- Expandable details
- Remediation section
- Copy to clipboard
- Color coding

### StatisticsPanel Component
**Props:**
- `statistics: ScanStatistics`

**Features:**
- Pie chart for severity distribution
- Bar chart for vulnerability types
- Metric cards
- Responsive design

## API Integration

### API Service (`services/api.ts`)

```typescript
// Core functions needed:
- startScan(url: string, options: ScanOptions): Promise<ScanResponse>
- getScan(scanId: string): Promise<ScanResult>
- listScans(): Promise<ScanResult[]>
- deleteScan(scanId: string): Promise<void>
- checkHealth(): Promise<HealthStatus>
```

### TypeScript Types (`types/index.ts`)

```typescript
interface ScanOptions {
  target_url: string;
  max_depth: number;
}

interface ScanResponse {
  scan_id: string;
  status: string;
  message: string;
}

interface ScanResult {
  scan_id: string;
  target_url: string;
  status: 'queued' | 'crawling' | 'testing' | 'completed' | 'failed';
  progress: number;
  start_time: string;
  end_time?: string;
  pages_crawled: number;
  input_points_found: number;
  vulnerabilities_found: number;
  vulnerabilities: Vulnerability[];
  summary: {
    critical: number;
    high: number;
    medium: number;
    low: number;
    info: number;
  };
}

interface Vulnerability {
  type: string;
  subtype: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low' | 'Info';
  url: string;
  method: string;
  parameter: string;
  payload: string;
  evidence: string;
  description: string;
  cvss_score: number;
  cwe: string;
  owasp: string;
  remediation: {
    summary: string;
    steps: string[];
  };
}
```

## Design System

### Color Palette

**Severity Colors:**
- Critical: `#DC2626` (red-600)
- High: `#EA580C` (orange-600)
- Medium: `#F59E0B` (amber-500)
- Low: `#10B981` (emerald-500)
- Info: `#3B82F6` (blue-500)

**Status Colors:**
- Queued: `#6B7280` (gray-500)
- Running: `#3B82F6` (blue-500)
- Completed: `#10B981` (emerald-500)
- Failed: `#DC2626` (red-600)

**UI Colors:**
- Primary: `#4F46E5` (indigo-600)
- Background: `#F9FAFB` (gray-50)
- Card: `#FFFFFF` (white)
- Border: `#E5E7EB` (gray-200)
- Text: `#111827` (gray-900)
- Text Secondary: `#6B7280` (gray-500)

### Typography
- Headings: `font-semibold` or `font-bold`
- Body: `font-normal`
- Code: `font-mono`
- Size scale: `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`

### Spacing
- Container: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- Cards: `p-6 rounded-lg shadow-sm`
- Sections: `space-y-6` or `gap-6`

### Responsive Breakpoints
- Mobile: default
- Tablet: `sm:` (640px)
- Desktop: `lg:` (1024px)
- Wide: `xl:` (1280px)

## User Flow Examples

### Flow 1: New User First Scan
1. Land on Home page
2. See warning and instructions
3. Click "Start New Scan"
4. Enter target URL (http://localhost:5001)
5. Check consent checkbox
6. Click "Start Scan"
7. Redirected to progress page
8. Watch real-time progress
9. Auto-redirected to results
10. Review vulnerabilities
11. Export report

### Flow 2: Returning User Check History
1. Land on Home page
2. See recent scans
3. Click "View All Scans"
4. Browse scan history
5. Filter by date
6. Click on specific scan
7. Review details
8. Re-run scan if needed

### Flow 3: Review Specific Vulnerability
1. On scan results page
2. See vulnerability list
3. Click "Critical" filter
4. Sort by CVSS score
5. Click on vulnerability card
6. Read detailed information
7. Expand remediation guide
8. Copy payload for testing
9. Save report

## Implementation Priority

### Phase 1.5 - MVP Frontend (Week 1-2)
**Priority: HIGH**
- [ ] Set up React + TypeScript project
- [ ] Configure Tailwind CSS
- [ ] Create basic layout (Header, Footer, Container)
- [ ] Implement Home page with basic info
- [ ] Build New Scan page with form
- [ ] Create Scan Progress page with polling
- [ ] Build basic Results page
- [ ] API service integration
- [ ] Basic routing

**Deliverable:** Working dashboard that can start scans and view results

### Phase 1.6 - Enhanced Features (Week 3)
**Priority: MEDIUM**
- [ ] Add Scan History page
- [ ] Implement filtering and sorting
- [ ] Add charts/visualizations
- [ ] Enhance vulnerability details
- [ ] Add export functionality
- [ ] Improve responsive design
- [ ] Add loading states and error handling

**Deliverable:** Polished, feature-complete dashboard

### Phase 1.7 - Polish & UX (Week 4)
**Priority: LOW**
- [ ] Add animations and transitions
- [ ] Improve error messages
- [ ] Add tooltips and help text
- [ ] Create About page
- [ ] Add keyboard shortcuts
- [ ] Performance optimization
- [ ] Accessibility improvements

**Deliverable:** Production-ready dashboard

## Technical Considerations

### CORS Configuration
Backend needs to allow frontend origin:
```python
# In backend/app/main.py - already configured
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### State Management
**Phase 1.5:** Use React useState and useEffect
**Phase 2:** Consider Redux or Zustand if needed

### Error Handling
- Network errors
- API errors (4xx, 5xx)
- Validation errors
- Timeout handling
- User-friendly error messages

### Performance
- Lazy loading for routes
- Memoization for expensive calculations
- Debouncing for search inputs
- Pagination for large lists
- Optimistic UI updates

### Testing Strategy
- Unit tests for utilities
- Component tests with React Testing Library
- Integration tests for critical flows
- E2E tests with Playwright (Phase 2)

## Development Workflow

### Setup
```bash
# Create React app with TypeScript
npx create-react-app frontend --template typescript

# Install dependencies
npm install axios react-router-dom recharts lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Development
```bash
# Run frontend dev server
npm start  # http://localhost:3000

# Run backend API
cd backend && python -m uvicorn app.main:app --reload
```

### Build
```bash
# Production build
npm run build

# Serve static files from backend (Phase 2)
```

## Security Considerations

### Frontend Security
- Validate all user inputs
- Sanitize displayed content
- Use HTTPS in production
- Implement CSP headers
- No sensitive data in localStorage
- Rate limiting for API calls

### User Authentication (Phase 2)
- JWT tokens
- Secure session management
- Role-based access control
- Multi-user support

## Deployment Options (Phase 2)

### Option 1: Separate Deployment
- Frontend: Netlify, Vercel, or GitHub Pages
- Backend: Heroku, Railway, or VPS

### Option 2: Integrated Deployment
- Serve frontend build from FastAPI
- Single deployment unit
- Easier to manage

## Success Metrics

### Usability
- [ ] Users can start a scan in < 30 seconds
- [ ] Results are clear and actionable
- [ ] No training required for basic use

### Performance
- [ ] Page load < 2 seconds
- [ ] Scan updates within 2 seconds
- [ ] Smooth animations (60fps)

### Accessibility
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] WCAG 2.1 Level AA compliance

## Next Steps

1. **Review this plan** - Make sure it aligns with your vision
2. **Choose tech stack** - React or Vue? Tailwind or other?
3. **Set up project** - Initialize React/TypeScript project
4. **Start with MVP** - Focus on core functionality first
5. **Iterate and improve** - Add features incrementally

## Questions to Consider

Before starting development:

1. **Do you want to learn React** or prefer Vue.js?
2. **Desktop-first or mobile-first** design approach?
3. **Dark mode** support from the start?
4. **User authentication** - needed now or later?
5. **Multi-language support** - needed?

---

**Ready to build?** This plan gives you a clear roadmap for creating a professional, user-friendly web interface for AttackerTool!
