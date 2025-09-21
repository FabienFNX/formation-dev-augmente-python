#!/usr/bin/env python3
"""
Start script for the Interest Rate API application
Runs on port 8081 (same as Java version)
"""

import uvicorn
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'interest-rate-api'))

if __name__ == "__main__":
    print("🚀 Starting Interest Rate API on http://localhost:8081")
    print("📋 Available endpoints:")
    print("   - POST /api/interest-rate/calculate → Calculate interest rate")
    print("   - GET  /api/interest-rate/categories/age → Age categories")
    print("   - GET  /api/interest-rate/categories/professional → Professional categories")
    print("   - GET  /api/interest-rate/config → Current configuration")
    print("   - GET  /swagger-ui.html → API documentation")
    print()

    uvicorn.run(
        "interest-rate-api.main:app",
        host="0.0.0.0",
        port=8081,
        reload=True,
        log_level="info"
    )