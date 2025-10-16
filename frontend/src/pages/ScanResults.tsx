import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import apiService from '../services/api';
import { ScanResult } from '../types';

const ScanResults: React.FC = () => {
  const { scanId } = useParams<{ scanId: string }>();
  const navigate = useNavigate();
  const [scan, setScan] = useState<ScanResult | null>(null);

  useEffect(() => {
    if (scanId) {
      apiService.getScan(scanId).then(setScan);
    }
  }, [scanId]);

  if (!scan) return <div className="p-8 text-center">Loading...</div>;

  const getSeverityColor = (severity: string) => {
    const colors: Record<string, string> = {
      Critical: 'bg-severity-critical',
      High: 'bg-severity-high',
      Medium: 'bg-severity-medium',
      Low: 'bg-severity-low',
    };
    return colors[severity] || 'bg-gray-500';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <Button variant="secondary" onClick={() => navigate('/')}>
            ← Back to Home
          </Button>
        </div>

        <Card className="mb-6">
          <h1 className="text-3xl font-bold mb-4">Scan Results</h1>
          <p className="text-gray-600 mb-2">Target: {scan.target_url}</p>
          <p className="text-gray-600">Status: {scan.status}</p>
        </Card>

        {scan.summary && (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
            {Object.entries(scan.summary).map(([severity, count]) => (
              <Card key={severity}>
                <p className="text-sm text-gray-600 capitalize">{severity}</p>
                <p className="text-3xl font-bold">{count}</p>
              </Card>
            ))}
          </div>
        )}

        <Card>
          <h2 className="text-2xl font-bold mb-4">
            Vulnerabilities ({scan.vulnerabilities.length})
          </h2>
          {scan.vulnerabilities.length === 0 ? (
            <p className="text-center py-8 text-gray-500">
              No vulnerabilities found
            </p>
          ) : (
            <div className="space-y-4">
              {scan.vulnerabilities.map((vuln, idx) => (
                <div key={idx} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="font-semibold text-lg">{vuln.type}</h3>
                      <p className="text-sm text-gray-600">{vuln.subtype}</p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-white text-sm ${getSeverityColor(vuln.severity)}`}>
                      {vuln.severity}
                    </span>
                  </div>
                  <div className="text-sm space-y-1 text-gray-600">
                    <p><strong>URL:</strong> {vuln.url}</p>
                    <p><strong>Parameter:</strong> {vuln.parameter}</p>
                    <p><strong>CVSS:</strong> {vuln.cvss_score}</p>
                    <p><strong>CWE:</strong> {vuln.cwe}</p>
                    <details className="mt-2">
                      <summary className="cursor-pointer font-medium">Remediation</summary>
                      <p className="mt-2">{vuln.remediation.summary}</p>
                    </details>
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

export default ScanResults;
