#!/usr/bin/env python3
"""
Start both applications simultaneously
"""

import subprocess
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor

def start_loan_simulator():
    """Start the loan simulator on port 8080"""
    print("🏠 Starting Loan Simulator...")
    subprocess.run([sys.executable, "start-loan-simulator.py"])

def start_interest_rate_api():
    """Start the interest rate API on port 8081"""
    print("💰 Starting Interest Rate API...")
    subprocess.run([sys.executable, "start-interest-rate-api.py"])

if __name__ == "__main__":
    print("🚀 Starting both Python applications...")
    print("📍 Loan Simulator: http://localhost:8080")
    print("📍 Interest Rate API: http://localhost:8081")
    print("📍 API Documentation: http://localhost:8081/swagger-ui.html")
    print()
    print("Press Ctrl+C to stop both applications")
    print("=" * 50)

    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(start_loan_simulator),
                executor.submit(start_interest_rate_api)
            ]

            for future in futures:
                future.result()

    except KeyboardInterrupt:
        print("\n🛑 Stopping applications...")
        sys.exit(0)