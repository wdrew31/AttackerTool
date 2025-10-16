import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import apiService from '../services/api';
import { ScanResult } from '../types';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [recentScans, setRecentScans] = useState<ScanResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [apiHealthy, setApiHealthy] = useState(false);

  useEffect(() => {
    checkApiHealth();
    loadRecentScans();
  }, []);

  const checkApiHealth = async () => {
    try {
      await apiService.checkHealth();
      setApiHealthy(true);
    } catch (error) {
      setApiHealthy(false);
      console.error('API health check failed:', error);
    }
  };

  const loadRecentScans = async () => {
    try {
      const scans = await apiService.listScans();
      // Get last 5 scans
      setRecentScans(scans.slice(0, 5));
    } catch (error) {
      console.error('Failed to load recent scans:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-status-completed';
      case 'failed':
        return 'text-status-failed';
      case 'running':
      case 'testing':
      case 'crawling':
        return 'text-status-running';
      default:
        return 'text-status-queued';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Warning Banner */}
        <div className="bg-red-50 border-l-4 border-red-600 p-4 mb-8">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-red-600"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-800">
                <strong>Important:</strong> Only scan applications you own or have explicit
                permission to test. Unauthorized security testing is illegal.
              </p>
            </div>
          </div>
        </div>

        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to AttackerTool
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Automated SQL Injection Security Scanner for Web Applications
          </p>
          
          {/* API Status */}
          <div className="flex justify-center items-center space-x-2 mb-6">
            <div
              className={`w-3 h-3 rounded-full ${
                apiHealthy ? 'bg-green-500' : 'bg-red-500'
              }`}
            />
            <span className="text-sm text-gray-600">
              {apiHealthy ? 'API Connected' : 'API Disconnected'}
            </span>
          </div>

          <Button size="lg" onClick={() => navigate('/scan/new')}>
            Start New Scan
          </Button>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <Card>
            <div className="text-center">
              <div className="w-12 h-12 bg-primary bg-opacity-10 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-6 h-6 text-primary"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Automated Scanning
              </h3>
              <p className="text-sm text-gray-600">
                Automatically crawls your web application and discovers potential vulnerabilities
              </p>
            </div>
          </Card>

          <Card>
            <div className="text-center">
              <div className="w-12 h-12 bg-primary bg-opacity-10 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-6 h-6 text-primary"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Detailed Reports
              </h3>
              <p className="text-sm text-gray-600">
                Get comprehensive reports with CVSS scores and remediation guidance
              </p>
            </div>
          </Card>

          <Card>
            <div className="text-center">
              <div className="w-12 h-12 bg-primary bg-opacity-10 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-6 h-6 text-primary"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                SQL Injection Detection
              </h3>
              <p className="text-sm text-gray-600">
                Detects error-based and blind SQL injection vulnerabilities
              </p>
            </div>
          </Card>
        </div>

        {/* Recent Scans */}
        <Card>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Recent Scans</h2>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => navigate('/history')}
            >
              View All
            </Button>
          </div>

          {loading ? (
            <div className="text-center py-8 text-gray-500">Loading...</div>
          ) : recentScans.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500 mb-4">No scans yet</p>
              <Button onClick={() => navigate('/scan/new')}>
                Start Your First Scan
              </Button>
            </div>
          ) : (
            <div className="space-y-3">
              {recentScans.map((scan) => (
                <div
                  key={scan.scan_id}
                  onClick={() => navigate(`/scan/${scan.scan_id}`)}
                  className="p-4 border border-gray-200 rounded-lg hover:border-primary hover:shadow-sm transition-all cursor-pointer"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 mb-1">
                        {scan.target_url}
                      </p>
                      <p className="text-sm text-gray-500">
                        {formatDate(scan.start_time)}
                      </p>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-900">
                          {scan.vulnerabilities_found} vulnerabilities
                        </p>
                        <p className={`text-sm font-medium ${getStatusColor(scan.status)}`}>
                          {scan.status}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default Home;
