"""
AttackerTool API
Main FastAPI application for web security scanning
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import logging

from app.scanner.crawler import WebCrawler
from app.modules.sql_injection import SQLInjectionTester

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AttackerTool API",
    description="Web Application Security Scanner - Phase 1: SQL Injection Testing",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for scans (will be replaced with database in Phase 2)
scans_db: Dict[str, Dict[str, Any]] = {}


class ScanRequest(BaseModel):
    """Request model for starting a new scan"""
    target_url: HttpUrl
    max_depth: Optional[int] = 2
    scan_type: Optional[str] = "sql_injection"


class ScanResponse(BaseModel):
    """Response model for scan status"""
    scan_id: str
    status: str
    message: Optional[str] = None


class ScanResult(BaseModel):
    """Detailed scan results"""
    scan_id: str
    target_url: str
    status: str
    progress: int
    start_time: str
    end_time: Optional[str] = None
    pages_crawled: int
    input_points_found: int
    vulnerabilities_found: int
    vulnerabilities: List[Dict[str, Any]]
    summary: Optional[Dict[str, int]] = None


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AttackerTool API",
        "version": "0.1.0",
        "description": "Web Application Security Scanner",
        "endpoints": {
            "start_scan": "POST /api/scans/start",
            "get_scan": "GET /api/scans/{scan_id}",
            "list_scans": "GET /api/scans",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/scans/start", response_model=ScanResponse)
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Start a new security scan
    
    Args:
        request: Scan configuration
        background_tasks: FastAPI background tasks
        
    Returns:
        Scan ID and status
    """
    scan_id = str(uuid.uuid4())
    target_url = str(request.target_url)
    
    # Initialize scan record
    scans_db[scan_id] = {
        "scan_id": scan_id,
        "target_url": target_url,
        "status": "queued",
        "progress": 0,
        "start_time": datetime.utcnow().isoformat(),
        "end_time": None,
        "pages_crawled": 0,
        "input_points_found": 0,
        "vulnerabilities_found": 0,
        "vulnerabilities": [],
        "summary": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        },
        "max_depth": request.max_depth,
        "scan_type": request.scan_type
    }
    
    # Run scan in background
    background_tasks.add_task(
        run_scan,
        scan_id=scan_id,
        target_url=target_url,
        max_depth=request.max_depth
    )
    
    logger.info(f"Scan {scan_id} queued for {target_url}")
    
    return ScanResponse(
        scan_id=scan_id,
        status="queued",
        message=f"Scan started for {target_url}"
    )


@app.get("/api/scans/{scan_id}", response_model=ScanResult)
async def get_scan(scan_id: str):
    """
    Get scan status and results
    
    Args:
        scan_id: UUID of the scan
        
    Returns:
        Scan results
    """
    if scan_id not in scans_db:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return scans_db[scan_id]


@app.get("/api/scans", response_model=List[ScanResult])
async def list_scans():
    """
    List all scans
    
    Returns:
        List of all scan results
    """
    return list(scans_db.values())


@app.delete("/api/scans/{scan_id}")
async def delete_scan(scan_id: str):
    """
    Delete a scan record
    
    Args:
        scan_id: UUID of the scan
        
    Returns:
        Deletion confirmation
    """
    if scan_id not in scans_db:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    del scans_db[scan_id]
    return {"message": f"Scan {scan_id} deleted"}


async def run_scan(scan_id: str, target_url: str, max_depth: int):
    """
    Execute the security scan (background task)
    
    Args:
        scan_id: UUID of the scan
        target_url: Target URL to scan
        max_depth: Maximum crawl depth
    """
    crawler = None
    tester = None
    
    try:
        # Update status to running
        scans_db[scan_id]["status"] = "crawling"
        scans_db[scan_id]["progress"] = 10
        logger.info(f"Scan {scan_id}: Starting crawl of {target_url}")
        
        # Initialize crawler
        crawler = WebCrawler(target_url, max_depth=max_depth)
        input_points = crawler.crawl()
        
        scans_db[scan_id]["pages_crawled"] = len(crawler.visited_urls)
        scans_db[scan_id]["input_points_found"] = len(input_points)
        scans_db[scan_id]["progress"] = 30
        
        logger.info(f"Scan {scan_id}: Found {len(input_points)} input points")
        
        if not input_points:
            scans_db[scan_id]["status"] = "completed"
            scans_db[scan_id]["progress"] = 100
            scans_db[scan_id]["end_time"] = datetime.utcnow().isoformat()
            logger.info(f"Scan {scan_id}: No input points found, scan complete")
            return
        
        # Start testing
        scans_db[scan_id]["status"] = "testing"
        logger.info(f"Scan {scan_id}: Starting SQL injection tests")
        
        # Initialize tester
        tester = SQLInjectionTester()
        all_vulnerabilities = []
        
        # Test each input point
        for i, input_point in enumerate(input_points):
            vulnerabilities = tester.test_input_point(input_point)
            all_vulnerabilities.extend(vulnerabilities)
            
            # Update progress (30% to 90%)
            progress = 30 + int((i + 1) / len(input_points) * 60)
            scans_db[scan_id]["progress"] = progress
        
        # Calculate summary statistics
        summary = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
        
        for vuln in all_vulnerabilities:
            severity = vuln.get("severity", "").lower()
            if severity in summary:
                summary[severity] += 1
        
        # Complete scan
        scans_db[scan_id]["status"] = "completed"
        scans_db[scan_id]["progress"] = 100
        scans_db[scan_id]["end_time"] = datetime.utcnow().isoformat()
        scans_db[scan_id]["vulnerabilities"] = all_vulnerabilities
        scans_db[scan_id]["vulnerabilities_found"] = len(all_vulnerabilities)
        scans_db[scan_id]["summary"] = summary
        
        logger.info(f"Scan {scan_id}: Complete. Found {len(all_vulnerabilities)} vulnerabilities")
        
    except Exception as e:
        logger.error(f"Scan {scan_id}: Error - {e}", exc_info=True)
        scans_db[scan_id]["status"] = "failed"
        scans_db[scan_id]["progress"] = 0
        scans_db[scan_id]["end_time"] = datetime.utcnow().isoformat()
        scans_db[scan_id]["error"] = str(e)
    
    finally:
        # Clean up resources
        if crawler:
            crawler.close()
        if tester:
            tester.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
