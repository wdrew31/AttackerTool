// TypeScript type definitions for AttackerTool

export interface ScanOptions {
  target_url: string;
  max_depth: number;
}

export interface ScanRequest {
  target_url: string;
  max_depth?: number;
  scan_type?: string;
}

export interface ScanResponse {
  scan_id: string;
  status: string;
  message?: string;
}

export type ScanStatus = 'queued' | 'crawling' | 'testing' | 'completed' | 'failed';

export type VulnerabilitySeverity = 'Critical' | 'High' | 'Medium' | 'Low' | 'Info';

export interface ScanResult {
  scan_id: string;
  target_url: string;
  status: ScanStatus;
  progress: number;
  start_time: string;
  end_time?: string;
  pages_crawled: number;
  input_points_found: number;
  vulnerabilities_found: number;
  vulnerabilities: Vulnerability[];
  summary?: {
    critical: number;
    high: number;
    medium: number;
    low: number;
    info: number;
  };
  error?: string;
}

export interface Vulnerability {
  type: string;
  subtype: string;
  severity: VulnerabilitySeverity;
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

export interface HealthStatus {
  status: string;
  timestamp: string;
}
