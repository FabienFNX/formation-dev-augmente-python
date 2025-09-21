#!/usr/bin/env python3
"""
Start script for the Loan Simulator application
Runs on port 8080 (same as Java version)
"""

import uvicorn
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'loan-simulator'))

if __name__ == "__main__":
    print("🚀 Starting Loan Simulator on http://localhost:8080")
    print("📁 Serving static files from Java project")
    print("📋 Available endpoints:")
    print("   - GET  /           → Frontend (HTML/CSS/JS)")
    print("   - POST /api/calculate-loan → Loan calculation")
    print("   - GET  /docs       → API documentation")
    print()

    uvicorn.run(
        "loan-simulator.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )