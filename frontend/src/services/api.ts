// API service for communicating with AttackerTool backend

import axios, { AxiosInstance } from 'axios';
import {
  ScanRequest,
  ScanResponse,
  ScanResult,
  HealthStatus,
} from '../types';

// API base URL - configure based on environment
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for logging
    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  /**
   * Check API health status
   */
  async checkHealth(): Promise<HealthStatus> {
    const response = await this.client.get<HealthStatus>('/health');
    return response.data;
  }

  /**
   * Start a new security scan
   */
  async startScan(request: ScanRequest): Promise<ScanResponse> {
    const response = await this.client.post<ScanResponse>(
      '/api/scans/start',
      request
    );
    return response.data;
  }

  /**
   * Get scan status and results by ID
   */
  async getScan(scanId: string): Promise<ScanResult> {
    const response = await this.client.get<ScanResult>(`/api/scans/${scanId}`);
    return response.data;
  }

  /**
   * List all scans
   */
  async listScans(): Promise<ScanResult[]> {
    const response = await this.client.get<ScanResult[]>('/api/scans');
    return response.data;
  }

  /**
   * Delete a scan by ID
   */
  async deleteScan(scanId: string): Promise<void> {
    await this.client.delete(`/api/scans/${scanId}`);
  }

  /**
   * Get API root information
   */
  async getApiInfo(): Promise<any> {
    const response = await this.client.get('/');
    return response.data;
  }
}

// Export singleton instance
const apiService = new ApiService();
export default apiService;
