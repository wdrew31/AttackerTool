import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import apiService from '../services/api';

const NewScan: React.FC = () => {
  const navigate = useNavigate();
  const [targetUrl, setTargetUrl] = useState('');
  const [maxDepth, setMaxDepth] = useState(2);
  const [consent, setConsent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const validateUrl = (url: string): boolean => {
    try {
      const urlObj = new URL(url);
      return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!validateUrl(targetUrl)) {
      setError('Please enter a valid URL starting with http:// or https://');
      return;
    }

    if (!consent) {
      setError('You must confirm you have permission to test this application');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.startScan({
        target_url: targetUrl,
        max_depth: maxDepth,
      });
      navigate(`/scan/${response.scan_id}/progress`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start scan');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <Card>
          <h1 className="text-3xl font-bold text-gray-900 mb-6">
            Start New Security Scan
          </h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Target URL */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target URL *
              </label>
              <input
                type="text"
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
                placeholder="http://localhost:5001"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                required
              />
              <p className="mt-1 text-sm text-gray-500">
                Enter the full URL of the application to scan
              </p>
            </div>

            {/* Max Depth */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Maximum Crawl Depth
              </label>
              <input
                type="number"
                value={maxDepth}
                onChange={(e) => setMaxDepth(parseInt(e.target.value))}
                min="1"
                max="5"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              />
              <p className="mt-1 text-sm text-gray-500">
                How many levels deep to crawl (1-5, default: 2)
              </p>
            </div>

            {/* Consent Checkbox */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div className="flex items-start">
                <input
                  type="checkbox"
                  id="consent"
                  checked={consent}
                  onChange={(e) => setConsent(e.target.checked)}
                  className="mt-1 h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
                />
                <label htmlFor="consent" className="ml-3 text-sm text-gray-700">
                  <strong>I confirm that:</strong>
                  <ul className="mt-2 list-disc list-inside space-y-1">
                    <li>I own this application or have explicit permission to test it</li>
                    <li>I understand that unauthorized testing is illegal</li>
                    <li>I accept responsibility for any consequences of this scan</li>
                  </ul>
                </label>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            )}

            {/* Submit Buttons */}
            <div className="flex space-x-4">
              <Button
                type="submit"
                disabled={loading}
                className="flex-1"
              >
                {loading ? 'Starting Scan...' : 'Start Scan'}
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={() => navigate('/')}
                disabled={loading}
              >
                Cancel
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default NewScan;
