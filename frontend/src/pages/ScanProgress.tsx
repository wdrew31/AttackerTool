import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import apiService from '../services/api';
import { ScanResult } from '../types';

const ScanProgress: React.FC = () => {
  const { scanId } = useParams<{ scanId: string }>();
  const navigate = useNavigate();
  const [scan, setScan] = useState<ScanResult | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!scanId) return;

    const pollInterval = setInterval(async () => {
      try {
        const result = await apiService.getScan(scanId);
        setScan(result);

        if (result.status === 'completed' || result.status === 'failed') {
          clearInterval(pollInterval);
          if (result.status === 'completed') {
            setTimeout(() => navigate(`/scan/${scanId}`), 1000);
          }
        }
      } catch (err) {
        setError('Failed to fetch scan status');
        clearInterval(pollInterval);
      }
    }, 2000);

    return () => clearInterval(pollInterval);
  }, [scanId, navigate]);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-3xl mx-auto px-4">
          <Card>
            <div className="text-center text-red-600">{error}</div>
          </Card>
        </div>
      </div>
    );
  }

  if (!scan) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-3xl mx-auto px-4">
          <Card>
            <div className="text-center">Loading...</div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <Card>
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Scan Progress</h1>
          
          <div className="space-y-6">
            {/* Progress Bar */}
            <div>
              <div className="flex justify-between text-sm text-gray-600 mb-2">
                <span>Progress</span>
                <span>{scan.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className="bg-primary h-4 rounded-full transition-all duration-500"
                  style={{ width: `${scan.progress}%` }}
                />
              </div>
            </div>

            {/* Status */}
            <div>
              <p className="text-sm text-gray-600 mb-1">Status</p>
              <p className="text-lg font-semibold capitalize">{scan.status}</p>
            </div>

            {/* Statistics */}
            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-600">Pages Crawled</p>
                <p className="text-2xl font-bold">{scan.pages_crawled}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Input Points</p>
                <p className="text-2xl font-bold">{scan.input_points_found}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Vulnerabilities</p>
                <p className="text-2xl font-bold text-red-600">
                  {scan.vulnerabilities_found}
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ScanProgress;
