import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/common/Header';
import Home from './pages/Home';
import NewScan from './pages/NewScan';
import ScanProgress from './pages/ScanProgress';
import ScanResults from './pages/ScanResults';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/scan/new" element={<NewScan />} />
          <Route path="/scan/:scanId/progress" element={<ScanProgress />} />
          <Route path="/scan/:scanId" element={<ScanResults />} />
          <Route path="/history" element={<Home />} />
          <Route path="/about" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
